import schedule
import signal
import sys
import time

from mastodon import MastodonError
from urllib.error import HTTPError
from fetcher import fetch, save_image_links, load_image_links
from tooter import toot, preload_image


def main():
    load_image_links()
    preload_image()
    schedule.every(4).hours.at(":00").do(toot)
    print('Ready!')
    while True:
        schedule.run_pending()
        time.sleep(1)

def sigterm_handler(signal, frame):
    print('Stopped!')
    save_image_links()
    sys.exit(0)



if __name__ == '__main__':
    try:
        signal.signal(signal.SIGTERM, sigterm_handler)
        main()
    except Exception as e:
        save_image_links()
        print(e)
        sys.exit(0)
    except KeyboardInterrupt:
        save_image_links()
        sys.exit(0)
