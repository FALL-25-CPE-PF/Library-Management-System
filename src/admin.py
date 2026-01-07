from books import BookManager

class Admin:

    def __init__(self):
        self.book = BookManager()

    def login(self):
        u = input("Admin username: ")
        p = input("Password: ")

        with open("data/admin.csv") as f:
            for line in f:
                user, pwd = line.strip().split(",")
                if u == user and p == pwd:
                    print("Login successful")
                    self.menu()
                    return
        print("Wrong admin login")

    def menu(self):
        while True:
            print("\n--- ADMIN MENU ---")
            print("1. Add Student")
            print("2. View Students")
            print("3. Add Book")
            print("4. View Issued Books")
            print("5. View Requests")
            print("6. Approve Request")
            print("7. Change Password")
            print("8. Logout")

            ch = input("Choice: ")

            if ch == "1":
                self.add_student()
            elif ch == "2":
                self.view_students()
            elif ch == "3":
                self.book.add_book()
            elif ch == "4":
                self.view_issued()
            elif ch == "5":
                self.view_requests()
            elif ch == "6":
                self.approve_request()
            elif ch == "7":
                self.change_password()
            elif ch == "8":
                break

    def add_student(self):
        u = input("Username: ")
        p = input("Password: ")
        t = input("Type (ug/pg/research/visit): ")

        with open("data/students.csv", "a") as f:
            f.write(f"{u},{p},{t}\n")
        print("Student added")

    def view_students(self):
        print("\n--- STUDENTS LIST ---")
        with open("data/students.csv") as f:
            for line in f:
                print(line.strip())

    def view_issued(self):
        print("\n--- ISSUED BOOKS ---")
        with open("data/issued.csv") as f:
            for line in f:
                print(line.strip())

    def view_requests(self):
        print("\n--- REQUESTS ---")
        with open("data/requests.csv") as f:
            for line in f:
                print(line.strip())

    def approve_request(self):
        u = input("Username: ")
        b = input("Book ID: ")

        with open("data/issued.csv", "a") as f:
            f.write(f"{u},{b}\n")
        print("Request approved")

    def change_password(self):
        old = input("Old password: ")
        new = input("New password: ")

        with open("data/admin.csv") as f:
            lines = f.readlines()

        with open("data/admin.csv", "w") as f:
            for line in lines:
                u, p = line.strip().split(",")
                if p == old:
                    f.write(f"{u},{new}\n")
                else:
                    f.write(line)
        print("Password changed")
