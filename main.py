import asyncio
import schedule
import signal
import sys
import time

from mastodon import MastodonError
from urllib.error import HTTPError
from fetcher import fetch, save_image_links, load_image_links
from tooter import toot, preload_image

from webserver import webserver


async def _start_bot():
    load_image_links()
    await preload_image()
    schedule.every(4).hours.at(":00").do(toot)
    print('Ready!')
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


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
