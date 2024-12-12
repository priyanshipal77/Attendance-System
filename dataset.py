import cv2
import os
import numpy as np
import pickle

# Initialize webcam and face detection
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error: Could not access the webcam")
    exit()

# Load the Haar Cascade for face detection
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize data storage for face images
face_data = []
i = 0
name = input("Enter your Name: ")

# Create a directory to store data if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

print("Starting to collect face data...")

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        crop_img = frame[y:y + h, x:x + w]
        resize_img = cv2.resize(crop_img, (50, 50))

        # Collect face data every 10 frames
        if len(face_data) < 20 and i % 10 == 0:
            face_data.append(resize_img.flatten())
            cv2.putText(frame, f"Collected: {len(face_data)}", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    i += 1
    cv2.imshow("Face Detection", frame)

    if len(face_data) == 20:
        print("Collected 20 face images")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

face_data = np.array(face_data)
names = [name] * 20

# Save face data using pickle
face_data_file = 'data/face_data.pkl'
names_file = 'data/names.pkl'
# Load existing data if available
if os.path.exists(face_data_file) and os.path.exists(names_file):
    with open(face_data_file, 'rb') as f:
        existing_faces = pickle.load(f)
    with open(names_file, 'rb') as f:
        existing_names = pickle.load(f)

    face_data = np.append(existing_faces, face_data, axis=0)
    names = existing_names + names

# Save updated data
with open(face_data_file, 'wb') as f:
    pickle.dump(face_data, f)
with open(names_file, 'wb') as f:
    pickle.dump(names, f)

print("Face data saved successfully!")