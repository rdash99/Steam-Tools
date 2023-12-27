import requests as r
import json


def getInventory(id):
    url = "https://steamcommunity.com/inventory/{}/753/6?l=english&count=5000".format(
        id)
    data = r.get(url)
    print("Inventory data received")
    print(data)
    inv = data.json()
    last = inv["assets"][len(inv["assets"])-1]["assetid"]
    with open("{}/{}.json".format(str(id), str(id)), "w") as f:
        f.write(json.dumps(inv))
    f.close()
    if inv['total_inventory_count'] > 5000:
        print("Inventory is over 5000 items, getting next page")
        url = "https://steamcommunity.com/inventory/{}/753/6?l=english&count=5000&start_assetid={}".format(
            id, last)
        with open("{}/{}.json".format(str(id), str(id)), "w") as f:
            f.append(json.dumps(inv))
        f.close()
        


def findDupes(id):
    try:
        with open("{}/{}.json".format(str(id), str(id)), "r") as f:
            data = json.loads(f.read())
        f.close()

    except IOError:
        getInventory(id)
        with open("{}/{}.json".format(str(id), str(id)), "r") as f:
            data = json.loads(f.read())
        f.close()

    with open("{}/{}.json".format(str(id), str(id)), "r") as f:
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
    print(str(len(dupes)) + " items found")
    print("Splitting into sellable and unsellable")

    with open("{}/{}_dupes.json".format(str(id), str(id)), "w") as f:
        f.write(json.dumps(dupes))
    f.close()
    checkSellable(id)


def checkSellable(id):
    with open("{}/{}_dupes.json".format(str(id), str(id)), "r") as f:
        items = json.loads(f.read())
    f.close()

    with open("{}/{}.json".format(str(id), str(id)), "r") as f:
        descriptions = json.loads(f.read())
    f.close()

    descriptions = descriptions["descriptions"]

    sellable = []
    unsellable = []
    for i in items:
        for j in descriptions:
            if j["instanceid"] != "0" and j["classid"] == i["classid"]:
                if j["marketable"] == 1:
                    sellable.append(formatDupe(j, i))
                else:
                    unsellable.append(formatDupe(j, i))
    print(str(len(sellable)) + " items found to sell")
    print(str(len(unsellable)) + " items found to convert to gems")
    with open("{}/{}_sellabledupes.json".format(str(id), str(id)), "w") as f:
        f.write(json.dumps(sellable))
    f.close()

    with open("{}/{}_sellabledupesNames.txt".format(str(id), str(id)), "w") as f:
        for i in sellable:
            f.write(str(i["name"]))
            f.write("\n")
    f.close()

    with open("{}/{}_unsellabledupesNames.txt".format(str(id), str(id)), "w") as f:
        for i in unsellable:
            f.write(str(i["name"]))
            f.write("\n")
    f.close()

    with open("{}/{}_unsellabledupes.json".format(str(id), str(id)), "w") as f:
        f.write(json.dumps(unsellable))
    f.close()


def formatDupe(description, item):
    data = {
        "name": description["name"],
        "classid": description["classid"],
        "market_hash_name": description["market_hash_name"],
        "market_fee_app": description["market_fee_app"],
        "commodity": description["commodity"],
        "tradable": description["tradable"],
        "marketable": description["marketable"],
        "appid": description["appid"],
        "instanceid": item["instanceid"],
        "contextid": item["contextid"],
        "assetid": item["assetid"],
    }
    return data
