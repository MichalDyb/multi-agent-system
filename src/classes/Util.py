import json

def buildDict(msgType: str, msgFor: str, msgData: dict) -> dict:
    data = {
        "MSG_TYPE": msgType,
        "FOR": msgFor,
        "DATA": msgData
    }
    return data

def encodeJSON(data: dict) -> str:
    return json.dumps(data)

def decodeJSON(data: str) -> dict:
    return json.loads(data)

def minimum(table: list) -> dict:
    minElem = None
    for element in table:
        if minElem is None:
            minElem = element
        if element["Dist"] < minElem["Dist"]:
            minElem = element
    for element in reversed(table):
        if minElem is None:
            minElem = element
        if element["Dist"] < minElem["Dist"]:
            minElem = element
    return minElem