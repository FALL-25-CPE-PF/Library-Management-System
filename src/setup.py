# setup.py
import csv
import os

def setup_files():
    files = {
        "admin.csv": [["username", "password"], ["admin", "admin123"]],
        "students.csv": [["sid", "name", "stype", "password"]],
        "books.csv": [["bid", "title", "author", "quantity", "available"]],
        "issued.csv": [["issue_id", "bid", "sid", "issue_date", "due_date", "return_date", "status"]],
        "requests.csv": [["req_id", "bid", "sid", "status"]]
    }
    
    for filename, data in files.items():
        if not os.path.exists(filename):
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print(f"Created {filename}")
        else:
            print(f"{filename} already exists")
    
    print("\nSetup complete!")

if __name__ == "__main__":
    setup_files()
