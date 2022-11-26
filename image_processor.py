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

    def file_size_check(self, url: str) -> bool:
        req = urllib.request.Request(
            url, method='HEAD')
        return int(urllib.request.urlopen(req).headers['Content-Length']) <= 10000000

    def fetch_and_process(self):
        filename = "image.png"
        meme = fetcher.fetch()
        while not self.file_size_check(meme[1]):
            meme = fetcher.fetch()
        urllib.request.urlretrieve(meme[1], filename)
        with Image.open(filename) as img:
            size = img.size
            if img.size[0]*img.size[1] > 16777216:
                img.thumbnail((4096,4096))
                img.save(filename)
        self.title = meme[0]
        self._id = self.mastodon.media_post(filename)
