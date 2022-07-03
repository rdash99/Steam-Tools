import requests as r
import json


def getInventory(id):
    url = "https://steamcommunity.com/inventory/{}/753/6?l=english&count=5000".format(
        id)
    data = r.get(url)
    inv = data.json()
    with open("{}.json".format(str(id)), "w") as f:
        f.write(json.dumps(inv))
    f.close()


def findDupes(id):
    with open("{}.json".format(str(id)), "r") as f:
        data = json.loads(f.read())
    f.close()

    with open("{}.json".format(str(id)), "r") as f:
        descriptions = json.loads(f.read())
    f.close()

    descriptions = descriptions["descriptions"]

    items = data["assets"]
    found = []
    dupes = []
    for i in items:
        if i["classid"] in found:
            dupes.append(i)
        else:
            found.append(i["classid"])
    print(data["total_inventory_count"] - len(found))

    with open("{}_dupes.json".format(str(id)), "w") as f:
        f.write(json.dumps(dupes))
    f.close()
    checkSellable(id)


def checkSellable(id):
    with open("{}_dupes.json".format(str(id)), "r") as f:
        items = json.loads(f.read())
    f.close()

    with open("{}.json".format(str(id)), "r") as f:
        descriptions = json.loads(f.read())
    f.close()

    descriptions = descriptions["descriptions"]

    sellable = []
    unsellable = []
    for i in items:
        for j in descriptions:
            if j["instanceid"] != "0" and j["classid"] == i["classid"]:
                if j["marketable"] == 1:
                    sellable.append(j)
                else:
                    unsellable.append(j)

    with open("{}_sellabledupes.json".format(str(id)), "w") as f:
        f.write(json.dumps(sellable))
    f.close()

    with open("{}_sellabledupesNames.txt".format(str(id)), "w") as f:
        for i in sellable:
            f.write(str(i["name"]))
            f.write("\n")
    f.close()

    with open("{}_unsellabledupesNames.txt".format(str(id)), "w") as f:
        for i in unsellable:
            f.write(str(i["name"]))
            f.write("\n")
    f.close()

    with open("{}_unsellabledupes.json".format(str(id)), "w") as f:
        f.write(json.dumps(unsellable))
    f.close()


def getGemValue(appID, itemType):
    url = "http://steamcommunity.com/auction/ajaxgetgoovalueforitemtype/?appid={}&item_type={}".format(
        appID, itemType)
    data = r.get(url)
    response = data.json()
    gem_value = response["goo_value"]
    return gem_value


def getItemValue(appID, market_hash_name):
    url = "http://steamcommunity.com/market/priceoverview/?appid={}&currency=2&market_hash_name={}".format(
        appID, market_hash_name)
    data = r.get(url)
    response = data.json()
    itemValue = int(float(response['lowest_price'][1:]) * 100)
    print(itemValue)
    return itemValue


def sellItem(itemInfo, sessionid, price):
    url = "http://steamcommunity.com/market/sellitem/"
    params = {"appid": itemInfo["appid"], "assetid": itemInfo["assetid"],
              "contextid": itemInfo["contextid"], "sessionid": sessionid, "price": price}
    headers = {"Referer": "https://steamcommunity.com/id/zugglybug/inventory/",
               "DNT": "1", "Origin": "https://steamcommunity.com"}
    data = r.post(url, params=params, headers=headers)
    response = data.json()
    assert response.status_code == 200
    return response
    # https://steamcommunity.com/market/sellitem/
    '''sessionid: 84f127b01e60b00f49ac8372
appid: 753
contextid: 6
assetid: 19990898507
amount: 1
price: 3'''


getInventory(76561198261714500)


findDupes(76561198261714500)

getItemValue("753", "998740-Mimic")

# code to enter required information of sessionid and steamid
""" sessionid = input("Enter sessionid: ")
steamid = input("Enter steamid: ") """
