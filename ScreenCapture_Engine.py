from ctypes import windll, Structure, c_long, byref
import keyboard
import pyautogui


def queryMousePosition():
    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x,pt.y


def detectKeypress(keyID):
    keypressed=" "
    while keypressed!=keyID:
        keypressed=keyboard.read_event().scan_code
        keyboard.read_event()
    print("point selected")


def getPosOnKeypress():
    detectKeypress(70)
    return queryMousePosition()


def getBoxRange():
    left, top = getPosOnKeypress()
    width, height = getPosOnKeypress()
    width, height = width-left, height-top
    if width<0:
        left = width+left
        width = -width
    if height<0:
        top = height+top
        height = -height
    return left, top, width, height


def rangeScreenshot(range):
    from numpy import array

    # left, top, width, height
    image=pyautogui.screenshot(region=range)
    image.save("imageTaken.png")
    return array(image)


# ***************************
def test():
    box=getBoxRange()
    print(box)
    rangeScreenshot(box)

# test()