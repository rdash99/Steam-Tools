import requests as r
import json
import time

URL_CHECK_ELIGIBILITY = 'https://steamcommunity.com/market/eligibilitycheck/'


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


def sellItem(jar, item, auth_ctx, price):
    url = "http://steamcommunity.com/market/sellitem/"
    parameters = {"sessionid": jar["sessionid"], "appid": str(item["appid"]), "contextid": item["contextid"], "assetid": item["assetid"],
                  "amount": '1', "price": str(price)}
    headers = {
        "Referer": "https://steamcommunity.com/profiles/{}/inventory/".format(auth_ctx["steamid"])}
    data = r.post(url, params=parameters, cookies=jar, headers=headers)
    response = data.json()
    print(parameters)
    print(response)
    assert data.status_code == 200
    return response


def check_eligibility(jar):
    resp = r.get(URL_CHECK_ELIGIBILITY,
                 cookies=jar, allow_redirects=False)

    return resp.status_code == 302


def sellAll(jar, auth_ctx, id):
    with open("{}/{}_sellabledupes.json".format(str(id), str(id)), "r") as f:
        items = json.loads(f.read())
    f.close()

    for item in items:
        price = getItemValue(item["appid"], item["market_hash_name"])
        sellItem(jar, item, auth_ctx, price)
        print("Sold {} for {}".format(item["name"], price))
        time.sleep(3)
        break
        
#move function to cards
def formatItem(item):
    data = {'quantity': 1, "market_hash_name": item["market_hash_name"]}
    return data
    
def multiSell(id):
    with open("{}/{}_sellabledupes.json".format(str(id), str(id)), "r") as f:
        items = json.loads(f.read())
    f.close()
    baseUrl = "http://steamcommunity.com/market/multisell?appid=753&contextid=6"
    
    splitItems = split(items, 20)

    urls = []
    
    sortedItems = []
    
    for item in splitItems:
        listData = []
        index = 0
        for i in item:
            #check if item is in list already and if so, add to quantity instead of adding new item
            try:
                if i["market_hash_name"] in listData[index]:
                    listData[i["market_hash_name"]]["quantity"] += 1
                else:
                    listData.append(formatItem(i))
            except:
                listData.append(formatItem(i))
        sortedItems.append(listData)
        print(listData)
        index+=1
        
        
    for item in sortedItems:
        url = baseUrl
        for i in item:
            url += ("&items[]={}&qty[]={}".format(i["market_hash_name"].replace(' ', "%20"), i["quantity"]))
        urls.append(url)
    with open("{}/{}_sellableurl.txt".format(str(id), str(id)), "w") as f:
        for url in urls:
            f.write(url + "\n")
    f.close()
    
def split(items, size):
    return [items[i:i+size] for i in range(0, len(items), size)]
