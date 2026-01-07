class FineSystem:

    def show_fine(self, stype):
        days = int(input("Late days: "))

        if stype == "ug":
            fine = days * 20
        elif stype == "pg":
            fine = days * 10v
        elif stype == "research":
            fine = days * 10
        else:
            fine = days * 30

        print("Fine =", fine)
