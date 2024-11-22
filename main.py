import cv2
from cvzone.HandTrackingMouse import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255,0,255)

while True:
    sucess, img = cap.read()
    # Se for necessario inverter a imagem
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:
        cursor = lmList[8]
        if 100 < cursor[0] < 300 and 100 < cursor[1]:
            colorR = (0, 255, 0)
        else:
            colorR = (255, 0, 255)

    cv2.rectangle(img, (100, 100), (300, 300), colorR, cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)