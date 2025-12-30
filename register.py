import cv2
import face_recognition
import time
import numpy as np
import db_handler

def register_new_student():
    """Captures 5 images from webcam to register a new student."""
    name = input("Enter Student Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    print("Opening Webcam... Please look safely at the camera.")
    cap = cv2.VideoCapture(0)
    
    # Wait for camera to warm up
    time.sleep(1.0)
    
    captured_encodings = []
    required_captures = 5
    
    while len(captured_encodings) < required_captures:
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            print("Failed to capture video or empty frame.")
            break
            
        # Ensure frame is uint8 and contiguous RGB
        # Ensure frame is uint8 and contiguous RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame = np.ascontiguousarray(rgb_frame, dtype=np.uint8)
        
        face_locations = face_recognition.face_locations(rgb_frame)
        
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Capturing: {len(captured_encodings)}/{required_captures}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if len(face_locations) == 1:
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(display_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            try:
                # Encode immediately
                encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                captured_encodings.append(encoding)
                print(f"Captured image {len(captured_encodings)}")
                time.sleep(0.5) 
            except Exception as e:
                print(f"Encoding error: {e}")

        elif len(face_locations) > 1:
            cv2.putText(display_frame, "Multiple faces detected! One at a time.", (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        cv2.imshow('Registration - Press Q to Quit', display_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    if len(captured_encodings) == required_captures:
        print("Saving data...")
        db_handler.save_student(name, captured_encodings)
    else:
        print("Registration cancelled or incomplete.")
