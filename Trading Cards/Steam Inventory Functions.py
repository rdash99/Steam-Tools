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
    items = data["descriptions"]
    found = []
    dupes = []
    for i in items:
        if i["name"] in found:
            dupes.append(i)
            print(str(len(dupes)) + " found")
        else:
            found.append(i["name"])

    with open("{}_dupes.json".format(str(id)), "w") as f:
        f.write(json.dumps(dupes))
    f.close()


# getInventory(76561198261714500)

# findDupes(76561198261714500)
