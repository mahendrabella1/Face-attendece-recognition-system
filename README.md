
# Face Recognition-Based Attendance System

This Python-based system utilizes facial recognition to automatically mark attendance and send daily email summaries. The system can register new users by capturing their face images, recognize faces during continuous video capture, and log attendance in a CSV file.

### Features:
- **User Registration**: Capture and register new users by saving their face images.
- **Face Recognition**: Continuously capture and recognize faces to mark attendance.
- **Attendance Logging**: Logs attendance in a CSV file with name, date, and time.
- **Voice Greeting**: Greets the recognized person with a voice message and logs their attendance.
- **Email Notification**: Sends daily attendance summary via email.
- **Real-time Operation**: Operates in real-time via the camera with continuous face detection.

---

### Prerequisites

- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **Libraries**: Install the following dependencies using pip:

```bash
pip install opencv-python face_recognition pyttsx3 pandas smtplib schedule
```

---

### Setup

1. **Directory Structure**:
   - `users/` – Folder where user images are saved.
   - `today.csv` – The CSV file that logs the attendance with columns: `Name`, `Date`, `Time`.

2. **Email Setup**:
   - Replace the `SENDER_EMAIL`, `SENDER_PASSWORD`, and `RECEIVER_EMAIL` variables in the script with valid email credentials.
   - This uses Gmail's SMTP server. Make sure you allow less secure apps or generate an app password if needed for Gmail.

---

### Running the System

1. **Start the system**:
   - Run the script `attendance_system.py`.

2. **Menu Options**:
   - **Option 1**: Register a new user. The user will be asked to look at the camera for face capture.
   - **Option 2**: Start continuous face recognition. The system will use your webcam to continuously capture and recognize faces, logging the attendance when a match is found.
   - **Option 3**: Exit the system.

3. **Attendance Recording**:
   - The system will log attendance in `today.csv` for every recognized face with the person's name, date, and time of attendance.

4. **Daily Email Summary**:
   - The system automatically sends a summary email at 9:45 PM daily, with the attendance recorded in `today.csv`.

---

### Code Walkthrough

- **`send_email()`**: Sends an email containing the attendance summary of the day.
- **`greet_and_record(name)`**: Greets the recognized user with a message and logs their attendance.
- **`register_user(name)`**: Captures and stores the user's face image for future recognition.
- **`recognize_faces()`**: Continuously detects faces using the webcam, compares them to stored face encodings, and records attendance if a match is found.
- **`schedule_daily_email()`**: Schedules and sends an email every day at 9:45 PM with the attendance summary.

---

### Example Workflow

1. When you run the script, you will see a menu prompting you to:
   - Register a new user.
   - Start face recognition.
   - Exit the system.

2. After registering a user, the system will save their face image in the `users/` folder. When their face is detected in future sessions, the system will greet them and log their attendance.

3. Each time a recognized face is detected, the system logs the attendance and saves it to `today.csv`.

4. Every day at 9:45 PM, the system sends an email with the day's attendance summary.


### Troubleshooting

- **Camera Not Found**: Ensure that your webcam is connected and accessible.
- **Incorrect Email Login**: If using Gmail, ensure that your email account allows "less secure apps" or generate an "app password."
- **Failed Image Capture**: Make sure the face is visible to the camera for a successful image capture.

