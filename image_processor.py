import cv2
import enchant
import fetcher
import json
import statics
import urllib.request
import pytesseract

from urllib.error import HTTPError
from mastodon import Mastodon
from ocr import GenerateAltText
from os.path import exists
from os import remove


class ImageProcessor:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ImageProcessor, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self):
        if (self.__initialized):
            return
        self.__initialized = True
        self._id = {}
        self.title = ''
        self.author = ''
        self.desc = ''
        self.alt_text_type = ''
        self.mastodon = Mastodon(
            access_token=statics.access_token,
            api_base_url=statics.api_base_url
        )
        self.set_instance_values()
        self.generator = GenerateAltText()

    def set_instance_values(self):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'curl/8.11')]
        try:
            server_info_raw = opener.open(
                '{}/api/v2/instance'.format(statics.api_base_url))
        except HTTPError:
            server_info_raw = opener.open(
                '{}/api/v1/instance'.format(statics.api_base_url))

        server_info = json.loads(server_info_raw.read())[
            'configuration']['media_attachments']

        self.image_size_limit = int(server_info['image_size_limit'])
        self.image_matrix_limit = int(server_info['image_matrix_limit'])
        self.supported_mime_types = [
            x for x in server_info['supported_mime_types'] if 'image/' in x]
        print(self.supported_mime_types)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def update_media(self):
        self.id = self.mastodon.media(self.id)
        if exists('alt_text.txt'):
            with open('alt_text.txt', 'r') as f:
                alt_text = f.read()
                self.mastodon.media_update(self.id, description=alt_text)
                remove('alt_text.txt')
                self.alt_text_type = 'manual'

    def image_check(self, url: str) -> bool:
        req = urllib.request.Request(
            url, method='HEAD')

        headers = urllib.request.urlopen(req).headers
        if int(headers['Content-Length']) <= self.image_size_limit and headers['Content-Type'] in self.supported_mime_types:
            return True

        return False

    async def fetch_and_process(self):
        filename = 'image.png'
        meme = await fetcher.fetch()
        while not self.image_check(meme[1]):
            meme = await fetcher.fetch()
        urllib.request.urlretrieve(meme[1], filename)
        img = cv2.imread(filename)
        size = img.shape
        if size[0]*size[1] > self.image_matrix_limit:
            # TODO: In case the image matrix limit is smaller than the default these values are not correct
            img = cv2.resize(img, maxsize, interpolation=cv2.CV_INTER_AREA)
            img.imwrite(filename)
        self.title = meme[0]
        self.author = meme[2]
        alt_text = self.generator.get_alt_text(filename)
        if alt_text == None:
            print("Alt-Text: {}".format("No ALT-Text for this post"))
        else:
            self.desc = alt_text[0]
            self.alt_text_type = alt_text[1]
            print("Alt-Text: {}".format(self.desc))
        self._id = self.mastodon.media_post(filename, description=self.desc)
