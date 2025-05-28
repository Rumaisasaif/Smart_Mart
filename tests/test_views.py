import pytest
import tkinter as tk
from tkinter import ttk
from view.login_view import LoginView
from view.admin_view import AdminView
from view.cashier_view import CashierView
from controller.main_controller import MainController

@pytest.fixture
def mock_tk(monkeypatch):
    """Mock tkinter components"""
    class MockTk:
        def __init__(self):
            self.calls = []
            self.geometry_val = None
            self.title_val = None
            self.destroyed = False
            
        def title(self, val):
            self.title_val = val
            self.calls.append(('title', val))
            
        def geometry(self, val):
            self.geometry_val = val
            self.calls.append(('geometry', val))
            
        def mainloop(self):
            self.calls.append('mainloop')
            
        def destroy(self):
            self.destroyed = True
            self.calls.append('destroy')
            
        def winfo_screenwidth(self):
            return 1920
            
        def winfo_screenheight(self):
            return 1080
    
    class MockVar:
        def __init__(self, value=''):
            self.value = value
            
        def get(self):
            return self.value
            
        def set(self, value):
            self.value = value
    
    class MockEntry:
        def __init__(self):
            self.value = ''
            self.state = 'normal'
            
        def get(self):
            return self.value
            
        def delete(self, start, end):
            self.value = ''
            
        def insert(self, index, value):
            self.value = value
            
        def configure(self, **kwargs):
            pass
    
    class MockCombobox:
        def __init__(self, values=None):
            self.value = ''
            self.values = values or []
            
        def get(self):
            return self.value
            
        def set(self, value):
            self.value = value
            
        def configure(self, **kwargs):
            pass
    
    class MockTreeview:
        def __init__(self):
            self.items = {}
            self.selected_item = None
            
        def get_children(self):
            return list(self.items.keys())
            
        def delete(self, item_id):
            if item_id in self.items:
                del self.items[item_id]
            
        def insert(self, parent, index, values):
            item_id = f"I{len(self.items)}"
            self.items[item_id] = values
            return item_id
            
        def selection(self):
            return [self.selected_item] if self.selected_item else []
            
        def item(self, item_id):
            return {'values': self.items[item_id]}
            
        def configure(self, **kwargs):
            pass
    
    # Patch tkinter classes
    monkeypatch.setattr('tkinter.Tk', MockTk)
    monkeypatch.setattr('tkinter.StringVar', lambda: MockVar())
    monkeypatch.setattr('tkinter.Entry', MockEntry)
    monkeypatch.setattr('tkinter.ttk.Entry', MockEntry)
    monkeypatch.setattr('tkinter.ttk.Combobox', MockCombobox)
    monkeypatch.setattr('tkinter.ttk.Treeview', MockTreeview)
    
    return MockTk()

def test_login_view_initialization(mock_tk, setup_test_files):
    """Test LoginView initialization"""
    view = LoginView()
    
    assert view.root.title_val == "Smart Mart - Login"
    assert "400x500" in view.root.geometry_val
    assert isinstance(view.controller, MainController)

def test_login_view_validation(mock_tk, setup_test_files, mock_messagebox):
    """Test login validation in LoginView"""
    view = LoginView()
    
    # Test empty credentials
    view.username_entry.value = ""
    view.password_entry.value = ""
    view.login()
    assert ("error", "Error", "Please enter both username and password") in mock_messagebox.shown_messages
    
    # Test invalid credentials
    view.username_entry.value = "wrong"
    view.password_entry.value = "wrong"
    view.login()
    assert ("error", "Error", "Invalid username or password") in mock_messagebox.shown_messages
    
    # Test valid admin login
    view.username_entry.value = "admin"
    view.password_entry.value = "admin123"
    view.login()
    assert view.root.destroyed

def test_admin_view_initialization(mock_tk, setup_test_files):
    """Test AdminView initialization"""
    view = AdminView()
    
    assert view.root.title_val == "Smart Mart - Admin Panel"
    assert "1000x700" in view.root.geometry_val
    assert isinstance(view.controller, MainController)

def test_admin_product_management(mock_tk, setup_test_files, mock_messagebox):
    """Test product management in AdminView"""
    view = AdminView()
    
    # Test adding product
    view.category_var.value = "Electronics"
    view.product_name.value = "Laptop"
    view.price.value = "999.99"
    view.quantity.value = "5"
    view.add_product()
    
    products = view.controller.get_all_products()
    assert ["Laptop", 999.99, 5] in products["Electronics"]
    
    # Test updating product
    view.price.value = "899.99"
    view.quantity.value = "10"
    view.update_product()
    
    products = view.controller.get_all_products()
    assert ["Laptop", 899.99, 10] in products["Electronics"]
    
    # Test deleting product
    view.product_tree.items = {"I0": ("Electronics", "Laptop", "$899.99", 10)}
    view.product_tree.selected_item = "I0"
    view.delete_product()
    
    products = view.controller.get_all_products()
    assert len(products["Electronics"]) == 0

def test_admin_cashier_management(mock_tk, setup_test_files, mock_messagebox):
    """Test cashier management in AdminView"""
    view = AdminView()
    
    # Test adding cashier
    view.cashier_username.value = "john"
    view.cashier_password.value = "password123"
    view.add_cashier()
    
    cashiers = view.controller.get_all_cashiers()
    assert "john" in cashiers
    
    # Test updating cashier
    view.cashier_password.value = "newpassword123"
    view.update_cashier()
    
    # Test deleting cashier
    view.cashier_tree.items = {"I0": ("john",)}
    view.cashier_tree.selected_item = "I0"
    view.delete_cashier()
    
    cashiers = view.controller.get_all_cashiers()
    assert "john" not in cashiers

def test_cashier_view_initialization(mock_tk, setup_test_files):
    """Test CashierView initialization"""
    view = CashierView("john")
    
    assert view.root.title_val == "Smart Mart - Cashier Panel (john)"
    assert "1200x800" in view.root.geometry_val
    assert isinstance(view.controller, MainController)
    assert view.username == "john"

def test_cashier_cart_operations(mock_tk, setup_test_files, mock_messagebox):
    """Test cart operations in CashierView"""
    view = CashierView("john")
    
    # Add a test product
    view.controller.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Test adding to cart
    view.category_var.value = "Electronics"
    view.product_var.value = "Laptop"
    view.quantity_var.value = "2"
    view.add_to_cart()
    
    assert len(view.cart) == 1
    assert view.cart[0] == ("Laptop", 999.99, 2)
    
    # Test payment processing
    view.payment_var.value = "Cash"
    view.process_payment()
    
    # Verify stock was reduced
    product = view.controller.get_product("Electronics", "Laptop")
    assert product[2] == 3  # Original 5 - 2
    
    # Verify cart was cleared
    assert len(view.cart) == 0

def test_cashier_view_error_handling(mock_tk, setup_test_files, mock_messagebox):
    """Test error handling in CashierView"""
    view = CashierView("john")
    
    # Test adding to cart without selection
    view.add_to_cart()
    assert ("error", "Error", "Please select both category and product") in mock_messagebox.shown_messages
    
    # Test invalid quantity
    view.category_var.value = "Electronics"
    view.product_var.value = "Laptop"
    view.quantity_var.value = "-1"
    view.add_to_cart()
    assert any("Quantity must be positive" in msg[2] for msg in mock_messagebox.shown_messages)
    
    # Test processing empty cart
    view.process_payment()
    assert ("info", "Info", "Cart is empty") in mock_messagebox.shown_messages 