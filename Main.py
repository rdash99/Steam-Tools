from Cleanup.file import setup, cleanup
from Market.cards import *
import time

setup(76561198261714500)
getInventory(76561198261714500)
findDupes(76561198261714500)
time.sleep(5)
cleanup(76561198261714500)
