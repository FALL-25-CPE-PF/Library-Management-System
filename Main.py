# ================== FILE MANAGER ==================
class FileManager:
    def read(self, filename):
        try:
            with open(filename, "r") as f:
                return f.readlines()
        except FileNotFoundError:
            return []

    def write(self, filename, data):
        with open(filename, "w") as f:
            f.writelines(data)

    def append(self, filename, data):
        with open(filename, "a") as f:
            f.write(data)


fm = FileManager()

# ================== FILE INIT ==================
def init_files():
    files = [
        "admin.csv",
        "students.csv",
        "books.csv",
        "requests.csv",
        "issued_books.csv",
        "fine.csv"
    ]
    for f in files:
        open(f, "a").close()

    if len(fm.read("admin.csv")) == 0:
        fm.append("admin.csv", "admin,admin123\n")


# ================== STUDENT ==================
class Student:
    issue_limit = 0
    fine_rate = 0
    rent_per_day = 10

    def __init__(self, sid, name, stype):
        self.sid = sid
        self.name = name
        self.stype = stype


class Undergraduate(Student):
    issue_limit = 2
    fine_rate = 20


class Postgraduate(Student):
    issue_limit = 4
    fine_rate = 15


class Research(Student):
    issue_limit = 6
    fine_rate = 10


class Guest(Student):
    issue_limit = 0
    fine_rate = 0


