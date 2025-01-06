import asyncio
import signal
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fetcher import fetch, save_image_links, load_image_links
from mastodon import MastodonError
from tooter import toot, preload_image
from urllib.error import HTTPError
from webserver import webserver


async def _start_bot():
    load_image_links()
    await preload_image()
    print('Ready!')
    scheduler.add_job(
        toot,
        trigger=IntervalTrigger(hours=4)
    )
    scheduler.start()


async def _start_server():
    await webserver.run_server()


async def main():
    bot_task = asyncio.create_task(_start_bot())
    server_task = asyncio.create_task(_start_server())
    await asyncio.gather(bot_task, server_task)


def sigterm_handler(signal, frame):
    print('Stopped!')
    save_image_links()
    sys.exit(0)


scheduler = AsyncIOScheduler()

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGTERM, sigterm_handler)
        asyncio.run(main())
    except Exception as e:
        save_image_links()
        print(e)
        sys.exit(0)
    except KeyboardInterrupt:
        save_image_links()
        sys.exit(0)
