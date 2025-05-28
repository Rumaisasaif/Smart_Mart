from model.product_model import ProductModel
from model.bill_model import BillModel
from model.user_model import UserModel

class MainController:
    def __init__(self):
        # Ensure admin account exists
        UserModel.create_initial_admin()

    def save_bill(self, total):
        return BillModel.save_bill(total)

    def add_product(self, category, name, price, quantity):
        return ProductModel.add_product(category, name, price, quantity)

    def update_product(self, category, name, new_price, new_quantity):
        return ProductModel.update_product(category, name, new_price, new_quantity)

    def get_all_products(self):
        return ProductModel.get_all_products()

    def delete_product(self, category, name):
        return ProductModel.delete_product(category, name)

    def get_product_price(self, name):
        return ProductModel.get_price(name)

    def add_to_cart(self, category, name, quantity=1):
        """
        Add product with quantity to cart.
        Returns tuple of (name, price, quantity)
        """
        product = ProductModel.get_product(category, name)
        if product is None:
            raise ValueError(f"Product '{name}' not found in category '{category}'")
        
        product_name, price, available_qty = product
        if quantity > available_qty:
            raise ValueError(f"Only {available_qty} items available for '{name}'")

        return (name, price, quantity)

    def calculate_total(self, cart):
        return sum(price * qty for _, price, qty in cart)

    def reduce_stock(self, category, name, quantity):
        """
        Reduce stock quantity of a product after purchase
        """
        return ProductModel.reduce_stock(category, name, quantity)

    def add_cashier(self, username, password):
        return UserModel.add_user(username, password)

    def update_cashier(self, username, password):
        return UserModel.update_user(username, password)

    def delete_cashier(self, username):
        return UserModel.delete_user(username)

    def get_all_cashiers(self):
        return UserModel.get_all_users()
    def get_products_by_category(self, category):
        """
        Return list of products in category as tuples with (name, price, quantity)
        """
        return ProductModel.get_products_by_category(category)

    def get_product(self, category, name):
        """
        Return a product info tuple (name, price, quantity) or None
        """
        return ProductModel.get_product(category, name)

    def validate_login(self, username, password):
        """
        Validate user login credentials
        Returns: 'admin', 'cashier', or None
        """
        if not username or not password:
            return None
            
        # First check if it's admin
        if username.lower() == "admin":
            if UserModel.validate_user(username, password):
                return "admin"
            return None
            
        # Then check if it's a valid cashier
        if UserModel.validate_user(username, password):
            return "cashier"
            
        return None

