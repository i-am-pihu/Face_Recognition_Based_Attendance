import cv2
#cap = cv2.VideoCapture('http://192.168.0.6:4747/vedio')
cap=0
cap = cv2.VideoCapture('http://192.168.0.5:4747/mjpegfeed')
print("yee")
i=0
while(i<50):
    ret,frame=cap.read()
    print(ret)
    i+=1
