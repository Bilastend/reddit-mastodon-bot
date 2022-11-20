import statics
import time
import urllib.request

from image_processor import ImageProcessor


image_processor = ImageProcessor()
image_processor.fetch_and_process()
# To ensure that there is no time problem when first starting the bot.
# Like starting the Bot at 15:59 when it is supposed to post at 16:00
while not "url" in image_processor.id or image_processor.id["url"] == None:
    image_processor.id = image_processor.mastodon.media(image_processor.id)
    time.sleep(1.0)


def toot():
    image_processor.id = image_processor.mastodon.media(image_processor.id)
    image_processor.mastodon.status_post(
        image_processor.title, media_ids=image_processor.id)
    image_processor.fetch_and_process()
