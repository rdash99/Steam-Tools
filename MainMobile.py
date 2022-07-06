from Cleanup.file import setup, cleanup
from Market.cards import *
from Market.market import *
#from Login.login import *
import requests as r
import time

id = input("Enter your Steam id: ")

cleanup(id)
setup(id)
getInventory(id)
findDupes(id)
# sellAll(market_jar, auth_ctx, id) - borked, not sure why
#time.sleep(5)
# cleanup(id)
