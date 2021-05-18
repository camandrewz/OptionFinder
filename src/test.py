import restAPI
import tableMaker
import websocket
import _thread
import time
import json
import os

def main():

    contracts = restAPI.createContractDictionary()

    # Function to clear std out
    def clear():
        os.system( 'cls' )

    # Define WebSocket callback functions
    def ws_message(ws, message):

        msg = json.loads(message)

        if msg["contract_id"] in list(contracts.keys()):
            contracts[msg["contract_id"]]["ask"] = msg["ask"]/100
            contracts[msg["contract_id"]]["bid"] = msg["bid"]/100

    def ws_open(ws):
        print("WebSocket Opened")

    def ws_thread(*args):
        ws = websocket.WebSocketApp("wss://api.ledgerx.com/ws?presence=true", on_open=ws_open, on_message=ws_message)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread, ())

    while True:
        time.sleep(5)

        clear()
        print(tableMaker.createTable(contracts).table)
        print("Main thread: %d" % time.time())


if __name__ == "__main__":
    main()
