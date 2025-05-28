from view.login_view import LoginView

def main():
    """
    Smart Mart - A Point of Sale System
    
    Features:
    1. Admin Panel
        - Manage products in 5 categories
        - Manage cashier accounts
        - View product stock
        
    2. Cashier Panel
        - Browse and add products to cart
        - Process payments (Cash/Card)
        - Generate bills
        
    Default Admin Credentials:
    Username: admin
    Password: admin123
    """
    LoginView()

if __name__ == "__main__":
    main()
