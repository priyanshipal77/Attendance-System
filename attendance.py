import cv2
import os
import numpy as np
import pickle
import time
from datetime import datetime
import csv
from playsound import playsound
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize global variables
attendance_log = {}
cooldown_time = 20 # Cooldown period in seconds
sound_path = "notification.mp3.mp3"  # Path to the sound file

# Function to mark attendance
def mark_attendance(name):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Cooldown to avoid marking the same person's attendance repeatedly
    if name in attendance_log:
        last_time = attendance_log[name]
        if time.time() - last_time < cooldown_time:
            return  # Skip if within cooldown period

    # Mark attendance in the log
    attendance_log[name] = time.time()
    print(f"Attendance marked for {name} at {current_datetime}")

    # Ensure 'attendance.csv' is created and write the attendance
    if not os.path.exists('attendance.csv'):
        with open('attendance.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "DateTime"])

    with open('attendance.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, current_datetime])
    print(f"Attendance saved for {name}.")

    # Play a notification sound
    playsound(sound_path)

# Function to start face recognition
def start_face_recognition():
    global video, recognized, start_time
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        messagebox.showerror("Error", "Could not access the webcam")
        return

    # Load saved face data and names
    if not os.path.exists('data/face_data.pkl') or not os.path.exists('data/names.pkl'):
        messagebox.showerror("Error", "No training data found")
        return

    with open('data/face_data.pkl', 'rb') as f:
        face_data = pickle.load(f)
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)

    face_data = np.array(face_data)
    recognized = False
    start_time = time.time()

    print("Starting face recognition...")

    # Continuously capture frames from the webcam
    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.2, 5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            crop_img = frame[y:y + h, x:x + w]
            resize_img = cv2.resize(crop_img, (50, 50)).flatten()

            # Match the detected face with saved data using Euclidean distance
            min_dist = float('inf')
            recognized_name = None
            for i, saved_face in enumerate(face_data):
                dist = np.linalg.norm(saved_face - resize_img)
                if dist < min_dist:
                    min_dist = dist
                    recognized_name = names[i]

            # Threshold for recognition (adjust as needed)
            if min_dist < 10000:
                if recognized_name:
                    mark_attendance(recognized_name)
                    cv2.putText(frame, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    recognized = True
                    attendance_label.config(text="Attendance Marked", fg="green")

        # Convert frame to image to display in Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)
        frame_photo = ImageTk.PhotoImage(image=frame_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=frame_photo)
        canvas.image = frame_photo

        # Exit after cooldown period or if 'q' is pressed
        if recognized and time.time() - start_time > cooldown_time:
            break

        root.update()

    video.release()

# Function to stop face recognition
def stop_face_recognition():
    global video
    video.release()
    print("Face recognition stopped.")
    root.quit()  # Close the Tkinter window

# Tkinter setup
root = tk.Tk()
root.title("Face Recognition Attendance System")

# Create a canvas to display the webcam feed
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Button to start face recognition
start_button = tk.Button(root, text="Start Recognition", command=start_face_recognition)
start_button.pack(pady=5)

# Button to stop face recognition
stop_button = tk.Button(root, text="Stop Recognition", command=stop_face_recognition)
stop_button.pack(pady=5)

# Label for displaying attendance status
attendance_label = tk.Label(root, text="", font=("Arial", 16))
attendance_label.pack(pady=5)

# Initialize face detector
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Run the Tkinter main loop
root.mainloop()