import cv2 as cv
import sys
import pickle
import cvzone
import numpy as np
# import firebase
import firebase_admin
from firebase_admin import credentials,storage,firestore
#
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred,{'storageBucket':'smartparking-25f7b.appspot.com'})
db = firestore.client()

# add data
doc_ref = db.collection(u'parkinglots').document(u'ZPY4tgVIVPs7KKdGBcpz')
# doc_ref.set({
#     u'freesSlots': 10,
#     u'totalSlots': 30,
# })
# read data
# users_ref = db.collection(u'parking')
# docs = users_ref.stream()
#
# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')

# bucket = storage.bucket()
# blob = bucket.get_blob('DSC_9014.jpg')
# arr = np.frombuffer(blob.download_as_string(),np.uint8)
# firebaseImg = cv.imdecode(arr,cv.COLOR_BGR2GRAY)
# cv.imshow('firebaseImage', firebaseImg)
#
# cv.waitKey(0)



# Video feed
cap = cv.VideoCapture('lot.mkv')
with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)
width, height = 60, 85

def checkParkingSpace(imgpro):
    spaceCount = 0
    for pos in posList:
        x,y = pos
        imgCrop = imgpro[y:y+height, x:x+width]
        cv.imshow("cropped", imgCrop)
        count = cv.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1, thickness=2, offset=0)
        if count < 500:
            color =(0,255,0)
            thickness = 5
            spaceCount+=1
        else:
            color =(0,0,255)
            thickness = 2
        cv.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)
    cvzone.putTextRect(img, str(spaceCount), (100, 50), scale=3, thickness=5, offset=20,colorR=(0,255,0))
    doc_ref.set({
        u'freeSlots': spaceCount,
        u'location': 'lesotho maseru roma',
        u'name': 'NUL Parking',
        u'totalSlots': 14,
    })
while True:
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv.adaptiveThreshold(imgBlur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,25,16)
    # removing the dots to make the image clearer
    imgMedian = cv.medianBlur(imgThreshold,5)
    # making picksils thicker to make it easier to differntiate between empty space
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpace(imgDilate)

    cv.imshow("Image",img)
    # cv.imshow("Image Blurred", imgBlur)
    # cv.imshow("Image Gray",imgGray)
    # cv.imshow("Image Dilated", imgDilate)
    cv.waitKey(10)
