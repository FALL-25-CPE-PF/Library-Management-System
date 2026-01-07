class BookManager:

    def add_book(self):
        bid = input("Book ID: ")
        name = input("Name: ")
        author = input("Author: ")
        qty = input("Quantity: ")
        rent = input("Rent per day: ")

        with open("data/books.csv", "a") as f:
            f.write(f"{bid},{name},{author},{qty},{rent}\n")
        print("Book added")

    def view_books(self):
        print("\n--- BOOKS LIST ---")
        with open("data/books.csv") as f:
            for line in f:
                print(line.strip())

    def search_book(self):
        key = input("Enter book name or author: ").lower()
        with open("data/books.csv") as f:
            found = False
            for line in f:
                if key in line.lower():
                    print(line.strip())
                    found = True
            if not found:
                print("No book found")
