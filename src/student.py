from books import BookManager
from fine import FineSystem

class Student:

    def __init__(self):
        self.book = BookManager()
        self.fine = FineSystem()

    def login(self):
        u = input("Username: ")
        p = input("Password: ")

        with open("data/students.csv") as f:
            for line in f:
                user, pwd, stype = line.strip().split(",")
                if u == user and p == pwd:
                    print("Login successful")
                    self.menu(u, stype)
                    return
        print("Wrong student login")

    def menu(self, user, stype):
        while True:
            print("\n--- STUDENT MENU ---")
            print("1. View Books")
            print("2. Search Book")
            print("3. Request Book")
            print("4. Return Book")
            print("5. Change Password")
            print("6. Check Fine")
            print("7. Logout")

            ch = input("Choice: ")

            if ch == "1":
                self.book.view_books()
            elif ch == "2":
                self.book.search_book()
            elif ch == "3":
                self.request_book(user, stype)
            elif ch == "4":
                self.return_book(user)
            elif ch == "5":
                self.change_password(user)
            elif ch == "6":
                self.fine.show_fine(stype)
            elif ch == "7":
                break

    def request_book(self, user, stype):
        if stype == "visit":
            print("Visit students cannot issue books")
            return

        b = input("Book ID: ")
        with open("data/requests.csv", "a") as f:
            f.write(f"{user},{b}\n")
        print("Book requested")

    def return_book(self):
        days_issued = int(input("Kitne din ke liye book issue thi: "))
        late_days = int(input("Late days: "))
        books = int(input("Total books: "))

        fine_system = FineSystem()
        rent, fine, total = fine_system.calculate_fine(
            self.stype, days_issued, late_days, books
        )

        print("\n--- Bill Slip ---")
        print("Student:", self.name)
        print("Book Rent:", rent)
        print("Late Fine:", fine)
        print("Total Amount:", total)
        
    def change_password(self, user):
        old = input("Old password: ")
        n1 = input("New password: ")
        n2 = input("Confirm password: ")

        if n1 != n2:
            print("Password mismatch")
            return

        with open("data/students.csv") as f:
            lines = f.readlines()

        with open("data/students.csv", "w") as f:
            for line in lines:
                u, p, t = line.strip().split(",")
                if u == user and p == old:
                    f.write(f"{u},{n1},{t}\n")
                else:
                    f.write(line)
        print("Password changed")
