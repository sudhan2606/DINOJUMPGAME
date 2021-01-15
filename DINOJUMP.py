import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import cv2

if __name__ == '__main__':
    seq = 0
    cap = cv2.VideoCapture(0)  # opens camera, parameter is source of camera, 0 is the default camera.
    # video quality (resolution)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # capturing speed in fps
    frameps = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print("width = ", width)
    print("Height = ", height)
    print("Frame count = ", frameps)
    counter = 0
    while (True):

        # Capture frame-by-frame, cap.read() returns a tuple, frame stores the frame by frame and ret stores T/F values depending on the camera.
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # inverted the frame to get the correct image
        flip = cv2.flip(frame, 1)
        # Display the resulting frame
        # Defining np array range for human skin
        min_YCrCb = np.array([0, 133, 77], np.uint8)
        max_YCrCb = np.array([235, 173, 127], np.uint8)
        # setting region of interest
        roi = flip[150:350, 150:350]
        # Get pointer to video frames from primary device
        # changing image to YCrCb colour
        imageYCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)
        skinRegionYCrCb = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)
        # bitwise image operation to detect skin colour
        skinYCrCb = cv2.bitwise_and(roi, roi, mask=skinRegionYCrCb)
        # printing text
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(flip, text='Running...', org=(150, 150), fontFace=font, fontScale=3, color=(255, 255, 255), thickness=5)
        # drawing rectangle in our region of interest
        cv2.rectangle(flip, pt1=(150, 150), pt2=(350, 350), color=(255, 255, 0), thickness=5)

        skinYCrCb = cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY)
        # thresholding image, reducing b&w image into 2 channel from 3 as contours work for binary image
        (thresh, skinYCrCb) = cv2.threshold(skinYCrCb, 127, 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(skinYCrCb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(type(contours))
        #print((contours))

        for x in contours:
            area = cv2.contourArea(x)
            #print(area)
            cv2.drawContours(skinYCrCb, contours, -1, (0, 255, 0), 3)
            if area>10000:
                counter = 1
                break

        if counter==1 and area<10000:
            counter = 0
            seq += 1
            print("JUMP",seq)
            pyautogui.press('space')
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(flip, text='JUMP', org=(150, 150), fontFace=font, fontScale=3, color=(255, 255, 255),
                        thickness=5)

        # showing the captured video
        cv2.imshow('frame', flip)

        # showing the region of  interest
        cv2.imshow('frame2', skinYCrCb)
        # plt.imshow(skinYCrCb)
        # plt.show()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
