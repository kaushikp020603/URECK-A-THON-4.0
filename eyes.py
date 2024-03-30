import cv2
import streamlit as st
import time

# Load the pre-trained face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to detect eyes
def detect_eyes(gray, frame):
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    return len(eyes)

def main():
    st.title("Live Eye Detector")
    stop = st.button("Stop")

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Cannot access camera")
        return

    # Variable to track time when eyes are closed
    last_closed_time = None

    while cap.isOpened() and not stop:
        ret, frame = cap.read()
        if not ret:
            st.warning("Cannot receive frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extract ROI (Region of Interest) for eyes
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Detect eyes
            num_eyes = detect_eyes(roi_gray, roi_color)

            if num_eyes == 0:
                if last_closed_time is None:
                    last_closed_time = time.time()
                else:
                    if time.time() - last_closed_time > 5:
                        st.warning("You seem unfocused!")
            else:
                last_closed_time = None

        # Display the frame
        st.image(frame, channels="BGR", use_column_width=True)

    # Release the camera and close OpenCV windows
    cap.release()

if __name__ == "__main__":
    main()
