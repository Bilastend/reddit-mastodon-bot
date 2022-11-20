import fetcher
import statics
import urllib.request

from mastodon import Mastodon


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

    def fetch_and_process(self):
        meme = fetcher.fetch()
        filename = "wholesomeness.png"
        img_url = meme[1]
        urllib.request.urlretrieve(img_url, filename)
        self.title = meme[0]
        self._id = self.mastodon.media_post(filename)
