import fetcher
import json
import statics
import urllib.request

from urllib.error import HTTPError
from mastodon import Mastodon
from PIL import Image


class ImageProcessor:
    def __init__(self):
        self._id = {}
        self.title = ""
        self.mastodon = Mastodon(
            access_token=statics.access_token,
            api_base_url=statics.api_base_url
        )
        self.set_instance_values()

    def set_instance_values(self):
        try:
            server_info_raw = urllib.request.urlopen(
                "{}/api/v2/instance".format(statics.api_base_url))
        except HTTPError:
            server_info_raw = urllib.request.urlopen(
                "{}/api/v1/instance".format(statics.api_base_url))

        server_info = json.loads(server_info_raw.read())[
            "configuration"]["media_attachments"]

        self.image_size_limit = int(server_info["image_size_limit"])
        self.image_matrix_limit = int(server_info["image_matrix_limit"])
        self.supported_mime_types = [x for x in server_info["supported_mime_types"] if "image/" in x]
        print(self.supported_mime_types)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def image_check(self, url: str) -> bool:
        req = urllib.request.Request(
            url, method='HEAD')

        headers = urllib.request.urlopen(req).headers
        if int(headers['Content-Length']) <= self.image_size_limit and headers['Content-Type'] in self.supported_mime_types:
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
            if img.size[0]*img.size[1] > self.image_matrix_limit:
                img.thumbnail((4096, 4096)) # TODO: In case the image matrix limit is smaller than the default these values are not correct
                img.save(filename)
        self.title = meme[0]
        self._id = self.mastodon.media_post(filename)
