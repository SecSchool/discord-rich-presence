import time
from pypresence import Presence

connected = False
wait = 10

def connect():
    global connected
    global wait
    try:
        rpc = Presence(client_id="1193490043612971030")
        print("Connecting...")
        rpc.connect()
        print("Connected.")
        connected = True
        wait = 10
        return rpc
    except Exception:
        print("Could not connect!")
        if wait < 30:
            wait += 5
        return None

rpc = connect()
try:
    while True:
        try:
            if rpc is None:
                rpc = connect()
            rpc.update(details="Join SecSchool today!", large_image="secschool", large_text="SecSchool", buttons=[{"label": "Website", "url": "https://secschool.net"}, {"label": "Discord", "url": "https://discord.gg/2bWxKHn8Yd"}])
        except Exception:
            if connected:
                print("Connection lost!")
                connected = False
                rpc = None
            print(f"Trying to reconnect in {wait} seconds.")
        time.sleep(wait)
except KeyboardInterrupt:
    if rpc is not None:
        rpc.close()