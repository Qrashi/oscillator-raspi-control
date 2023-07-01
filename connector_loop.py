import re
import select
import subprocess
import threading

from display import SmartDisplay
from static_info import VERSION, SHORT_COMMIT
import socket
from time import sleep
from keyinput import init as init_keyinput
from keyinput.button_manager import ButtonManager

from datetime import datetime

display: SmartDisplay


class ConnectorState:
    camera_link_last_ping: int = 0
    tracker_link_last_ping: int = 0
    cl_socket: socket.socket
    tl_socket: socket.socket
    ip: str = ""
    ready: bool = False


class LogicState():
    stage: str = "waiting_user"
    timer: float
    interval: float = 0.01


"""
States:
1. waiting_user: waiting for user to set-up experiment and bring experiment into neutral position, press
2. waiting_user_confirm: waiting for user to confirm that springs are in neutral position , press, send photo + trackID 
3. waiting_neutral_photo: waiting for cl to confirm neutral phase photo, cl status "ready"
4. waiting_tl: waiting for user to enter experiment data into tracking link, tl status "ready"
5. waiting_angle: waiting for user to set springs into start position, conformation will start recording on cl, 2x press
6. waiting_recording: wait for recording to start, cl status "recording"
7. waiting_experiment_start: wait for user to release springs, release
8. running: experiment is running, press send complete
9. waiting_experiment_end: wait until all links are ready to receive again, receive reset_confirm 
"""


class UnsupportedProtocolException(Exception):
    ...


class TrackerState:
    current_tracking_id: int = 0
    ready: bool = False
    protocol_version: int = 0


class CameraState:
    recording: bool = False
    ready: bool = False
    protocol_version: int = 0
    """
    Camera communication:
    0. state
    1. trackingID:ID
    2. neutral_photo
    3. photo_confirm
    """


CAMERA_PROTOCOL = 1
TRACKER_PROTOCOL = 1

state = ConnectorState()
camera = CameraState()
tracker = TrackerState()
experiment = LogicState()

#
def init_ip():
    # Fetch IP address
    result = subprocess.check_output(['ip', 'addr']).decode('utf-8')
    ip_addresses = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', result)
    filtered_addresses = [ip for ip in ip_addresses if ip.startswith('192')]
    if len(filtered_addresses) < 1:
        # Probably not using correct wi-fi
        state.ip = ""
        return
    state.ip = filtered_addresses[0]


def init_loop(displ: SmartDisplay):
    global display
    display = displ
    state.cl_socket = socket.socket()
    state.cl_socket.bind(('', 12735))
    state.cl_socket.listen(1)
    state.tl_socket = socket.socket()
    state.tl_socket.bind(('', 12736))
    state.tl_socket.listen(1)
    threading.Thread(target=start_display_loop, args=()).start()
    threading.Thread(target=start_logic_loop, args=())


def start_logic_loop():
    keyinput = init_keyinput()
    while True:
        check_buttons(keyinput)
        sleep(experiment.interval)



def check_buttons(button_module: ButtonManager):
    if state.ready:
        if experiment.stage == "waiting_user":
            if button_module.confirmed():
                experiment.stage = "waiting_user_confirm"
                update_display()
                state.cl_socket.send("trackingID:" + str(tracker.current_tracking_id))
        elif experiment.stage == "waiting_user_confirm":
            if button_module.confirmed():
                state.cl_socket.send("neutral_photo".encode('utf-8'))
                experiment.stage = "waiting_neutral_photo"
                update_display()
    else:
        if button_module.confirmed() or button_module.experiment():
            print("reg")
            display.center(3, "[press] registered!")

