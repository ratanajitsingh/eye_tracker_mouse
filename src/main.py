import cv2
import mediapipe as mp
import pyautogui
import numpy as np

def main():

    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
    screen_w, screen_h = pyautogui.size()

    padding = 215
    pyautogui.FAILSAFE = False

    if not cam.isOpened():
        print("cam not open")
        return

    print("sys ready, q to quit")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.flip(frame,1)
        frame_h, frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks

        #created an active box so that the movement is smooth
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
                if id == 473:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)

                    #mapping camera coords to screen coords with padding for smoothness
                    screen_x = np.interp(x, (padding, frame_w - padding), (0,screen_w))
                    screen_y = np.interp(y, (padding, frame_h - padding), (0, screen_h))
                    pyautogui.moveTo(screen_x, screen_y)


        cv2.imshow('eye controlled mouse', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



