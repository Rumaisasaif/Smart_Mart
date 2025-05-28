import tkinter as tk
from tkinter import ttk, messagebox
from controller.main_controller import MainController
from view.theme_manager import ThemeManager
import os

class CashierView:
    def __init__(self, username):
        self.controller = MainController()
        self.username = username
        self.cart = []  # List of tuples (name, price, quantity)
        
        self.root = tk.Tk()
        self.root.title(f"Smart Mart - Cashier Panel ({username})")
        self.root.geometry("1200x800")
        
        # Apply theme
        ThemeManager.apply_theme()
        ThemeManager.configure_window(self.root)
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Header
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill="x")
        
        title_label = ttk.Label(header_frame, text="CASHIER PANEL", style="Title.TLabel")
        title_label.pack(side="left")
        
        cashier_label = ttk.Label(header_frame, text=f"Logged in as: {username}", style="Subtitle.TLabel")
        cashier_label.pack(side="right")

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Left frame for product selection
        left_frame = ttk.LabelFrame(main_frame, text="Add Products", padding="20")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Category selection
        ttk.Label(left_frame, text="Category:").pack(anchor="w", pady=(0, 5))
        self.category_var = tk.StringVar()
        categories = ["Electronics", "Groceries", "Clothing", "Books", "Beauty"]
        self.category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, values=categories, state="readonly")
        self.category_combo.pack(fill="x", pady=(0, 15))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_select)

        # Product selection
        ttk.Label(left_frame, text="Product:").pack(anchor="w", pady=(0, 5))
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(left_frame, textvariable=self.product_var, state="readonly")
        self.product_combo.pack(fill="x", pady=(0, 15))

        # Quantity
        ttk.Label(left_frame, text="Quantity:").pack(anchor="w", pady=(0, 5))
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = ttk.Entry(left_frame, textvariable=self.quantity_var)
        self.quantity_entry.pack(fill="x", pady=(0, 15))

        # Add to cart button
        ttk.Button(left_frame, text="Add to Cart", command=self.add_to_cart, style="Success.TButton").pack(fill="x", pady=20)

        # Right frame for cart and payment
        right_frame = ttk.LabelFrame(main_frame, text="Cart", padding="20")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Cart display
        self.cart_text = tk.Text(right_frame, height=15, width=50)
        self.cart_text.pack(pady=10, fill="both", expand=True)

        # Payment method
        payment_frame = ttk.LabelFrame(right_frame, text="Payment Method", padding=10)
        payment_frame.pack(pady=10, fill="x")
        
        self.payment_var = tk.StringVar(value="Cash")
        ttk.Radiobutton(payment_frame, text="Cash", variable=self.payment_var, value="Cash").pack(side="left", padx=20)
        ttk.Radiobutton(payment_frame, text="Card (10% discount)", variable=self.payment_var, value="Card").pack(side="left", padx=20)

        # Process payment button
        ttk.Button(right_frame, text="Process Payment", command=self.process_payment, style="Success.TButton").pack(fill="x", pady=10)

        # Initialize product list
        self.products_by_category = {}
        self.update_cart_display()

        self.root.mainloop()

    def on_category_select(self, event=None):
        category = self.category_var.get()
        if category:
            products = self.controller.get_products_by_category(category)
            self.products_by_category[category] = products
            self.product_combo['values'] = [p[0] for p in products]  # p[0] is the product name
            self.product_combo.set('')  # Clear current selection

    def add_to_cart(self):
        category = self.category_var.get()
        product_name = self.product_var.get()
        
        if not category or not product_name:
            messagebox.showerror("Error", "Please select both category and product")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            # Add to cart using controller
            item = self.controller.add_to_cart(category, product_name, quantity)
            self.cart.append(item)
            self.update_cart_display()
            
            # Clear selections
            self.product_var.set('')
            self.quantity_var.set('1')
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_cart_display(self):
        self.cart_text.delete('1.0', tk.END)
        
        if not self.cart:
            self.cart_text.insert(tk.END, "Cart is empty\n")
            return
            
        # Display cart items
        self.cart_text.insert(tk.END, f"{'Product':<30}{'Price':>10}{'Qty':>8}{'Total':>12}\n")
        self.cart_text.insert(tk.END, "-" * 60 + "\n")
        
        total = 0
        for name, price, qty in self.cart:
            item_total = price * qty
            total += item_total
            self.cart_text.insert(tk.END, f"{name:<30}${price:>9.2f}{qty:>8}${item_total:>11.2f}\n")
            
        self.cart_text.insert(tk.END, "\n" + "-" * 60 + "\n")
        
        # Apply discount if card payment
        if self.payment_var.get() == "Card":
            discount = total * 0.10
            self.cart_text.insert(tk.END, f"{'Subtotal:':<30}${total:>31.2f}\n")
            self.cart_text.insert(tk.END, f"{'Discount (10%):':<30}${discount:>31.2f}\n")
            total -= discount
            
        self.cart_text.insert(tk.END, f"{'Total:':<30}${total:>31.2f}\n")

    def process_payment(self):
        if not self.cart:
            messagebox.showinfo("Info", "Cart is empty")
            return

        total = self.controller.calculate_total(self.cart)
        
        # Apply discount for card payment
        if self.payment_var.get() == "Card":
            total = total * 0.9  # 10% discount

        try:
            # Reduce stock for all items
            for name, _, qty in self.cart:
                category = None
                # Find the category for the product
                for cat, products in self.products_by_category.items():
                    if any(p[0] == name for p in products):
                        category = cat
                        break
                        
                if category:
                    self.controller.reduce_stock(category, name, qty)

            # Save the bill
            self.controller.save_bill(total)
            
            messagebox.showinfo("Success", 
                              f"Payment processed successfully!\n\n"
                              f"Payment Method: {self.payment_var.get()}\n"
                              f"Total Amount: ${total:.2f}")
            
            # Clear cart
            self.cart = []
            self.update_cart_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process payment: {str(e)}")

if __name__ == "__main__":
    CashierView("test_cashier")
