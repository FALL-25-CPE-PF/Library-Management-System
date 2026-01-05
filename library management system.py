import csv
import os

# ---------------- FILE INIT ---------------- #

def init_files():
    files = ["admin.csv", "users.csv", "books.csv", "issued.csv", "requests.csv"]
    for f in files:
        if not os.path.exists(f):
            open(f, "w").close()

    # Default admin
    if os.stat("admin.csv").st_size == 0:
        with open("admin.csv", "a", newline="") as file:
            csv.writer(file).writerow(["admin", "admin123"])

init_files()

# ---------------- STUDENT LOGIN ---------------- #

def user_login():
    while True:
        student_id = input("Enter Student ID: ")
        student_pass = input("Enter Password: ")

        with open("users.csv", "r") as file:
            for row in csv.reader(file):
                if row and row[0] == student_id and row[4] == student_pass:
                    if row[3] == "ACTIVE":
                        print("User Login Successful")
                        show_user_status(student_id)
                        return student_id
                    else:
                        print("User is BLOCKED")
                        return None
            else:
                print("Invalid ID or Password")

        cont = input("Try again? (Y/N): ").upper()
        if cont != "Y":
            return None

# ---------------- HELPERS ---------------- #

def get_student_type(student_id):
    with open("users.csv", "r") as file:
        for row in csv.reader(file):
            if row and row[0] == student_id:
                return row[2]
    return None

def count_issued_books(student_id):
    count = 0
    with open("issued.csv", "r") as file:
        for row in csv.reader(file):
            if row and row[0] == student_id and row[4] == "NO":
                count += 1
    return count

def total_fine(student_id):
    fine = 0
    with open("issued.csv", "r") as file:
        for row in csv.reader(file):
            if row and row[0] == student_id and row[4] == "NO":
                fine += int(row[3])
    return fine

def show_user_status(student_id):
    stype = get_student_type(student_id)
    limits = {"UG": 2, "PG": 3, "RS": 5, "GUEST": 1}
    issued = count_issued_books(student_id)
    fine = total_fine(student_id)

    print("\n----- USER STATUS -----")
    print("Student Type:", stype)
    print("Books Issued:", issued)
    print("Total Allowed:", limits[stype])
    print("Remaining:", limits[stype] - issued)
    print("Unpaid Fine:", fine)
    print("-----------------------\n")

def block_user(student_id):
    updated_users = []
    with open("users.csv", "r") as file:
        for row in csv.reader(file):
            if row and row[0] == student_id:
                row[3] = "BLOCKED"
            updated_users.append(row)
    with open("users.csv", "w", newline="") as file:
        csv.writer(file).writerows(updated_users)

def unblock_user(student_id):
    updated_users = []
    with open("users.csv", "r") as file:
        for row in csv.reader(file):
            if row and row[0] == student_id:
                row[3] = "ACTIVE"
            updated_users.append(row)
    with open("users.csv", "w", newline="") as file:
        csv.writer(file).writerows(updated_users)