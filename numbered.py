import argparse
import os
import json
import subprocess

HERDR_BIN = os.getenv("HERDR_BIN_PATH", "herdr")
SEPERATOR = " "


def herdr_run(cmds):
    cmd = [HERDR_BIN]
    cmd.extend(cmds)
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout) if not res.returncode else {}


def get_name(number, label):
    split = label.split(SEPERATOR)
    prefix = split[0]
    label_new = label

    if prefix.isdigit():
        prefix = int(prefix)
        if prefix == number:
            return True, label_new

        label_new = SEPERATOR.join(split[1:])

    return False, f"{number}{SEPERATOR}{label_new}"


def rename_ws(ws):
    number = ws.get("number")
    label = ws.get("label")
    skip, name = get_name(number, label)
    if skip:
        return

    herdr_run(["workspace", "rename", ws.get("workspace_id"), name])


def handle_workspace():
    all_ws = herdr_run(["workspace", "list"])["result"]["workspaces"]
    for ws in all_ws:
        rename_ws(ws)


def main():
    handle_workspace()


if __name__ == "__main__":
    main()
