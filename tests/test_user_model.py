import pytest
from model.user_model import UserModel
import json

def test_admin_initialization(setup_test_files):
    """Test that admin account is properly initialized"""
    # Admin file should be created with default credentials
    with open(UserModel.ADMIN_FILE, 'r') as f:
        admin_data = json.load(f)
    
    assert admin_data['username'] == 'admin'
    # Test with known hash of 'admin123'
    assert admin_data['password'] == '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'

def test_add_user(setup_test_files):
    """Test adding a new cashier"""
    # Add a new cashier
    assert UserModel.add_user('john', 'password123')
    
    # Verify cashier was added
    with open(UserModel.CASHIERS_FILE, 'r') as f:
        cashiers = json.load(f)
    
    assert 'john' in cashiers
    # Verify password was hashed
    assert len(cashiers['john']) == 64  # SHA-256 hash length

def test_add_duplicate_user(setup_test_files):
    """Test adding a duplicate cashier"""
    # Add first cashier
    UserModel.add_user('john', 'password123')
    
    # Try to add duplicate
    with pytest.raises(ValueError) as exc:
        UserModel.add_user('john', 'different_password')
    assert "already exists" in str(exc.value)

def test_add_invalid_user(setup_test_files):
    """Test adding users with invalid credentials"""
    # Test empty username
    with pytest.raises(ValueError):
        UserModel.add_user('', 'password123')
    
    # Test empty password
    with pytest.raises(ValueError):
        UserModel.add_user('john', '')
    
    # Test admin username
    with pytest.raises(ValueError):
        UserModel.add_user('admin', 'password123')

def test_update_user(setup_test_files, sample_cashiers):
    """Test updating a cashier's password"""
    # Add a test cashier
    UserModel.add_user('john', 'password123')
    
    # Update password
    assert UserModel.update_user('john', 'newpassword123')
    
    # Verify password was updated
    with open(UserModel.CASHIERS_FILE, 'r') as f:
        cashiers = json.load(f)
    
    old_hash = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'  # hash of 'password'
    assert cashiers['john'] != old_hash

def test_update_nonexistent_user(setup_test_files):
    """Test updating a non-existent cashier"""
    with pytest.raises(ValueError) as exc:
        UserModel.update_user('nonexistent', 'password123')
    assert "not found" in str(exc.value)

def test_delete_user(setup_test_files):
    """Test deleting a cashier"""
    # Add a test cashier
    UserModel.add_user('john', 'password123')
    
    # Delete the cashier
    assert UserModel.delete_user('john')
    
    # Verify cashier was deleted
    with open(UserModel.CASHIERS_FILE, 'r') as f:
        cashiers = json.load(f)
    
    assert 'john' not in cashiers

def test_delete_nonexistent_user(setup_test_files):
    """Test deleting a non-existent cashier"""
    with pytest.raises(ValueError) as exc:
        UserModel.delete_user('nonexistent')
    assert "not found" in str(exc.value)

def test_delete_admin(setup_test_files):
    """Test that admin cannot be deleted"""
    with pytest.raises(ValueError) as exc:
        UserModel.delete_user('admin')
    assert "Cannot delete admin" in str(exc.value)

def test_get_all_users(setup_test_files):
    """Test getting list of all cashiers"""
    # Add test cashiers
    UserModel.add_user('john', 'password123')
    UserModel.add_user('mary', 'password456')
    
    users = UserModel.get_all_users()
    assert isinstance(users, list)
    assert 'john' in users
    assert 'mary' in users
    assert len(users) == 2

def test_validate_admin(setup_test_files):
    """Test admin login validation"""
    # Test correct credentials
    assert UserModel.validate_user('admin', 'admin123')
    
    # Test incorrect password
    assert not UserModel.validate_user('admin', 'wrong_password')

def test_validate_cashier(setup_test_files):
    """Test cashier login validation"""
    # Add a test cashier
    UserModel.add_user('john', 'password123')
    
    # Test correct credentials
    assert UserModel.validate_user('john', 'password123')
    
    # Test incorrect password
    assert not UserModel.validate_user('john', 'wrong_password')
    
    # Test non-existent cashier
    assert not UserModel.validate_user('nonexistent', 'password123') 