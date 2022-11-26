from Cleanup.file import setup, cleanup
from Market.cards import *
from Market.market import *
from Login.login import *
import requests as r
import time

decision = input("Enter 'y' to login or 'n' to skip and enter your steam id: ")

decision = decision.lower()

if decision == 'y':
    username = input("Enter your Steam username: ")
    password = input("Enter your Steam password: ")
    jar = r.cookies.RequestsCookieJar()
    auth_ctx = login(jar, username, password)

    id = auth_ctx['steamid']

    # init session
    resp = r.get('https://steamcommunity.com/', cookies=jar)
    jar.update(resp.cookies)

    market_jar = transfer_login(jar, auth_ctx)
    if check_eligibility(market_jar):
        setup(id)
        getInventory(id)
        findDupes(id)
        try:
            multiSell(id)
        except Exception as e:
            print("Error selling cards: " + e)
            pass

else:
    id = input("Enter your Steam id: ")
    setup(id)
    getInventory(id)
    findDupes(id)
    try:
        multiSell(id)
    except Exception as e:
        print("Error selling cards: " + e)
        pass
    # sellAll(market_jar, auth_ctx, id) - borked, not sure why


# time.sleep(5)
# cleanup(id)
