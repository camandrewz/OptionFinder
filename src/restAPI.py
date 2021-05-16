import requests
import json


def getContracts():
    url = "https://api.ledgerx.com/trading/contracts"

    querystring = {"active": "true", "derivative_type": "options_contract"}
    headers = {"Accept": "application/json"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    jsonObj = json.loads(response.text)

    return jsonObj


def createNewContractObject(obj):

    contract = {"type": obj["type"], "strike": (obj["strike_price"]/100), "expiration": obj["date_expires"],
                "underlying": obj["underlying_asset"], "collateral": obj["collateral_asset"], "open_interest": obj["open_interest"], "multiplier": obj["multiplier"]}

    return contract


def createContractDictionary():

    json = getContracts()
    contractsDict = {}

    for obj in json["data"]:

        #if (obj["collateral_asset"] == "USD"):
        key = obj["id"]
        contractsDict[key] = createNewContractObject(obj)

    return contractsDict
