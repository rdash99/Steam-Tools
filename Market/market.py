import requests as r
import json

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


def sellItem(jar, itemInfo, sessionid, price):
    url = "http://steamcommunity.com/market/sellitem/"
    params = {"appid": itemInfo["appid"], "assetid": itemInfo["assetid"],
              "contextid": itemInfo["contextid"], "amount": "1", "sessionid": sessionid, "price": price}
    headers = {"Referer": "https://steamcommunity.com/id/zugglybug/inventory/",
               "DNT": "1", "Origin": "https://steamcommunity.com"}
    data = r.post(url, params=params, cookies=jar, headers=headers)
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


def check_eligibility(jar):
    resp = requests.get(URL_CHECK_ELIGIBILITY,
                        cookies=jar, allow_redirects=False)
    jar.update(resp.cookies)

    return resp.status_code == 302


getItemValue("753", "998740-Mimic")
