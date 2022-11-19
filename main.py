import asyncio
import aioschedule as schedule
import time

from fetcher import fetch
from tooter import toot

async def toot_some_wholesome_stuff():
    meme = await fetch()
    await toot(meme)
    print("Toot!")

schedule.every().hour.at(":00").do(toot_some_wholesome_stuff)

loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(schedule.run_pending())
    time.sleep(0.1)
