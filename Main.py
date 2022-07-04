from Cleanup.file import setup, cleanup
from Market.cards import *
from Market.market import *
from Login.login import *
import requests as r
import time

username = input("Enter your Steam username: ")
password = input("Enter your Steam password: ")
jar = r.cookies.RequestsCookieJar()

auth_ctx = login(jar, username, password)
print(auth_ctx)

id = auth_ctx['steamid']

# init session
resp = r.get('https://steamcommunity.com/', cookies=jar)
jar.update(resp.cookies)

market_jar = transfer_login(jar, auth_ctx)

setup(id)
getInventory(id)
findDupes(id)
time.sleep(5)
cleanup(id)
