from OCR_Engine import *

def testOnData(config, dir):
    import os.path
    import cv2

    similList=[]
    filesList = [name for name in os.listdir(dir+"input") if not(name.endswith(".txt"))]
    for fileName in filesList:
        in_image = cv2.imread(dir+"input/"+fileName)
        in_text = open(dir + "input/" + fileName[:-3] + "txt", "r").read()

        out_image = imagePostPro(in_image)
        out_text = itt_OCR(out_image, config)
        # out_text = ""

        cv2.imwrite(dir + "output/" + fileName, out_image)
        open(dir + "output/" + fileName[:-3]+"txt", "w", encoding="utf-8").write(out_text)

        similList.append((sen_simil_ratio(in_text, out_text), fileName[:-4]))

    similList.sort()
    text=""
    mean=0
    for s in similList:
        mean+=s[0]
        text+=s[1]+": "+str(s[0])+"\n"
    open(dir + "error.txt", "a").write(text)
    return round(mean / len(similList), 3)


def sen_simil_ratio(X,Y):
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    # tokenization
    X_set = word_tokenize(X)
    Y_set = word_tokenize(Y)
    if len(X_set)==0 or len(Y_set)==0: return 0

    # form a set containing keywords of both strings
    l1 = []; l2 = []
    rvector = Y_set+X_set
    for w in rvector:
        if w in X_set: l1.append(1)
        else: l1.append(0)

        if w in Y_set: l2.append(1)
        else: l2.append(0)

    # cosine formula
    c = 0
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    return round(cosine, 3)


def testPSM(dir):
    from traceback import format_exc
    open(dir + "error.txt", "w").write("")
    for j in [1, 2]:
        for i in [6, 11, 4, 1, 3, 12]:
            try:
                open(dir + "error.txt", "a").write("average: "+str(testOnData('--psm {} --oem {}'.format(i,j), dir)))
                open(dir + "error.txt", "a").write('\n{}, {}\n'.format(i, j))
                open(dir + "error.txt", "a").write("\n*******************\n")
            except Exception:
                print(format_exc())
                print(Exception)
                continue


def testBox(config, dir, fileName):
    import os.path
    import cv2

    for name in os.listdir(dir + "input"):
        if not(name.endswith(".txt")) and name.split(".")[0]==fileName:
            in_image = cv2.imread(dir+"input/"+name)
            break

    image = imagePostPro(in_image)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    h, w = image.shape
    boxes = pytesseract.image_to_boxes(image, lang='eng', config=config)
    for b in boxes.splitlines():
        b = b.split(' ')
        image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    cv2.imshow('image', image)
    cv2.waitKey(0)


def test(config, dir):
    open(dir + "error.txt", "w").write("")
    open(dir + "error.txt", "a").write("average: "+str(testOnData(config, dir)))

dir = "Test_DataBase/"
# testPSM(dir)
test('--psm 6 --oem 1', dir)
# testBox('--psm 6 --oem 1', dir, "1")