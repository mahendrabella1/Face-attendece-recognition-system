import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime
import face_recognition
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# Paths and files
USER_IMAGE_PATH = 'users/'
ATTENDANCE_FILE = 'attendance.csv'

if not os.path.exists(USER_IMAGE_PATH):
    os.makedirs(USER_IMAGE_PATH)

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'w') as f:
        f.write('Name,Date,Time\n')

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        tk.Label(self.root, text="Attendance System", font=("Arial", 20)).pack(pady=20)

        # Buttons
        tk.Button(self.root, text="Register New User", command=self.register_user, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Log In", command=self.recognize_user, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View Attendance Details", command=self.show_attendance_details, font=("Arial", 14)).pack(pady=10)

    def register_user(self):
        name = simpledialog.askstring("Input", "Enter your name:")
        if not name:
            messagebox.showwarning("Warning", "Name cannot be empty.")
            return
        
        user_folder = os.path.join(USER_IMAGE_PATH, name)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Info", "Capturing your image. Please look at the camera...")
        
        ret, frame = cap.read()
        if ret:
            file_path = os.path.join(user_folder, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(file_path, frame)
            messagebox.showinfo("Success", f"Registration successful. Your image is saved as {file_path}")
        else:
            messagebox.showerror("Error", "Failed to capture your image.")
        
        cap.release()
        cv2.destroyAllWindows()

    def recognize_user(self):
        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Info", "Recognizing face. Please look at the camera...")
        
        known_face_encodings = []
        known_face_names = []
        
        for name in os.listdir(USER_IMAGE_PATH):
            user_folder = os.path.join(USER_IMAGE_PATH, name)
            for filename in os.listdir(user_folder):
                if filename.endswith(".jpg"):
                    img = face_recognition.load_image_file(os.path.join(user_folder, filename))
                    encoding = face_recognition.face_encodings(img)
                    if encoding:
                        known_face_encodings.append(encoding[0])
                        known_face_names.append(name)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image.")
                break
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_cascade.detectMultiScale(rgb_frame, 1.1, 4)
            
            face_encodings = face_recognition.face_encodings(rgb_frame)
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                
                current_time = datetime.now().strftime('%H:%M:%S')
                current_date = datetime.now().strftime('%Y-%m-%d')
                
                with open(ATTENDANCE_FILE, 'a') as f:
                    f.write(f'{name},{current_date},{current_time}\n')
                
                messagebox.showinfo("Info", f"Welcome, {name}! Your attendance has been recorded.")
                break
            
            if name != "Unknown":
                break
        
        cap.release()
        cv2.destroyAllWindows()

    def show_attendance_details(self):
        if not os.path.exists(ATTENDANCE_FILE):
            messagebox.showwarning("Warning", "No attendance data available.")
            return
        
        df = pd.read_csv(ATTENDANCE_FILE)
        user_attendance = df.groupby('Name').size()
        total_days = len(df['Date'].unique())
        all_users = os.listdir(USER_IMAGE_PATH)
        attendance_details = ""

        for name in all_users:
            present_days = user_attendance.get(name, 0)
            absent_days = total_days - present_days
            percentage = (present_days / total_days) * 100 if total_days > 0 else 0
            attendance_details += (f"Name: {name}\n"
                                   f"Present Days: {present_days}\n"
                                   f"Absent Days: {absent_days}\n"
                                   f"Attendance Percentage: {percentage:.2f}%\n\n")

        messagebox.showinfo("Attendance Details", attendance_details)

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()
