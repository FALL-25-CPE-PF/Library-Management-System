def create_file(filename, header):
    try:
        with open(filename, "r"):
            pass
    except:
        with open(filename, "w") as f:
            f.write(header + "\n")

def setup():
    # create all files in data folder
    create_file("data/admin.csv", "username,password")
    create_file("data/students.csv", "username,password,type")
    create_file("data/books.csv", "id,name,author,quantity,rent")
    create_file("data/issued.csv", "username,book_id")
    create_file("data/requests.csv", "username,book_id")

    # default admin
    with open("data/admin.csv", "r") as f:
        lines = f.readlines()

    if len(lines) == 1:
        with open("data/admin.csv", "a") as f:
            f.write("admin,123\n")

