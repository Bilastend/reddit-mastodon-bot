import pytesseract
import enchant
import cv2

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
        words = [x.strip() for x in description_temp.split(" ") if len(x) > 0 and not "@" in x]

        for word in words:
            if self.dictionary.check(self.get_clean_word(word)):
                identified_words += 1
        percentage = identified_words/len(words) if len(words) != 0 else 0

        return (description,percentage)

    def get_best_image(self, img):
        d = {}
        types = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV, cv2.THRESH_TRUNC]

        for thresh_type in types:
            _, tmp = cv2.threshold(img, 200, 255, thresh_type)
            d[thresh_type] = self.check_description(pytesseract.image_to_string(tmp,lang='eng').replace("|","I"))

        return max(d.values(), key=lambda sub: sub[1])

    def get_alt_text(self, image):
        im = cv2.imread(image)

        descriptions = (self.check_description(pytesseract.image_to_string(im,lang='eng').replace("|","I")),
                                    self.get_best_image(im))

        best_desc, percentage = max(descriptions, key=lambda desc: desc[1])

        while best_desc.endswith("\n"):
            best_desc = best_desc[:-1]

        return best_desc if percentage >= 0.89 else None




