import schedule
import time

from fetcher import fetch
from tooter import toot


def toot_some_wholesome_stuff():
    toot()
    print("Toot!")


schedule.every().hour.at(":00").do(toot_some_wholesome_stuff)

while True:
    schedule.run_pending()
    time.sleep(1)
