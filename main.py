import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime
import face_recognition
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyttsx3
import schedule
import time
import threading

# Paths and files
USER_IMAGE_PATH = 'users/'
ATTENDANCE_FILE = 'today.csv'

if not os.path.exists(USER_IMAGE_PATH):
    os.makedirs(USER_IMAGE_PATH)

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'w') as f:
        f.write('Name,Date,Time\n')

# Email configuration
SENDER_EMAIL = 'your mail id--iam hiding my mail you can replace with your mail'
SENDER_PASSWORD = 'password'
RECEIVER_EMAIL = 'replace your receiver mail for whom you are sending'

# To store attendance data
attendance_data = []

def send_email():
    """Send an email notification for attendance summary."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Craft the email
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        message['Subject'] = f'Attendance Summary for {datetime.now().strftime("%Y-%m-%d")}'
        
        # Email for all recorded attendance
        df = pd.read_csv(ATTENDANCE_FILE)
        attendance_summary = df.to_string(index=False)
        body = f"Attendance Summary for {datetime.now().strftime('%Y-%m-%d')}:\n\n{attendance_summary}"
        
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.send_message(message)
        server.quit()

        print('Daily attendance summary email sent.')
    except Exception as e:
        print(f'Failed to send email: {str(e)}')

def greet_and_record(name):
    """Greet the recognized person and log their attendance."""
    engine = pyttsx3.init()
    current_hour = datetime.now().hour
    greeting = "Good morning" if current_hour < 12 else "Good afternoon"

    greeting_text = f"{greeting}, {name}! Attendance captured."
    engine.say(greeting_text)
    engine.runAndWait()

    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Append to attendance data
    attendance_data.append([name, current_date, current_time])

    # Write the data to the CSV file
    with open(ATTENDANCE_FILE, 'a', newline='') as f:
        writer = pd.DataFrame([[name, current_date, current_time]], columns=['Name', 'Date', 'Time'])
        writer.to_csv(f, header=False, index=False)

    print(f"Attendance captured for {name} at {current_time} on {current_date}.")

def register_user(name):
    """Register a new user by capturing their face."""
    user_folder = os.path.join(USER_IMAGE_PATH, name)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    cap = cv2.VideoCapture(0)
    print("Capturing image... Please look at the camera.")
    
    ret, frame = cap.read()
    if ret:
        file_path = os.path.join(user_folder, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        cv2.imwrite(file_path, frame)
        print(f"Registration successful. Your image is saved as {file_path}")
    else:
        print("Failed to capture your image.")

    cap.release()
    cv2.destroyAllWindows()

def recognize_faces():
    """Continuously recognize faces and mark attendance."""
    cap = cv2.VideoCapture(0)
    print("Starting continuous face recognition. Press 'q' to quit.")
    
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
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            
            if name != "Unknown":
                greet_and_record(name)
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting face recognition.")
            break

    cap.release()
    cv2.destroyAllWindows()

def schedule_daily_email():
    """Schedule a daily email at 10 PM."""
    schedule.every().day.at("09:45").do(send_email)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Start the email scheduling in a separate thread
    email_thread = threading.Thread(target=schedule_daily_email, daemon=True)
    email_thread.start()

    while True:
        print("1: Register a new user")
        print("2: Start continuous face recognition")
        print("3: Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the name of the person to register: ")
            register_user(name)
        elif choice == '2':
            recognize_faces()
        elif choice == '3':
            print("Exiting system.")
            break
        else:
            print("Invalid choice")
