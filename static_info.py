from subprocess import run, PIPE
import sys


VERSION = "b0.1"
COMMIT = "could not get commit."
SHORT_COMMIT = "ERROR"

if __name__ == "__main__":
    print("Please run controller.py and not this file.")
    sys.exit()

try:
    commit = run("git log -n 1 --pretty=format:\"%H\"", stdout=PIPE, stderr=PIPE, shell=True, check=True)
    COMMIT = commit.stdout.decode('utf-8')
    short_commit = run("git rev-parse --short HEAD", stdout=PIPE, stderr=PIPE, shell=True, check=True)
    SHORT_COMMIT = short_commit.stdout.decode('utf-8').replace("\n", "")
except Exception as e:
    print(f"Could not find current commit: {e}")
