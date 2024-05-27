import statics
import time
import urllib.request

from image_processor import ImageProcessor


image_processor = ImageProcessor()


# To ensure that there is no time problem when first starting the bot.
# Like starting the Bot at 15:59 when it is supposed to post at 16:00
def preload_image():
    image_processor.fetch_and_process()
    while not "url" in image_processor.id or image_processor.id["url"] == None:
        image_processor.id = image_processor.mastodon.media(image_processor.id)
        time.sleep(1.0)


def toot():
    image_processor.update_media()
    text = image_processor.title + " (by u/{})".format(image_processor.author)
    if image_processor.alt_text_type != 'manual':
        text += f'(\n{image_processor.alt_text_type} Alt-Text)'
    image_processor.mastodon.status_post(
        text, media_ids=image_processor.id)
    print("Toot!")
    image_processor.fetch_and_process()
