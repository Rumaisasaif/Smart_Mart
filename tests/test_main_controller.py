import pytest
from controller.main_controller import MainController
import json

@pytest.fixture
def controller():
    """Fixture providing a MainController instance"""
    return MainController()

def test_controller_initialization(controller, setup_test_files):
    """Test controller initialization"""
    # Verify admin account is created
    with open(controller.UserModel.ADMIN_FILE, 'r') as f:
        admin_data = json.load(f)
    
    assert admin_data['username'] == 'admin'
    assert len(admin_data['password']) == 64  # SHA-256 hash

def test_save_bill(controller, setup_test_files):
    """Test saving a bill through controller"""
    # Save a bill
    total = 999.99
    bill_number = controller.save_bill(total)
    
    # Verify bill was saved
    with open(controller.BillModel.BILLS_FILE, 'r') as f:
        bills = json.load(f)
    
    assert len(bills) == 1
    assert bills[0]['total'] == total
    assert bills[0]['bill_number'] == bill_number

def test_product_management(controller, setup_test_files):
    """Test product management through controller"""
    # Add product
    controller.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Verify product exists
    products = controller.get_all_products()
    assert "Electronics" in products
    assert ["Laptop", 999.99, 5] in products["Electronics"]
    
    # Update product
    controller.update_product("Electronics", "Laptop", 899.99, 10)
    products = controller.get_all_products()
    assert ["Laptop", 899.99, 10] in products["Electronics"]
    
    # Delete product
    controller.delete_product("Electronics", "Laptop")
    products = controller.get_all_products()
    assert len(products["Electronics"]) == 0

def test_cashier_management(controller, setup_test_files):
    """Test cashier management through controller"""
    # Add cashier
    controller.add_cashier("john", "password123")
    
    # Verify cashier exists
    cashiers = controller.get_all_cashiers()
    assert "john" in cashiers
    
    # Update cashier
    controller.update_cashier("john", "newpassword123")
    
    # Verify login with new password
    assert controller.validate_login("john", "newpassword123") == "cashier"
    
    # Delete cashier
    controller.delete_cashier("john")
    cashiers = controller.get_all_cashiers()
    assert "john" not in cashiers

def test_cart_operations(controller, setup_test_files):
    """Test cart operations through controller"""
    # Add a product
    controller.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Add to cart
    item = controller.add_to_cart("Electronics", "Laptop", 2)
    assert item == ("Laptop", 999.99, 2)
    
    # Calculate total
    total = controller.calculate_total([item])
    assert total == 1999.98  # 999.99 * 2
    
    # Reduce stock
    controller.reduce_stock("Electronics", "Laptop", 2)
    product = controller.get_product("Electronics", "Laptop")
    assert product[2] == 3  # Original 5 - 2

def test_product_queries(controller, setup_test_files, sample_products):
    """Test product query methods"""
    # Add sample products
    for category, items in sample_products.items():
        for name, price, qty in items:
            controller.add_product(category, name, price, qty)
    
    # Test get_products_by_category
    electronics = controller.get_products_by_category("Electronics")
    assert len(electronics) == 2
    assert ("Laptop", 999.99, 5) in electronics
    
    # Test get_product
    product = controller.get_product("Electronics", "Laptop")
    assert product == ("Laptop", 999.99, 5)
    
    # Test get_product_price
    price = controller.get_product_price("Laptop")
    assert price == 999.99

def test_login_validation(controller, setup_test_files):
    """Test login validation through controller"""
    # Test admin login
    assert controller.validate_login("admin", "admin123") == "admin"
    assert controller.validate_login("admin", "wrong_password") is None
    
    # Add a cashier
    controller.add_cashier("john", "password123")
    
    # Test cashier login
    assert controller.validate_login("john", "password123") == "cashier"
    assert controller.validate_login("john", "wrong_password") is None
    assert controller.validate_login("nonexistent", "password123") is None

def test_error_handling(controller, setup_test_files):
    """Test error handling in controller methods"""
    # Test invalid product operations
    with pytest.raises(ValueError):
        controller.add_product("InvalidCategory", "Product", 100, 5)
    
    with pytest.raises(ValueError):
        controller.update_product("Electronics", "NonexistentProduct", 100, 5)
    
    with pytest.raises(ValueError):
        controller.delete_product("Electronics", "NonexistentProduct")
    
    # Test invalid cashier operations
    with pytest.raises(ValueError):
        controller.add_cashier("", "password123")
    
    with pytest.raises(ValueError):
        controller.update_cashier("nonexistent", "password123")
    
    with pytest.raises(ValueError):
        controller.delete_cashier("nonexistent")
    
    # Test invalid cart operations
    with pytest.raises(ValueError):
        controller.add_to_cart("Electronics", "NonexistentProduct", 1)
    
    with pytest.raises(ValueError):
        controller.reduce_stock("Electronics", "NonexistentProduct", 1) 