# ================== ADMIN ==================
class Admin:
    def login(self):
        u = input("Username: ")
        p = input("Password: ")
        for line in fm.read("admin.csv"):
            user, pwd = line.strip().split(",")
            if u == user and p == pwd:
                self.username = u
                return True
        return False

    def change_password(self):
        old = input("Old Password: ")
        new = input("New Password: ")
        con = input("Confirm Password: ")
        if new != con:
            print("Password mismatch")
            return
        data = fm.read("admin.csv")
        updated = []
        for line in data:
            u, p = line.strip().split(",")
            if u == self.username:
                if p != old:
                    print("Old password incorrect")
                    return
                updated.append(f"{u},{new}\n")
            else:
                updated.append(line)
        fm.write("admin.csv", updated)
        print("Admin password changed successfully")

    def add_student(self):
        sid = input("Student ID: ")
        name = input("Name: ")
        stype = input("Type (UG/PG/RS/GUEST): ").upper()
        password = input("Password: ")
        fm.append("students.csv", f"{sid},{name},{stype},{password}\n")
        print("Student added successfully")

    def add_book(self):
        bid = input("Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        qty = input("Quantity: ")
        fm.append("books.csv", f"{bid},{title},{author},{qty}\n")
        print("Book added")

    def view_books(self):
        print("\nID | Title | Author | Qty")
        for line in fm.read("books.csv"):
            print(line.strip())

    def view_students(self):
        print("\nID | Name | Type")
        for line in fm.read("students.csv"):
            sid, name, stype, _ = line.strip().split(",")
            print(sid, name, stype)

    def approve_requests(self):
        reqs = fm.read("requests.csv")
        if not reqs:
            print("No requests")
            return

        for r in reqs:
            print(r.strip())

        sid = input("Student ID: ")
        bid = input("Book ID: ")

        books = fm.read("books.csv")
        updated = []
        issued = False

        for line in books:
            b = line.strip().split(",")
            if b[0] == bid and int(b[3]) > 0:
                b[3] = str(int(b[3]) - 1)
                issued = True
            updated.append(",".join(b) + "\n")

        if not issued:
            print("Book not available")
            return

        fm.write("books.csv", updated)
        fm.append("issued_books.csv", f"{sid},{bid},0\n")
        fm.write("requests.csv", [r for r in reqs if r.strip() != f"{sid},{bid}"])
        print("Book issued successfully")


# ================== ISSUE MANAGER ==================
class IssueManager:
    def request_book(self, student):
        if student.issue_limit == 0:
            print("Guests cannot request books")
            return
        bid = input("Book ID: ")
        fm.append("requests.csv", f"{student.sid},{bid}\n")
        print("Request sent")

    def return_book(self, student):
        bid = input("Book ID: ")
        try:
            days_kept = int(input("Enter number of days the book was kept: "))
        except ValueError:
            print("Invalid input for days")
            return

        issued = fm.read("issued_books.csv")
        new_issued = []
        found = False

        for line in issued:
            s, b, *_ = line.strip().split(",")
            if s == student.sid and b == bid:
                late_days = max(0, days_kept - 7)  # subtract first 7 days
                fine = late_days * student.fine_rate
                rent = days_kept * student.rent_per_day
                total = fine + rent

                fm.append("fine.csv",
                          f"{student.sid},{bid},{days_kept},{late_days},{fine},{rent},{total}\n")

                print(f"Days kept: {days_kept}")
                print(f"Late days: {late_days}")
                print(f"Rent: {rent}")
                print(f"Fine: {fine}")
                print(f"Total: {total}")

                found = True
            else:
                new_issued.append(line)

        if not found:
            print("Record not found")
            return

        fm.write("issued_books.csv", new_issued)

        # Update book quantity
        books = fm.read("books.csv")
        updated_books = []
        for line in books:
            b = line.strip().split(",")
            if b[0] == bid:
                b[3] = str(int(b[3]) + 1)
            updated_books.append(",".join(b) + "\n")
        fm.write("books.csv", updated_books)
        print("Book returned successfully")


# ================== SYSTEM ==================
class LibrarySystem:
    def admin_menu(self):
        admin = Admin()
        if not admin.login():
            print("Invalid admin login")
            return

        while True:
            print("\n1.Add Student\n2.Add Book\n3.View Students\n4.View Books\n5.Approve Requests\n6.Change Password\n7.Exit")
            ch = input("Choice: ")
            if ch == "1":
                admin.add_student()
            elif ch == "2":
                admin.add_book()
            elif ch == "3":
                admin.view_students()
            elif ch == "4":
                admin.view_books()
            elif ch == "5":
                admin.approve_requests()
            elif ch == "6":
                admin.change_password()
            else:
                break

    def student_menu(self):
        sid = input("Student ID: ")
        pwd = input("Password: ")

        student = None
        student_pwd = None
        for line in fm.read("students.csv"):
            s, name, stype, p = line.strip().split(",")
            if s == sid and p == pwd:
                student_pwd = p
                if stype == "UG":
                    student = Undergraduate(s, name, stype)
                elif stype == "PG":
                    student = Postgraduate(s, name, stype)
                elif stype == "RS":
                    student = Research(s, name, stype)
                else:
                    student = Guest(s, name, stype)

        if not student:
            print("Invalid student login")
            return

        im = IssueManager()

        while True:
            print("\n1.Available Books\n2.Request Book\n3.Return Book\n4.View Fine\n5.Change Password\n6.Exit")
            ch = input("Choice: ")
            if ch == "1":
                print("".join(fm.read("books.csv")))
            elif ch == "2":
                im.request_book(student)
            elif ch == "3":
                im.return_book(student)
            elif ch == "4":
                print("".join(fm.read("fine.csv")))
            elif ch == "5":
                self.change_student_password(student, student_pwd)
            else:
                break

    def change_student_password(self, student, old_pwd):
        old = input("Old Password: ")
        if old != old_pwd:
            print("Old password incorrect")
            return
        new = input("New Password: ")
        con = input("Confirm Password: ")
        if new != con:
            print("Password mismatch")
            return

        data = fm.read("students.csv")
        updated = []
        for line in data:
            sid, name, stype, pwd = line.strip().split(",")
            if sid == student.sid:
                updated.append(f"{sid},{name},{stype},{new}\n")
            else:
                updated.append(line)
        fm.write("students.csv", updated)
        print("Password changed successfully")

    def run(self):
        init_files()
        while True:
            print("\n1.Admin Login\n2.Student Login\n3.Exit")
            ch = input("Choice: ")
            if ch == "1":
                self.admin_menu()
            elif ch == "2":
                self.student_menu()
            else:
                break


# ================== RUN ==================
if __name__ == "__main__":
    LibrarySystem().run()

