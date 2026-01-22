import cv2
import mediapipe as mp
import pyautogui

def main():

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Unable to open camera.")
        return

    print("system ready, q to quit")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.flip(frame,1)

        cv2.imshow('Eye controlled mouse', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()