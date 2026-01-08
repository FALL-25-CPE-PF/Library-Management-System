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
