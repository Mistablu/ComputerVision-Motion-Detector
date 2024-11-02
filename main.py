import cv2
import time
from sendemail import send_email
from datetime import datetime

video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
status_list = []
count = 1

while True:
    now = datetime.now()
    status = 0
    check, frame = video.read()
    cv2.imwrite(f"images/{count}.png",frame)
    count = count+1
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21),0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email()

    #Display date and timestamp on video
    cv2.putText(img=frame,text=now.strftime("%A"),org=(20,30),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                color=(255,255,255),thickness=2,lineType=cv2.LINE_AA)
     
    cv2.putText(img=frame,text=now.strftime("%H:%M:%S"),org=(20,60),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)


    cv2.imshow("My video",frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
