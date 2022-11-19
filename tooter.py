import asyncio
import statics
import time
import urllib.request

from mastodon import Mastodon

mastodon = Mastodon(
    access_token = statics.access_token,
    api_base_url = "https://botsin.space/"
)

async def toot(data: tuple):
    filename = "wholesomeness.png"
    img_url = data[1]
    urllib.request.urlretrieve(img_url, filename)
    meme = mastodon.media_post(filename)
    await asyncio.sleep(5)
    mastodon.status_post(data[0], media_ids=meme)