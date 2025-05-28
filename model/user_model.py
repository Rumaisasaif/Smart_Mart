import os
import json
import hashlib

class UserModel:
    CASHIERS_FILE = "cashiers.txt"
    ADMIN_FILE = "admin.txt"
    
    # Default admin credentials - will be saved to admin.txt if it doesn't exist
    DEFAULT_ADMIN = {
        "username": "admin",
        "password": hashlib.sha256("admin123".encode()).hexdigest()
    }

    @classmethod
    def _init_admin(cls):
        """Initialize admin.txt with default credentials if it doesn't exist"""
        if not os.path.exists(cls.ADMIN_FILE):
            with open(cls.ADMIN_FILE, "w") as f:
                json.dump(cls.DEFAULT_ADMIN, f, indent=2)

    @classmethod
    def _load_cashiers(cls):
        """Load cashiers from file, create file if doesn't exist"""
        if not os.path.exists(cls.CASHIERS_FILE):
            # Create empty cashiers file
            with open(cls.CASHIERS_FILE, "w") as f:
                json.dump({}, f)
            return {}
        try:
            with open(cls.CASHIERS_FILE, "r") as f:
                data = f.read()
                return json.loads(data) if data else {}
        except:
            return {}

    @classmethod
    def _save_cashiers(cls, cashiers):
        """Save cashiers to file"""
        with open(cls.CASHIERS_FILE, "w") as f:
            json.dump(cashiers, f, indent=2)

    @classmethod
    def add_user(cls, username, password):
        if not username or not password:
            raise ValueError("Username and password are required")
            
        # Initialize admin file if it doesn't exist
        cls._init_admin()
            
        # Don't allow creating admin user
        if username.lower() == "admin":
            raise ValueError("Cannot create user with username 'admin'")
            
        cashiers = cls._load_cashiers()
        
        # Check if username already exists
        if username in cashiers:
            raise ValueError(f"Username '{username}' already exists")
            
        # Hash the password before storing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cashiers[username] = hashed_password
        
        cls._save_cashiers(cashiers)
        return True

    @classmethod
    def update_user(cls, username, new_password):
        if not username or not new_password:
            raise ValueError("Username and new password are required")
            
        # Don't allow updating admin password through this method
        if username.lower() == "admin":
            raise ValueError("Cannot update admin password through this method")
            
        cashiers = cls._load_cashiers()
        
        if username not in cashiers:
            raise ValueError(f"Username '{username}' not found")
            
        # Hash the new password
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        cashiers[username] = hashed_password
        
        cls._save_cashiers(cashiers)
        return True

    @classmethod
    def delete_user(cls, username):
        if not username:
            raise ValueError("Username is required")
            
        # Don't allow deleting admin
        if username.lower() == "admin":
            raise ValueError("Cannot delete admin user")
            
        cashiers = cls._load_cashiers()
        
        if username not in cashiers:
            raise ValueError(f"Username '{username}' not found")
            
        del cashiers[username]
        cls._save_cashiers(cashiers)
        return True

    @classmethod
    def get_all_users(cls):
        return list(cls._load_cashiers().keys())

    @classmethod
    def validate_user(cls, username, password):
        """
        Validate user credentials for both admin and cashiers
        Returns True if credentials are valid, False otherwise
        """
        # Initialize admin file if it doesn't exist
        cls._init_admin()
        
        # Hash the provided password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Check if it's admin
        if username.lower() == "admin":
            try:
                with open(cls.ADMIN_FILE, "r") as f:
                    admin_data = json.load(f)
                return admin_data.get("password", "") == hashed_password
            except:
                return False
        
        # Check if it's a cashier
        cashiers = cls._load_cashiers()
        stored_password = cashiers.get(username, "")
        return stored_password == hashed_password

    @classmethod
    def create_initial_admin(cls):
        """Create initial admin account if it doesn't exist"""
        cls._init_admin()
