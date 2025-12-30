import db_handler
import register
import attendance

def main():
    db_handler.init_db()
    
    while True:
        print("\n=== HOSTEL ATTENDANCE SYSTEM ===")
        print("[1] Register New Student")
        print("[2] Start Attendance Mode")
        print("[3] Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            register.register_new_student()
        elif choice == '2':
            attendance.start_attendance_system()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
