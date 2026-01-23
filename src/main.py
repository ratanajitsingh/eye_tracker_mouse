import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

def main():

    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
    screen_w, screen_h = pyautogui.size()


    # Initialisation of variables

    #box dimensions - adjust depending on the user and use case
    padding = 215
    #smoothing variable, lower it is the fast the mouse is but the more jittery its movements. Higher, slower but smoother movements
    smoothing = 3
    #sensitivity for blink to click - lower if its clicking when eyes are open, increase if it doesn't click even when you blink
    blinky = 0.004
    #storing locations for smoothness prev location x,y and current location x,y
    prevl_x, prevl_y = 0,0
    curl_x, curl_y = 0,0
    #Start in set up mode
    calibrate = True
    #Visual aid for clicking
    last_click_time = 0

    #removes quitting when hitting edge of screen
    pyautogui.FAILSAFE = False

    if not cam.isOpened():
        print("cam not open")
        return

    print("sys ready, q to quit")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        #flipping camera
        frame = cv2.flip(frame,1)
        frame_h, frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks

        if calibrate:
            #setup mode
            cv2.putText(frame, F"Setup: Padding {padding}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.putText(frame, "Press 'W' to make box smaller", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 1)
            cv2.putText(frame, "Press 'S' to make box bigger", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 1)
            cv2.putText(frame, "Press 'Enter' to Start", (10,110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            #red rectangle means its in set up phase
            cv2.rectangle(frame, (padding,padding), (frame_w -padding, frame_h- padding), (0,0,255), 2)
        else:
            #active mode
            cv2.putText(frame, "Active mode (esc to Quit)", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            #box made in blue when in active phase
            cv2.rectangle(frame, (padding, padding), (frame_w - padding, frame_h - padding), (255, 0, 0), 2)


        if landmark_points:
            landmarks = landmark_points[0].landmark


            for id, landmark in enumerate(landmarks):

                #474-478 left iris, 469-473 right iris
                if id in range(474, 478) or id in range(469, 473):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)

                    cv2.circle(frame, (x,y), 3, (0,255,255), -1)

                #eyelid detection
                if id in [145, 159]:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x,y), 3, (0,255,0), -1)

                #mouse control logic
                if id == 473 and not calibrate:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)

                    #mapping camera coords to screen coords with padding for smoothness
                    target_x = np.interp(x, (padding, frame_w - padding), (0,screen_w))
                    target_y = np.interp(y, (padding, frame_h - padding), (0, screen_h))

                    #smoothing: current pos = previous + ( target - prev) / smoothing factor
                    curl_x = prevl_x + (target_x - prevl_x) / smoothing
                    curl_y = prevl_y + (target_y - prevl_y) / smoothing

                    pyautogui.moveTo(curl_x, curl_y)

                    prevl_x, prevl_y = curl_x, curl_y

            if not calibrate:
                left_eye_top = landmarks[159]
                left_eye_bottom = landmarks[145]

                if (left_eye_bottom.y - left_eye_top.y) < blinky:
                    pyautogui.click()
                    print("click")
                    #sleeps after the click to prevent double-clicking since the loop is fast
                    time.sleep(0.5)


        if time.time() - last_click_time < 1.0:
            cv2.putText(frame, "click", (frame_w // 2 - 50, frame_h // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)

        cv2.imshow('eye controlled mouse', frame)

        key = cv2.waitKey(1) & 0xFF

        #quitting logic
        if key == ord("q") or key == 27:
            break

        if calibrate:
            if key == ord("w"):
                padding +=5
            elif key ==ord("s"):
                padding = max(0, padding - 5)
            elif key == 13:
                calibrate = False




    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



