import cv2


img = cv2.line(img, (310, 240), (330, 240), (255, 255, 0), 2)
img = cv2.line(img, (340, 240), (360, 240), (255, 255, 0), 2)
cv2.imshow("MyTello", img)