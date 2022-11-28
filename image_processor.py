import fetcher
import statics
import urllib.request

from mastodon import Mastodon
from PIL import Image


class ImageProcessor:
    def __init__(self):
        self._id = {}
        self.title = ""
        self.mastodon = Mastodon(
            access_token=statics.access_token,
            api_base_url="https://botsin.space/"
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def image_check(self, url: str) -> bool:
        valid_mime_type = ["image/jpeg", "image/png", "image/gif",
                           "image/heic", "image/heif", "image/webp", "image/avif", ]
        req = urllib.request.Request(
            url, method='HEAD')

        headers = urllib.request.urlopen(req).headers
        if int(headers['Content-Length']) <= 10485760 and headers['Content-Type'] in valid_mime_type:
            return True

        return False

    def fetch_and_process(self):
        filename = "image.png"
        meme = fetcher.fetch()
        while not self.image_check(meme[1]):
            meme = fetcher.fetch()
        urllib.request.urlretrieve(meme[1], filename)
        with Image.open(filename) as img:
            size = img.size
            if img.size[0]*img.size[1] > 16777216:
                img.thumbnail((4096, 4096))
                img.save(filename)
        self.title = meme[0]
        self._id = self.mastodon.media_post(filename)
