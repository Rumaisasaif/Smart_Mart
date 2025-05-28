import pytest
from model.product_model import ProductModel
import json

def test_add_product(setup_test_files):
    """Test adding a new product"""
    # Add a new product
    assert ProductModel.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Verify product was added
    with open(ProductModel.PRODUCTS_FILE, 'r') as f:
        products = json.load(f)
    
    assert len(products["Electronics"]) == 1
    assert products["Electronics"][0] == ["Laptop", 999.99, 5]

def test_add_duplicate_product(setup_test_files):
    """Test adding a duplicate product"""
    # Add first product
    ProductModel.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Try to add duplicate
    with pytest.raises(ValueError) as exc:
        ProductModel.add_product("Electronics", "Laptop", 899.99, 3)
    assert "already exists" in str(exc.value)

def test_add_invalid_product(setup_test_files):
    """Test adding products with invalid data"""
    # Test invalid category
    with pytest.raises(ValueError):
        ProductModel.add_product("InvalidCategory", "Laptop", 999.99, 5)
    
    # Test empty name
    with pytest.raises(ValueError):
        ProductModel.add_product("Electronics", "", 999.99, 5)
    
    # Test negative price
    with pytest.raises(ValueError):
        ProductModel.add_product("Electronics", "Laptop", -999.99, 5)
    
    # Test negative quantity
    with pytest.raises(ValueError):
        ProductModel.add_product("Electronics", "Laptop", 999.99, -5)

def test_update_product(setup_test_files):
    """Test updating a product"""
    # Add a test product
    ProductModel.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Update product
    assert ProductModel.update_product("Electronics", "Laptop", 899.99, 10)
    
    # Verify product was updated
    with open(ProductModel.PRODUCTS_FILE, 'r') as f:
        products = json.load(f)
    
    assert products["Electronics"][0] == ["Laptop", 899.99, 10]

def test_update_nonexistent_product(setup_test_files):
    """Test updating a non-existent product"""
    with pytest.raises(ValueError) as exc:
        ProductModel.update_product("Electronics", "NonexistentProduct", 999.99, 5)
    assert "not found" in str(exc.value)

def test_delete_product(setup_test_files):
    """Test deleting a product"""
    # Add a test product
    ProductModel.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Delete the product
    assert ProductModel.delete_product("Electronics", "Laptop")
    
    # Verify product was deleted
    with open(ProductModel.PRODUCTS_FILE, 'r') as f:
        products = json.load(f)
    
    assert len(products["Electronics"]) == 0

def test_delete_nonexistent_product(setup_test_files):
    """Test deleting a non-existent product"""
    with pytest.raises(ValueError) as exc:
        ProductModel.delete_product("Electronics", "NonexistentProduct")
    assert "not found" in str(exc.value)

def test_get_all_products(setup_test_files, sample_products):
    """Test getting all products"""
    # Add sample products
    for category, items in sample_products.items():
        for name, price, qty in items:
            ProductModel.add_product(category, name, price, qty)
    
    # Get all products
    products = ProductModel.get_all_products()
    
    # Verify structure and content
    assert isinstance(products, dict)
    assert "Electronics" in products
    assert "Groceries" in products
    assert len(products["Electronics"]) == 2
    assert len(products["Groceries"]) == 2
    
    # Verify specific products
    electronics = products["Electronics"]
    assert ["Laptop", 999.99, 5] in electronics
    assert ["Smartphone", 599.99, 10] in electronics

def test_get_products_by_category(setup_test_files, sample_products):
    """Test getting products by category"""
    # Add sample products
    for category, items in sample_products.items():
        for name, price, qty in items:
            ProductModel.add_product(category, name, price, qty)
    
    # Get products by category
    electronics = ProductModel.get_products_by_category("Electronics")
    groceries = ProductModel.get_products_by_category("Groceries")
    
    # Verify electronics
    assert len(electronics) == 2
    assert ("Laptop", 999.99, 5) in electronics
    assert ("Smartphone", 599.99, 10) in electronics
    
    # Verify groceries
    assert len(groceries) == 2
    assert ("Bread", 2.99, 20) in groceries
    assert ("Milk", 3.99, 15) in groceries

def test_get_product(setup_test_files):
    """Test getting a specific product"""
    # Add a test product
    ProductModel.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Get the product
    product = ProductModel.get_product("Electronics", "Laptop")
    
    # Verify product details
    assert product == ("Laptop", 999.99, 5)
    
    # Test non-existent product
    assert ProductModel.get_product("Electronics", "NonexistentProduct") is None

def test_reduce_stock(setup_test_files):
    """Test reducing product stock"""
    # Add a test product
    ProductModel.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Reduce stock
    assert ProductModel.reduce_stock("Electronics", "Laptop", 2)
    
    # Verify stock was reduced
    product = ProductModel.get_product("Electronics", "Laptop")
    assert product[2] == 3  # New quantity
    
    # Test reducing more than available
    with pytest.raises(ValueError):
        ProductModel.reduce_stock("Electronics", "Laptop", 5)  # Only 3 left
    
    # Test reducing from non-existent product
    with pytest.raises(ValueError):
        ProductModel.reduce_stock("Electronics", "NonexistentProduct", 1)

def test_get_price(setup_test_files):
    """Test getting product price"""
    # Add a test product
    ProductModel.add_product("Electronics", "Laptop", 999.99, 5)
    
    # Get price
    price = ProductModel.get_price("Laptop")
    assert price == 999.99
    
    # Test non-existent product
    with pytest.raises(ValueError):
        ProductModel.get_price("NonexistentProduct") 