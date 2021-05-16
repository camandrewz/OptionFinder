import restAPI
import websocket
import _thread
import time
import json
import datetime
from dateutil.parser import parse
from terminaltables import AsciiTable


def main():

    contracts = restAPI.createContractDictionary()

    # Define WebSocket callback functions
    def ws_message(ws, message):

        msg = json.loads(message)

        # print("WebSocket thread: ", msg)

        if msg["contract_id"] in list(contracts.keys()):
            contracts[msg["contract_id"]]["ask"] = msg["ask"]/100
            contracts[msg["contract_id"]]["bid"] = msg["bid"]/100

            # print(contracts[msg["contract_id"]])

    def ws_open(ws):
        # ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')
        print("WebSocket Opened")

    def ws_thread(*args):
        ws = websocket.WebSocketApp(
            "wss://api.ledgerx.com/ws?presence=true", on_open=ws_open, on_message=ws_message)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread, ())

    while True:
        time.sleep(5)

        table_data = [
            ['Type', 'Strike', 'Expiration', "Underlying", "Collateral", "Open Interest", "Multiplier", "Ask", "Bid"]]

        for contract in contracts.values():

            list = []

            list.append(contract["type"])
            list.append(contract["strike"])

            date = parse(contract["expiration"])

            list.append(date.strftime('%m/%d/%Y'))
            list.append(contract["underlying"])
            list.append(contract["collateral"])
            list.append(contract["open_interest"])
            list.append(contract["multiplier"])

            if ("ask" in contract.keys()):
                list.append(contract["ask"])
                list.append(contract["bid"])
            else:
                list.append("N/A")
                list.append("N/A")

            table_data.append(list)

        table = AsciiTable(table_data)
        print(table.table)
        print("Main thread: %d" % time.time())


if __name__ == "__main__":
    main()
