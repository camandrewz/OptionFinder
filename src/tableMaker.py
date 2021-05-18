from terminaltables import AsciiTable
from dateutil.parser import parse


def createTable(contractsDict):

    table_data = [
        ['Type', 'Strike', 'Expiration', "Underlying", "Collateral", "Open Interest", "Multiplier", "Ask", "Bid", "Ask per Contract", "Bid per Contract"]]

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
            list.append(contractsDict["ask"])
            list.append(contractsDict["bid"])
            list.append(contractsDict["ask"]/100)
            list.append(contractsDict["bid"]/100)
        else:
            list.append("N/A")
            list.append("N/A")
            list.append("N/A")
            list.append("N/A")

        table_data.append(list)

    table = AsciiTable(table_data)
    return table
