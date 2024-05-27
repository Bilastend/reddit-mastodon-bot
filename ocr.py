import base64
import cv2
import enchant
import pytesseract
import statics
import requests


class GenerateAltText:

    def __init__(self):
        self.dictionary = enchant.Dict("en_US")

    def get_clean_word(self, word):
        clean_word = word.strip()
        clean_word = ''.join([x for x in clean_word if x.isalpha()])
        return clean_word if len(clean_word) > 0 else "-"

    def check_description(self, description):
        identified_words = 0
        description_temp = description.replace("\n", " ")
        words = [x.strip() for x in description_temp.split(" ")
                 if len(x) > 0 and not "@" in x]

        for word in words:
            if self.dictionary.check(self.get_clean_word(word)):
                identified_words += 1
        percentage = identified_words/len(words) if len(words) != 0 else 0

        return (description, percentage)

    def get_best_image(self, img):
        d = {}
        types = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV,
                 cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV, cv2.THRESH_TRUNC]

        for thresh_type in types:
            _, tmp = cv2.threshold(img, 200, 255, thresh_type)
            d[thresh_type] = self.check_description(
                pytesseract.image_to_string(tmp, lang='eng').replace("|", "I"))

        return max(d.values(), key=lambda sub: sub[1])

    def get_alt_text(self, image):

        if hasattr(statics, 'open_ai_key'):
            ai_alt_text = self.get_alt_text_ai(image)

            if ai_alt_text.status_code == 200:
                print("AI-ALT")
                return (ai_alt_text.json().get('choices')[0].get('message').get('content'), 'AI')

        print("OCR-ALT")
        return self.get_alt_text_ocr(image)

    def get_alt_text_ocr(self, image):
        im = cv2.imread(image)

        descriptions = (self.check_description(pytesseract.image_to_string(im, lang='eng').replace("|", "I")),
                        self.get_best_image(im))

        best_desc, percentage = max(descriptions, key=lambda desc: desc[1])

        while best_desc.endswith("\n"):
            best_desc = best_desc[:-1]

        return (best_desc, 'OCR') if percentage >= 0.89 else None

    def get_alt_text_ai(self, image):

        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(image)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {statics.open_ai_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                # TODO: Change prompt to make the description feel & read less like an AI Text
                # s/o to https://heydingus.net/shortcuts/generate-alt-text-with-openai-vision for the prompt
                            "text": """
                Please provide a functional, objective description of the provided
                image in no more than 1500 characters
                so that someone who is visually impaired would be able to imagine it. Don't
                include a conclusion or a summary. You should not begin the description with any variation of 'The image'.
                If there is text found in the image, it is very important that you transcribe all of it. In case of an
                social media post dont describe profile pictures"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return response
