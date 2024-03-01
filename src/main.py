import time, psutil, argparse
from pypresence import Presence

rpc = None
connected = False
wait = 15

def connect():
    global connected
    global wait
    try:
        rpc = Presence(client_id="1193490043612971030")
        print("Connecting...")
        rpc.connect()
        print("Connected.")
        connected = True
        wait = 15
        return rpc
    except Exception:
        print("Could not connect!")
        if wait < 30:
            wait += 5
        return None

def disconnect():
    global connected
    global rpc
    if rpc is not None:
        print("Disconnecting...")
        rpc.close()
        print("Disconnected.")
        rpc = None
    connected = False

def is_running():
    global process_blacklist
    if process_blacklist is not None:
        for process in psutil.process_iter():
            if process.name() in process_blacklist:
                print(f"Blacklisted process '{process.name()}' detected!")
                return True
    return False

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--blacklist", "-b", required=False)
arguments = argument_parser.parse_args()

if arguments.blacklist is None:
    process_blacklist = None
else:
    try:
        process_blacklist_file = open(arguments.blacklist, "r")
        process_blacklist = set(line.strip() for line in process_blacklist_file.readlines())
        print(f"Blacklist '{arguments.blacklist}' loaded.")
    except Exception:
        print(f"File '{arguments.blacklist}' not found or no permission!")
        exit(1)

try:
    while True:
        try:
            if is_running():
                disconnect()
            else:
                if rpc is None:
                    rpc = connect()
                rpc.update(details="Join SecSchool today!", large_image="secschool", large_text="SecSchool", buttons=[{"label": "Website", "url": "https://secschool.net"}, {"label": "Discord", "url": "https://discord.gg/2bWxKHn8Yd"}])
        except Exception:
            if connected:
                print("Connection lost!")
                rpc = None
                disconnect()
            print(f"Trying to reconnect in {wait} seconds.")
        # Rate Limit (15s):  https://discord.com/developers/docs/rich-presence/how-to#updating-presence
        time.sleep(wait)
except KeyboardInterrupt:
    disconnect()