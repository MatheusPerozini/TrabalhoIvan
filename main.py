import cv2
from cvzone.HandTrackingMouse import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    cv2.rectangle(img, (100, 100), (300, 300), (255,0,255), cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)