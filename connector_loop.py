import re
import select
import subprocess
import threading

from display import SmartDisplay
from static_info import VERSION
import socket
from time import sleep

from datetime import datetime

display: SmartDisplay


class ConnectorState:
    camera_link_last_ping: int = 0
    tracker_link_last_ping: int = 0
    cl_socket: socket
    tl_socket: socket
    ip: str = ""


state = ConnectorState()


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
    pass


def handle_message(client_socket, connection_type: str):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode()
        if connection_type == "cl":
            state.camera_link_last_ping = datetime.now().timestamp()
        else:
            state.tracker_link_last_ping = datetime.now().timestamp()
        if message == "ping":
            continue

    client_socket.close()


def accept_connections():
    while True:
        ready, _, _ = select.select([state.cl_socket, state.tl_socket], [], [], 0)
        for sock in ready:
            if sock == state.tl_socket:
                client, _ = state.tl_socket.accept()
                threading.Thread(target=handle_message, args=(client, "cl")).start()
            else:
                client, _ = state.cl_socket.accept()
                threading.Thread(target=handle_message, args=(client, "tl")).start()


def start_display_loop():
    while True:
        update_display()
        sleep(0.5)


def update_display():
    # refresh display
    display.left_right(0, f"orc {VERSION}", datetime.now().strftime("%H:%M:%S"))
    if state.ip == "":
        # IP address not set
        init_ip()
        if state.ip == "":
            # IP still unset (wrong Wi-Fi)
            display.center(1, "init (link)")
            display.center(2, "X wrong Wi-Fi X")
            return

    display.center(3, "please connect")
    display.center(1, "cam " + (
        "X" if state.camera_link_last_ping == 0 else "OK") + " tracking " + "X" if state.tracker_link_last_ping == 0 else "OK")
    display.center(2, state.ip)
