# student.py
import csv
from datetime import datetime
from fines import FineSystem

class Student:
    def __init__(self, sid, name, stype):
        self.sid = sid
        self.name = name
        self.stype = stype
        self.books_file = "books.csv"
        self.issued_file = "issued.csv"
    
    def view_books(self):
        print("\n--- AVAILABLE BOOKS ---")
        print("ID\tTitle\t\tAuthor\t\tAvailable")
        print("-" * 50)
        
        try:
            with open(self.books_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and len(row) >= 5:
                        if int(row[4]) > 0:  # Only show available books
                            print(f"{row[0]}\t{row[1][:15]}\t{row[2][:15]}\t{row[4]}")
        except:
            print("No books available")
    
    def request_book(self):
        bid = input("Enter Book ID to request: ")
        
        # Check book availability
        available = False
        book_name = ""
        
        try:
            with open(self.books_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == bid:
                        if int(row[4]) > 0:
                            available = True
                            book_name = row[1]
                            break
        except:
            pass
        
        if not available:
            print("Book not available or invalid ID!")
            return
        
        # Save request
        req_id = f"REQ{self.sid}{datetime.now().strftime('%H%M%S')}"
        
        try:
            with open("requests.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([req_id, bid, self.sid, "pending"])
            print(f"Book '{book_name}' requested successfully!")
            print(f"Request ID: {req_id}")
        except:
            print("Error saving request")
    
    def return_book(self):
        bid = input("Enter Book ID to return: ")
        
        # Find issued book
        issued = False
        issue_data = []
        
        try:
            with open(self.issued_file, "r") as f:
                reader = csv.reader(f)
                all_rows = list(reader)
                
            for row in all_rows:
                if row and row[1] == bid and row[2] == self.sid and row[6] == "issued":
                    issued = True
                    issue_data = row
                    break
        except:
            pass
        
        if not issued:
            print("No issued book found with this ID!")
            return
        
        # Get return details
        days = int(input("How many days you had the book? "))
        late_days = int(input("How many days late? "))
        
        # Calculate fine
        fs = FineSystem()
        rent, fine, total = fs.calculate(self.stype, days, late_days, 1)
        
        # Update book count
        try:
            books = []
            with open(self.books_file, "r") as f:
                reader = csv.reader(f)
                books = list(reader)
            
            for row in books:
                if row and row[0] == bid:
                    available = int(row[4])
                    row[4] = str(available + 1)
                    break
            
            with open(self.books_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(books)
        except:
            print("Error updating book data")
        
        print("\n--- RETURN RECEIPT ---")
        print(f"Student: {self.name} ({self.sid})")
        print(f"Book ID: {bid}")
        print(f"Rent: ₹{rent}")
        print(f"Late Fine: ₹{fine}")
        print(f"Total: ₹{total}")
        print("Book returned successfully!")
    
    def change_password(self):
        old = input("Enter old password: ")
        new = input("Enter new password: ")
        confirm = input("Confirm new password: ")
        
        if new != confirm:
            print("New passwords don't match!")
            return
        
        try:
            students = []
            with open("students.csv", "r") as f:
                reader = csv.reader(f)
                students = list(reader)
            
            updated = False
            for row in students:
                if row and row[0] == self.sid:
                    if row[3] == old:
                        row[3] = new
                        updated = True
                        break
                    else:
                        print("Old password is wrong!")
                        return
            
            if updated:
                with open("students.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(students)
                print("Password changed successfully!")
        except:
            print("Error changing password")

class StudentMenu:
    @staticmethod
    def show_menu(student):
        while True:
            print(f"\n--- STUDENT MENU ---")
            print(f"Welcome, {student.name}")
            print("1. View Available Books")
            print("2. Request a Book")
            print("3. Return a Book")
            print("4. Change Password")
            print("5. Logout")
            
            choice = input("Enter choice (1-5): ")
            
            if choice == "1":
                student.view_books()
            elif choice == "2":
                student.request_book()
            elif choice == "3":
                student.return_book()
            elif choice == "4":
                student.change_password()
            elif choice == "5":
                print("Logged out successfully!")
                break
            else:
                print("Invalid choice!")

# Create instance
student_menu = StudentMenu()
