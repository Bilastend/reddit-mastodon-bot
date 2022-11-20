import schedule
import sys
import time

from fetcher import fetch, save_image_links, load_image_links
from tooter import toot, preload_image


def toot_some_wholesome_stuff():
    toot()
    print("Toot!")


def main():
    load_image_links()
    preload_image()
    schedule.every().hour.at(":00").do(toot_some_wholesome_stuff)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    try:
        print('Servus.')
        main()
    except KeyboardInterrupt:
        save_image_links()
        sys.exit(0)
