import errors
from display import init
from connector_loop import init_loop
from errors import report_error, context
from static_info import VERSION, SHORT_COMMIT
from singlejson import load
from file_defaults import CONFIG
from subprocess import run, PIPE
import os
import sys
import socket


from datetime import datetime

context.code = "controller"
context.task = "initialisation"

def initialize():
    """
    Initialize all controller functionality
    :return:
    """
    errors.context.code = "controller"
    errors.context.task = "display initialisation"
    display = init()
    display.left_right(0, f"orc {VERSION}", datetime.now().strftime("%H:%M")+":??")
    display.center(1, "init (hw)")
    display.center(2, "display")
    display.center(3, f"git: {SHORT_COMMIT}")

    config = load("config.json", default=CONFIG).json

    context.task = "checking for git-updates"
    if config["git_update"]:
        display.center(1, "init (git)")
        display.center(2, "fetching [1/2]")
        context.task = "git fetch"
        code = run("git fetch", stdout=PIPE, stderr=PIPE, shell=True)
        if code.returncode != 0:
            # Wrong return code
            display.center(2, "fetch error")
            report_error("Could not fetch git updates! code: " + str(code.returncode),
                         exception="Log: stdout:\n" + str(code.stdout) + "\nstderr:\n" + str(code.stderr))
        else:
            if not code.stdout.decode('utf-8').endswith(" "):
                # Update found
                display.center(2, "downloading [2/2]")
            context.task = "git pull"
            code = run("git pull", stdout=PIPE, stderr=PIPE, shell=True)
            if code.returncode != 0:
                display.center(2, "dl error")
                report_error("Could not pull git updates! code: " + str(code.returncode),
                             exception="Log: stdout:\n" + str(code.stdout) + "\nstderr:\n" + str(code.stderr))
            else:
                context.task = "update commit"
                if not code.stdout.decode('utf-8').endswith("up to date.\n"):
                    display.center(2, "updated, restarting")
                    print("restarting!")
                    os.execl(sys.executable, sys.executable, *sys.argv)

    display.center(1, "init (link)")
    display.center(2, "finding IP")

    context.code = "connector init"
    context.task = "ip address fetch"
    init_loop(display)

if __name__ == "__main__":
    initialize()
else:
    report_error("controller not main!")