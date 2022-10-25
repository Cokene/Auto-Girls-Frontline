from autoLSupport import *


def isLSupport():
    initImage = cv2.imread(IMAGE_PATH+"L_support.png")
    capImage  = getImage(L_SUPPORT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    cv2.imwrite('test.png',capImage)
    return imageCompare(initImage,capImage)
isLSupport()
