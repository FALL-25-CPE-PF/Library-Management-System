# library_main.py
from auth import login_system
from student import student_menu
from admin import admin_menu

def main():
    while True:
        print("\n" + "="*40)
        print("LIBRARY MANAGEMENT SYSTEM")
        print("="*40)
        print("1. Admin Login")
        print("2. Student Login")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == "1":
            admin = login_system.admin_login()
            if admin:
                admin_menu.show_menu()
        
        elif choice == "2":
            student = login_system.student_login()
            if student:
                student_menu.show_menu(student)
        
        elif choice == "3":
            print("Thank you for using Library System!")
            break
        
        else:
            print("Invalid choice! Please enter 1, 2 or 3")

if __name__ == "__main__":
    main()
