import pytest
import os
import json
import shutil
from pathlib import Path

@pytest.fixture(autouse=True)
def setup_test_files(tmp_path):
    """
    Creates temporary test files and cleans them up after tests.
    This fixture runs automatically for all tests.
    """
    # Store original file paths
    original_paths = {
        'products': 'products.txt',
        'cashiers': 'cashiers.txt',
        'admin': 'admin.txt',
        'bills': 'bills.txt'
    }
    
    # Create test files in temporary directory
    test_files = {}
    for key, filepath in original_paths.items():
        test_path = tmp_path / filepath
        test_files[key] = str(test_path)
        
        # Create empty files
        if key == 'products':
            data = {"Electronics": [], "Groceries": [], "Clothing": [], "Books": [], "Beauty": []}
        elif key == 'cashiers':
            data = {}
        elif key == 'admin':
            data = {"username": "admin", "password": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"}  # admin123
        elif key == 'bills':
            data = []
            
        with open(test_path, 'w') as f:
            json.dump(data, f)
    
    # Patch the file paths in the models
    from model.product_model import ProductModel
    from model.user_model import UserModel
    from model.bill_model import BillModel
    
    ProductModel.PRODUCTS_FILE = test_files['products']
    UserModel.CASHIERS_FILE = test_files['cashiers']
    UserModel.ADMIN_FILE = test_files['admin']
    BillModel.BILLS_FILE = test_files['bills']
    
    yield test_files
    
    # Cleanup: Delete temporary files
    for filepath in test_files.values():
        if os.path.exists(filepath):
            os.remove(filepath)

@pytest.fixture
def sample_products():
    """Fixture providing sample product data"""
    return {
        "Electronics": [
            ("Laptop", 999.99, 5),
            ("Smartphone", 599.99, 10)
        ],
        "Groceries": [
            ("Bread", 2.99, 20),
            ("Milk", 3.99, 15)
        ]
    }

@pytest.fixture
def sample_cashiers():
    """Fixture providing sample cashier data"""
    return {
        "john": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password
        "mary": "6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4"   # password123
    }

@pytest.fixture
def mock_messagebox(monkeypatch):
    """Mock tkinter messagebox for testing GUI interactions"""
    class MockMessageBox:
        def __init__(self):
            self.shown_messages = []
            self.last_response = True  # For yes/no dialogs
            
        def showerror(self, title, message):
            self.shown_messages.append(("error", title, message))
            
        def showinfo(self, title, message):
            self.shown_messages.append(("info", title, message))
            
        def askyesno(self, title, message):
            self.shown_messages.append(("yesno", title, message))
            return self.last_response
            
        def clear(self):
            self.shown_messages = []
            
    mock = MockMessageBox()
    monkeypatch.setattr("tkinter.messagebox", mock)
    return mock 