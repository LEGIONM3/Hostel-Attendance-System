import cv2
import face_recognition
import numpy as np
import db_handler

def start_attendance_system():
    """Main loop for detecting faces and logging attendance."""
    print("Loading known faces...")
    known_names, known_encodings = db_handler.get_known_faces()
    
    if not known_names:
        print("No students registered! Please register someone first.")
        return

    print("Starting Attendance Camera... Press 'q' to quit.")
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            break
            
        # Optimization: Resize to 1/4
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Force uint8 type just to be safe (though resize usually keeps type)
        small_frame = small_frame.astype(np.uint8)
        
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame, dtype=np.uint8)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    db_handler.log_attendance(name)

            face_names.append(name)

        # Draw results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up
            top *= 4; right *= 4; bottom *= 4; left *= 4

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        cv2.imshow('Hostel Attendance System', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
