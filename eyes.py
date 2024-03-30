import streamlit as st
import cv2
from PIL import Image
import numpy as np
import time

# Function to process video frame and detect eyes
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eyes_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    return frame

# Main function to run the application
def main():
    st.title("Real-time Study Session Monitoring")

    st.header("Student's Study Session")

    # Create a VideoCapture object to capture video from the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        st.error("Error: Unable to open webcam.")
        return

    # Display the video stream in the Streamlit app
    while True:
        ret, frame = cap.read()  # Read a frame from the webcam

        if not ret:
            st.error("Error: Unable to capture frame.")
            break

        # Process the frame (detect eyes)
        processed_frame = process_frame(frame)

        # Convert the frame from OpenCV BGR format to PIL format
        pil_frame = Image.fromarray(processed_frame[:,:,::-1])

        # Display the frame in the Streamlit app
        st.image(pil_frame, channels="BGR")

        # Sleep for a short duration to control the frame rate
        time.sleep(0.1)

    # Release the VideoCapture object and close the Streamlit app when done
    cap.release()

# Run the application
if __name__ == "__main__":
    main()
