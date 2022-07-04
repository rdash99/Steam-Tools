import requests as r
import json


def getInventory(id):
    url = "https://steamcommunity.com/inventory/{}/753/6?l=english&count=5000".format(
        id)
    data = r.get(url)
    inv = data.json()
    with open("{}/{}.json".format(str(id), str(id)), "w") as f:
        f.write(json.dumps(inv))
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
    print(data["total_inventory_count"] - len(found))

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
                    sellable.append(j)
                else:
                    unsellable.append(j)

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


# getInventory(76561198261714500)


# findDupes(76561198261714500)


# code to enter required information of sessionid and steamid
""" sessionid = input("Enter sessionid: ")
steamid = input("Enter steamid: ") """
