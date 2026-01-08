# auth.py
import csv

class LoginSystem:
    def __init__(self):
        self.admin_file = "admin.csv"
        self.student_file = "students.csv"
        
    def admin_login(self):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        
        try:
            with open(self.admin_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == username and row[1] == password:
                        print("Admin login successful!")
                        return True
        except:
            pass
        
        print("Invalid admin credentials!")
        return False
    
    def student_login(self):
        student_id = input("Enter student ID: ")
        password = input("Enter password: ")
        
        try:
            with open(self.student_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == student_id and row[3] == password:
                        from student import Student
                        return Student(row[0], row[1], row[2])
        except:
            pass
        
        print("Invalid student credentials!")
        return None

# Create instance
login_system = LoginSystem()