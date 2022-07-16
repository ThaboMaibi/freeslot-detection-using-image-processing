import cv2 as cv
import sys
import pickle




width, height = 65, 85
try:
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


#
def mouseClick(events,x,y,flags,params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1 , y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('carParkPos', 'wb') as f:
        pickle.dump(posList,f)

while True:
    # cv.rectangle(img, (30, 200), (100, 150), (255, 0, 255), 2)
    img = cv.imread("test.png")
    for pos in posList:
        cv.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)

    cv.imshow("Image", img)
    cv.setMouseCallback("Image", mouseClick)
    cv.waitKey(1)