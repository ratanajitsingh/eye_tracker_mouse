# Eye controlled Mouse
A hands free cursor controller that tracks eye movements and blink gestures using Python, OpenCV and MediaPipe.

## Description
This project uses computer vision to map facial landmarks to screen coordinates, allowing users to control the mouse cursor purely through their head/eye movements and gestures. There is a custom **Calibration Mode** which allows users to adjust the active tracking area to their specific set up and **Smoothing** for reduction of jitter.

## Features 
* **Real-Time Eye Tracking:** Maps the iris position to screen coordinates 
* **Interactive Calibration:** Adjustable Active Area to fit the users range of motion 
* **Blink clicking:** Whenever the left eye blinks a mouse click is registered 
* **Smooth cursor:** Using smoothing through math to reduce camera and mouse jitter

## Tech Stack
* **Python 3.x**
* **OpenCV:** Video capture and frame processing
* **MediaPipe:** Face mesh and iris tracking
* **PyAutoGUI:** Cross-platform mouse control 
* **NumPy**: Coordinate interpolation and vector math

## Installation 
1. **Clone repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/eye-tracker-mouse.git](https://github.com/YOUR_USERNAME/eye-tracker-mouse.git)
    cd eye-tracker-mouse
    ```
2. **Create a virtual environment :**
    made using virtual environment, not necessary but highly recommended
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
   
## Usage 
1. **Run script on terminal:**
    ```bash
    python src/main.py
    ```
2. **Phase 1: Calibration mode**
    * Indicated through **RED** box 
    * **Press 'W':** This will shrink the box making it easier to reach corners and not hurt your neck 
    * **Press 'S':** This will grow the box, making it easier to be precise but harder to reach each part 
    * **Press 'Enter':** Confirm settings and start the mouse functionality
3. **Phase 2: Active control**
    * Indicated through **BLUE** box
    * **Move Cursor:** Move your head/eyes, to control mouse following your gaze on the screen 
    * **CLICK:** Blink your **LEFT** eye to initiate a click
    * **Quit:** Press 'Esc' or 'q' to exit

## Config 
The exact variables can also be changed in the config area on the top of the 'src/main.py' 

## Troubleshooting 
* **Lighting:** Ensure your face is well-lit. Shadows can decrease accuracy 
* **Camera Index:** if camera doesn't open, change the cv2.VideoCapture(0) to cv2.VideoCapture(1) in main.py
* **Permissions:** On macOS, there may be some permissions that need to be allowed 

## License
Open source and available under the MIT license 

## Screenshots