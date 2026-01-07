class FineSystem:
    def calculate_fine(self, stype, days_issued, late_days, books):
        rent_per_day = 10

        # Rent calculation
        rent = books * days_issued * rent_per_day

        # Late fine calculation
        if stype == "ug":
            fine = late_days * 20
        elif stype == "pg":
            fine = late_days * 10
        elif stype == "research":
            fine = late_days * 10
        else:
            fine = late_days * 30

        total = rent + fine
        return rent, fine, total
