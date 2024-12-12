A Python-based attendance management system that utilizes face recognition technology to mark and log attendance automatically. This project integrates OpenCV for real-time face detection, Tkinter for a user-friendly interface, and CSV for attendance data storage.

**FEATURES**
Real-Time Face Detection: Leverages OpenCV's Haar Cascade to detect faces in real-time using a webcam.
Automated Attendance Logging: Marks and logs attendance with the date and time, preventing duplicate entries using a cooldown mechanism.
User-Friendly Interface: Interactive GUI built with Tkinter for easy operation.
Data Storage: Attendance records are saved in a CSV file for easy access and management.
Lightweight and Portable: Runs locally without requiring a database or internet connection.
_Technologies Used_
Python
OpenCV
Tkinter
NumPy
CSV
**HOW IT WORKS**
Train the system by storing face data for individuals.
Start the application to recognize faces in real-time via webcam.
Attendance is automatically logged in a CSV file with the person's name and timestamp.
Future Enhancements
Integration with a database for scalable data storage.
Adding multi-face recognition for group attendance marking.
Improved UI/UX design.
