import keyboard
from ScreenCapture_Engine import rangeScreenshot, getBoxRange
from OCR_Engine import itt_OCR, imagePostPro
from TTS_Engine import playGTTS


def main():
    prev = False
    while True:
        print("\n\n\n\n\n\n")

        keypressed = "select point"
        while keypressed != 70:
            keypressed = keyboard.read_event().scan_code
            keyboard.read_event()
            if keypressed==71:
                prev=not(prev)
                print("save range set to "+ str(prev))

        if prev:
            print("old range")
        else:
            print("new session")
            box=getBoxRange()

        text=itt_OCR(imagePostPro(rangeScreenshot(box)))

        try: playGTTS(text)
        except AssertionError: pass


if __name__ == '__main__':
    main()