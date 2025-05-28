import pytest
from model.bill_model import BillModel
import json
from datetime import datetime

def test_save_bill(setup_test_files):
    """Test saving a new bill"""
    # Save a bill
    total = 999.99
    bill_number = BillModel.save_bill(total)
    
    # Verify bill was saved
    with open(BillModel.BILLS_FILE, 'r') as f:
        bills = json.load(f)
    
    assert len(bills) == 1
    bill = bills[0]
    
    # Verify bill structure
    assert bill['bill_number'] == bill_number
    assert bill['total'] == total
    assert 'date' in bill
    
    # Verify date format
    try:
        datetime.strptime(bill['date'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        pytest.fail("Date format is incorrect")

def test_save_multiple_bills(setup_test_files):
    """Test saving multiple bills"""
    # Save multiple bills
    totals = [999.99, 499.99, 1499.99]
    bill_numbers = []
    
    for total in totals:
        bill_number = BillModel.save_bill(total)
        bill_numbers.append(bill_number)
    
    # Verify bills were saved
    with open(BillModel.BILLS_FILE, 'r') as f:
        bills = json.load(f)
    
    assert len(bills) == len(totals)
    
    # Verify bill numbers are unique and sequential
    assert len(set(bill_numbers)) == len(bill_numbers)  # All numbers are unique
    assert sorted(bill_numbers) == bill_numbers  # Numbers are sequential

def test_save_invalid_bill(setup_test_files):
    """Test saving bills with invalid data"""
    # Test negative total
    with pytest.raises(ValueError):
        BillModel.save_bill(-100)
    
    # Test zero total
    with pytest.raises(ValueError):
        BillModel.save_bill(0)

def test_bill_number_format(setup_test_files):
    """Test bill number formatting"""
    # Save a few bills
    for total in [999.99, 499.99, 1499.99]:
        bill_number = BillModel.save_bill(total)
        
        # Verify bill number format (should be a string with leading zeros)
        assert isinstance(bill_number, str)
        assert bill_number.isdigit()
        assert len(bill_number) >= 4  # Should have at least 4 digits with leading zeros

def test_bill_persistence(setup_test_files):
    """Test that bills persist between model instances"""
    # Save a bill
    total1 = 999.99
    bill_number1 = BillModel.save_bill(total1)
    
    # Create a new bill with a new model instance
    total2 = 499.99
    bill_number2 = BillModel.save_bill(total2)
    
    # Verify both bills exist
    with open(BillModel.BILLS_FILE, 'r') as f:
        bills = json.load(f)
    
    assert len(bills) == 2
    assert any(b['bill_number'] == bill_number1 and b['total'] == total1 for b in bills)
    assert any(b['bill_number'] == bill_number2 and b['total'] == total2 for b in bills) 