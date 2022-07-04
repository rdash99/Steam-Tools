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
    parameters = {"sessionid": jar["sessionid"], "appid": item["appid"], "contextid": item["contextid"], "assetid": item["assetid"],
                  "amount": 1, "price": price}
    headers = {"Referer": "https://steamcommunity.com/id/zugglybug/inventory/",
               "DNT": "1"}
    data = r.post(url, params=parameters, cookies=jar, headers=headers)
    response = data.json()
    print(response)
    assert data.status_code == 200
    return response


def check_eligibility(jar):
    resp = r.get(URL_CHECK_ELIGIBILITY,
                 cookies=jar, allow_redirects=False)
    jar.update(resp.cookies)

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
