import os
import json
from datetime import datetime

class BillModel:
    BILLS_FILE = "bills.txt"

    @staticmethod
    def save_bill(total):
        """Save a bill with the given total"""
        if total <= 0:
            raise ValueError("Total must be positive")

        try:
            with open(BillModel.BILLS_FILE, 'r') as f:
                bills = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            bills = []

        bill_number = str(len(bills) + 1).zfill(4)  # Format as 0001, 0002, etc.
        bill = {
            'bill_number': bill_number,
            'total': total,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        bills.append(bill)

        with open(BillModel.BILLS_FILE, 'w') as f:
            json.dump(bills, f)

        return bill_number

    @classmethod
    def get_all_bills(cls):
        """
        Get all bills from the bills.txt file
        Returns a list of tuples: (bill_number, total)
        """
        bills = []
        if os.path.exists(cls.BILLS_FILE):
            with open(cls.BILLS_FILE, "r") as f:
                for line in f:
                    try:
                        bill_part, total_part = line.strip().split(":")
                        bill_number = int(bill_part.split()[1])
                        total = float(total_part.strip())
                        bills.append((bill_number, total))
                    except:
                        continue
        return bills
