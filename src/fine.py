# fines.py
class FineSystem:
    def calculate(self, stype, days_issued, late_days, books_count):
        # Rent per day for each student type
        if stype == "ug":
            rent_per_day = 10
        elif stype == "pg":
            rent_per_day = 15
        elif stype == "research":
            rent_per_day = 20
        else:
            rent_per_day = 10
        
        # Fine per day for late return
        if stype == "ug":
            fine_per_day = 20
        elif stype == "pg":
            fine_per_day = 10
        elif stype == "research":
            fine_per_day = 5
        else:
            fine_per_day = 20
        
        # Calculate charges
        rent = books_count * days_issued * rent_per_day
        fine = books_count * late_days * fine_per_day
        total = rent + fine
        
        return rent, fine, total
