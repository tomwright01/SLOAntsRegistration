import cv2
import numpy as np

def main(fname,grayscale):
    """Extracts the frames from an AVI file and returns an np.array"""
    cap = cv2.VideoCapture(fname)
    ret = True
    imgs = np.zeros((cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT),
                    cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH),
                    cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)),np.uint8)
    iFrame = 0
    while True:
        ret,img=cap.read()
        if not ret:
            break
        imgs[:,:,iFrame]=img[:,:,0]
        iFrame += 1
            
    cap.release
    return(imgs)