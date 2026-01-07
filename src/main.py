from setup import setup
from admin import Admin
from student import Student

setup()

admin = Admin()
student = Student()

while True:
    print("\n1. Admin Login")
    print("2. Student Login")
    print("3. Exit")

    choice = input("Choice: ")

    if choice == "1":
        admin.login()
    elif choice == "2":
        student.login()
    elif choice == "3":
        break