def handle_message(client_socket: socket.socket, connection_type: str):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode('utf-8')
        if connection_type == "cl":
            state.camera_link_last_ping = datetime.now().timestamp()
            if experiment.stage == "waiting_neutral_photo":
                if message == "photo_confirm":
                    experiment.stage = "waiting_tl"
                    update_display()
                    continue

        else:
            state.tracker_link_last_ping = datetime.now().timestamp()
        if message == "ping":
            client_socket.send("ping".encode('utf-8'))
            continue
        if message.startswith("state"):
            # state update
            if connection_type == "cl":
                if int(re.findall(r'protocol:(\d+)', message)[0]) != CAMERA_PROTOCOL:
                    raise UnsupportedProtocolException(
                        f"camera protocol version not compatible with local version ({CAMERA_PROTOCOL})")
                camera.ready = bool(int(re.findall(r'ready:(\d+)', message)[0]))
                camera.recording = bool(int(re.findall(r'recording:(\d+)', message)[0]))
            if connection_type == "tl":
                if int(re.findall(r'protocol:(\d+)', message)[0]) != TRACKER_PROTOCOL:
                    raise UnsupportedProtocolException(
                        f"tracker protocol version not compatible with local version ({TRACKER_PROTOCOL})")
                tracker.current_tracking_id = int(re.findall(r'tracking_id:(\d+)', message)[0])
                tracker.ready = bool(int(re.findall(r'ready:(\d+)', message)[0]))

    client_socket.close()


def accept_connections():
    while True:
        ready, _, _ = select.select([state.cl_socket, state.tl_socket], [], [], 0)
        for sock in ready:
            if sock == state.tl_socket:
                client, _ = state.tl_socket.accept()
                threading.Thread(target=handle_message, args=(client, "tl")).start()

            else:
                client, _ = state.cl_socket.accept()
                threading.Thread(target=handle_message, args=(client, "cl")).start()
            if state.camera_link_last_ping != 0 and state.tracker_link_last_ping != 0:
                state.ready = True


def start_display_loop():
    while True:
        update_display()
        sleep(0.5)


UNKNOWN_MSG = "???"


def update_display():
    # refresh display
    if state.ready:
        if experiment.stage not in ["waiting_user_confirm"]: display.left_right(0, f"orc {VERSION}", datetime.now().strftime("%H:%M:%S"))
        if experiment.stage == "waiting_user":
            display.center(1, "set up parameters")
            display.center(2, "[press] to continue")
            display.right(3, f"#{tracker.current_tracking_id if tracker.current_tracking_id != 0 else UNKNOWN_MSG}")
        elif experiment.stage == "waiting_user_confirm":
            display.center(0, "ensure that springs")
            display.center(1, "are in ! NEUTRAL !")
            display.center(2, "position +HANDS OFF!")
            display.center(3, "[press] to continue")
        elif experiment.stage == "waiting_neutral_photo":
            display.center(1, "DO NOT TOUCH")
            display.center(2, "photo in progress")
            display.right(3, f"#{tracker.current_tracking_id if tracker.current_tracking_id != 0 else UNKNOWN_MSG}")
        elif experiment.stage == "waiting_tl":
            display.center(1, "continue on tracker")
            display.center(2, "waiting...")
            display.right(3, f"#{tracker.current_tracking_id if tracker.current_tracking_id != 0 else UNKNOWN_MSG}")
        elif experiment.stage == "waiting_angle":
            display.center(1, "asd")

    else:
        display.left_right(0, f"orc {VERSION}", datetime.now().strftime("%H:%M:%S"))
        # set-up not complete
        if state.ip == "":
            # IP address not set
            init_ip()
            if state.ip == "":
                # IP still unset (wrong Wi-Fi)
                display.center(1, "init (link)")
                display.center(2, "X wrong Wi-Fi X")
                return

        display.center(3, "ready to connect")
        if datetime.now().second % 4 < 2:
            display.center(1, "x camera link x" if state.camera_link_last_ping == 0 else "OK camera link OK")
        else:
            display.center(1, "x tracker link x" if state.tracker_link_last_ping == 0 else "OK tracker link OK")

        display.center(2, state.ip)


