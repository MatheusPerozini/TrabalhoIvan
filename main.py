import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (100,0,255)

cx, cy, w, h = 100, 100, 200, 200

class DragRect():
    def __init__(self, posCenter, size=[150,150]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
               self.posCenter = cursor

rectList = []
for x in range(3):
    rectList.append(DragRect([x*200+100, 150]))

while True:
    sucess, img = cap.read()
    # Se for necessario inverter a imagem
    img = cv2.flip(img, 1)
    
    hands, img = detector.findHands(img)
    
    if hands:
        hand = hands[0] 
        lmList = hand['lmList'] 
        
        if lmList:
            x1, y1 = lmList[4][0], lmList[4][1]  # Coordenadas do polegar
            x2, y2 = lmList[8][0], lmList[8][1]  # Coordenadas do dedo indicador
            l, _, _ = detector.findDistance((x1, y1), (x2, y2))  # Distancia entre os dois pontos
            if l < 40:
                cursorX, cursorY, _ = lmList[8]
                cursor = [cursorX, cursorY]
                print(cursor)
                for rect in rectList:
                    rect.update(cursor)
    
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    
    cv2.imshow("Image", out)
    cv2.waitKey(1)