# Hostel Attendance System

A Face Recognition-based Attendance System built with Python, OpenCV, and SQLite. This application automates the process of recording hostel attendance by recognizing registered students via a webcam.

## 📌 Features

-   **Face Registration**: Capture and store student facial encodings securely.
-   **Real-time Attendance**: Detects faces from a webcam feed and marks attendance instantly.
-   **Database Integration**: Uses SQLite to persist student data and attendance logs.
-   **Anti-Spamming**: Implements a 60-second cooldown to prevent multiple logs for the same person within a short time.
-   **Simple CLI**: Easy-to-use menu-driven interface.

## 🛠 Tech Stack

-   **Python 3.x**
-   **OpenCV** (`cv2`): For video capture and image processing.
-   **Face Recognition**: For generating face encodings and matching (dlib-based).
-   **SQLite3**: Lightweight database for storage.
-   **NumPy**: Efficient array manipluation.

## 📋 Prerequisites

Before running the project, ensure you have Python installed. You also need to install the required dependencies.

### Dependencies
The project relies on `face_recognition`, which requires `dlib`. Installing `dlib` can sometimes be tricky on Windows; you may need to install CMake and Visual Studio build tools first.

## 🚀 Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone <repository-url>
    cd hostel-attendance-system
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    *If `requirements.txt` is missing, manually install:*
    ```bash
    pip install opencv-python face-recognition numpy
    ```

## 🎮 Usage

Run the main script to start the application:

```bash
python main.py
```

You will see the following menu:

```text
=== HOSTEL ATTENDANCE SYSTEM ===
[1] Register New Student
[2] Start Attendance Mode
[3] Exit
```

### 1. Register New Student
-   Select option **1**.
-   Enter the student's name.
-   Look at the camera. The system will capture **5 distinct images** to build a reliable face encoding.
-   Data is saved to `attendance.db`.

### 2. Start Attendance Mode
-   Select option **2**.
-   The webcam window will open.
-   The system will scan for faces.
-   **Green Box**: Known student (Attendance Logged).
-   **Red Box**: Unknown face.
-   Press `q` to quit the camera view.

### 3. View Data
-   Attendance logs are stored in the `attendance_logs` table in `attendance.db`.
-   You can view them using any SQLite viewer or by writing a simple script to query the table.

## 📂 Project Structure

```
├── main.py          # Entry point of the application (Menu)
├── register.py      # Module to handle student registration
├── attendance.py    # Module to run the attendance system
├── db_handler.py    # Database operations (Init, Save, Log)
├── requirements.txt # Python dependencies
└── attendance.db    # SQLite database (Created automatically)
```

## ⚙️ Configuration
-   **Encodings**: The system currently captures 5 frames per registration to ensure accuracy.
-   **Cooldown**: Default log cooldown is set to **60 seconds** in `db_handler.py`.

## 🤝 Future Improvements
-   Add a GUI (Graphical User Interface).
-   Export attendance logs to CSV/Excel.
-   Admin dashboard for viewing logs.
-   Remote database support.
