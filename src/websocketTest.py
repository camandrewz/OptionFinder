# Import WebSocket client library (and others)
import websocket
import _thread
import time
import json

# Define WebSocket callback functions


def ws_message(ws, message):

    if message["type"] == "action_report":
        print("WebSocket thread: %s" % message)


def ws_open(ws):
    #ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')
    print("WebSocket Opened")


def ws_thread(*args):
    ws = websocket.WebSocketApp(
        "wss://api.ledgerx.com/ws?presence=true", on_open=ws_open, on_message=ws_message)
    ws.run_forever()

# Start a new thread for the WebSocket interface
#_thread.start_new_thread(ws_thread, ())


# Continue other (non WebSocket) tasks in the main thread
while True:
    time.sleep(5)
    print("Main thread: %d" % time.time())
