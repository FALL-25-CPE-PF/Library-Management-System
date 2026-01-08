# admin.py
import csv

class Admin:
    def __init__(self):
        self.books_file = "books.csv"
        self.students_file = "students.csv"
    
    def add_book(self):
        print("\n--- ADD NEW BOOK ---")
        bid = input("Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        qty = input("Quantity: ")
        
        try:
            with open(self.books_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([bid, title, author, qty, qty])  # Available = Quantity
            print(f"Book '{title}' added successfully!")
        except:
            print("Error adding book")
    
    def add_student(self):
        print("\n--- ADD NEW STUDENT ---")
        sid = input("Student ID: ")
        name = input("Name: ")
        stype = input("Type (ug/pg/research): ").lower()
        password = input("Password: ")
        
        # Validate type
        if stype not in ["ug", "pg", "research"]:
            print("Invalid type! Using 'ug'")
            stype = "ug"
        
        try:
            with open(self.students_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([sid, name, stype, password])
            print(f"Student '{name}' added successfully!")
        except:
            print("Error adding student")
    
    def view_books(self):
        print("\n--- ALL BOOKS IN LIBRARY ---")
        print("ID\tTitle\t\tAuthor\t\tQty\tAvailable")
        print("-" * 60)
        
        try:
            with open(self.books_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and len(row) >= 5:
                        print(f"{row[0]}\t{row[1][:15]}\t{row[2][:15]}\t{row[3]}\t{row[4]}")
        except:
            print("No books in database")
    
    def manage_requests(self):
        print("\n--- PENDING REQUESTS ---")
        
        try:
            with open("requests.csv", "r") as f:
                reader = csv.reader(f)
                requests = [row for row in reader if row and row[3] == "pending"]
        except:
            requests = []
        
        if not requests:
            print("No pending requests!")
            return
        
        for i, req in enumerate(requests, 1):
            print(f"{i}. Request ID: {req[0]}, Book: {req[1]}, Student: {req[2]}")
        
        try:
            choice = int(input("\nSelect request number to approve (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(requests):
                selected = requests[choice-1]
                
                # Update book quantity
                books = []
                with open(self.books_file, "r") as f:
                    reader = csv.reader(f)
                    books = list(reader)
                
                for row in books:
                    if row and row[0] == selected[1]:
                        available = int(row[4])
                        if available > 0:
                            row[4] = str(available - 1)
                            
                            # Update book file
                            with open(self.books_file, "w", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerows(books)
                            
                            # Update request status
                            all_reqs = []
                            with open("requests.csv", "r") as f:
                                reader = csv.reader(f)
                                all_reqs = list(reader)
                            
                            for req_row in all_reqs:
                                if req_row and req_row[0] == selected[0]:
                                    req_row[3] = "approved"
                                    break
                            
                            with open("requests.csv", "w", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerows(all_reqs)
                            
                            print("Book issued successfully!")
                        else:
                            print("Book not available!")
                        break
        except:
            print("Invalid selection!")
    
    def change_password(self):
        old = input("Enter old password: ")
        new = input("Enter new password: ")
        confirm = input("Confirm new password: ")
        
        if new != confirm:
            print("New passwords don't match!")
            return
        
        try:
            admins = []
            with open("admin.csv", "r") as f:
                reader = csv.reader(f)
                admins = list(reader)
            
            updated = False
            for row in admins:
                if row and row[0] == "admin":
                    if row[1] == old:
                        row[1] = new
                        updated = True
                        break
                    else:
                        print("Old password is wrong!")
                        return
            
            if updated:
                with open("admin.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(admins)
                print("Password changed successfully!")
        except:
            print("Error changing password")

class AdminMenu:
    @staticmethod
    def show_menu():
        admin = Admin()
        
        while True:
            print("\n--- ADMIN MENU ---")
            print("1. Add New Book")
            print("2. Add New Student")
            print("3. View All Books")
            print("4. Manage Book Requests")
            print("5. Change Password")
            print("6. Logout")
            
            choice = input("Enter choice (1-6): ")
            
            if choice == "1":
                admin.add_book()
            elif choice == "2":
                admin.add_student()
            elif choice == "3":
                admin.view_books()
            elif choice == "4":
                admin.manage_requests()
            elif choice == "5":
                admin.change_password()
            elif choice == "6":
                print("Admin logged out!")
                break
            else:
                print("Invalid choice!")

# Create instance
admin_menu = AdminMenu()
