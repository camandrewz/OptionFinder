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

    def createTable(contractsDict):
        table_data = [
            ['Type', 'Strike', 'Expiration', "Underlying", "Collateral", "Open Interest", "Multiplier", "Ask", "Bid"]]

        for contractsDict in contractsDict.values():

            list = []

            list.append(contractsDict["type"])
            list.append(contractsDict["strike"])

            date = parse(contractsDict["expiration"])

            list.append(date.strftime('%m/%d/%Y'))
            list.append(contractsDict["underlying"])
            list.append(contractsDict["collateral"])
            list.append(contractsDict["open_interest"])
            list.append(contractsDict["multiplier"])

            if "ask" in contractsDict.keys():
                list.append(contractsDict["ask"]/100)
                list.append(contractsDict["bid"]/100)
            else:
                list.append("N/A")
                list.append("N/A")

            table_data.append(list)

        table = AsciiTable(table_data)
        return table

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread, ())

    while True:
        time.sleep(5)

        print(createTable(contracts).table)
        print("Main thread: %d" % time.time())


if __name__ == "__main__":
    main()
