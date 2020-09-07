import pytesseract
from autocorrect import Speller
import cv2


def imagePostPro(image):
    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(image):
        return cv2.GaussianBlur(image, (3,5), 1.5)

    # thresholding
    def thresholding(image, w):
        if w: w=cv2.THRESH_BINARY
        else: w=cv2.THRESH_BINARY_INV

        return cv2.threshold(image, 0, 255, w + cv2.THRESH_OTSU)[1]
        # return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, w, 21, 3)

    # check if text has white background
    def whiteBackgroundCheck(image):
        img=cv2.resize(image, (300, 300))
        black=0; white=0
        for collomn in img:
            for c in collomn:
                if c<120:  black+=1
                else: white+=1
        if white>=black: return True
        return False

    def add_margin(image):
        margin = 30 # int(0.05 * pow(image.shape[0]*image.shape[1], 0.5))
        return cv2.copyMakeBorder(image.copy(),margin,margin,margin,margin,cv2.BORDER_CONSTANT,value=(0,0,0))

    def resize(image):
        c=1500/image.shape[1]
        return cv2.resize(image, (int(image.shape[1]*c), int(image.shape[0]*c)))

    image = resize(image)
    image = get_grayscale(image)
    image = thresholding(image, whiteBackgroundCheck(image))
    image = remove_noise(image)
    image = add_margin(image)

    cv2.imwrite("imagePost.png", image)
    return image


def itt_OCR(image, config='--psm 4 --oem 1'): # oem 1, 2 -- psm 6, 11, 4, 1, 3, 12
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(image, lang='eng', config=config)
    spell = Speller()
    text = spell(text)

    print("text is: \n"+text)
    return text


# ***************************
def test():
    image = cv2.imread("imageTaken.jpg")
    image = imagePostPro(image)
    cv2.imwrite("imagePost.png", image)
    itt_OCR(cv2.imread("imagePost.png"))


# test()

