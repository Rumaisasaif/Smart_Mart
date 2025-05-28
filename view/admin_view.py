import tkinter as tk
from tkinter import ttk, messagebox
from controller.main_controller import MainController
from view.theme_manager import ThemeManager

class AdminView:
    def __init__(self):
        self.controller = MainController()
        
        self.root = tk.Tk()
        self.root.title("Smart Mart - Admin Panel")
        self.root.geometry("1000x700")
        
        # Apply theme
        ThemeManager.apply_theme()
        ThemeManager.configure_window(self.root)
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"1000x700+{x}+{y}")
        
        # Header
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill="x")
        
        title_label = ttk.Label(header_frame, text="ADMIN PANEL", style="Title.TLabel")
        title_label.pack(side="left")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Create tabs
        self.products_tab = ttk.Frame(self.notebook, padding=20)
        self.cashiers_tab = ttk.Frame(self.notebook, padding=20)
        
        self.notebook.add(self.products_tab, text='Manage Products')
        self.notebook.add(self.cashiers_tab, text='Manage Cashiers')
        
        self._init_products_tab()
        self._init_cashiers_tab()
        
        self.root.mainloop()
    
    def _init_products_tab(self):
        # Left panel - Product Management
        left_frame = ttk.LabelFrame(self.products_tab, text="Add/Edit Product", padding=20)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Category selection
        ttk.Label(left_frame, text="Category:").pack(anchor="w", pady=(0, 5))
        self.category_var = tk.StringVar()
        categories = ["Electronics", "Groceries", "Clothing", "Books", "Beauty"]
        self.category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, values=categories, state="readonly")
        self.category_combo.pack(fill="x", pady=(0, 15))
        
        # Product details
        ttk.Label(left_frame, text="Product Name:").pack(anchor="w", pady=(0, 5))
        self.product_name = ttk.Entry(left_frame)
        self.product_name.pack(fill="x", pady=(0, 15))
        
        ttk.Label(left_frame, text="Price:").pack(anchor="w", pady=(0, 5))
        self.price = ttk.Entry(left_frame)
        self.price.pack(fill="x", pady=(0, 15))
        
        ttk.Label(left_frame, text="Quantity:").pack(anchor="w", pady=(0, 5))
        self.quantity = ttk.Entry(left_frame)
        self.quantity.pack(fill="x", pady=(0, 15))
        
        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(btn_frame, text="Add Product", command=self.add_product, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Product", command=self.update_product).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Product", command=self.delete_product, style="Warning.TButton").pack(side="left", padx=5)
        
        # Right panel - Product List
        right_frame = ttk.LabelFrame(self.products_tab, text="Product List", padding=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Product list with scrollbar
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill="both", expand=True)
        
        self.product_tree = ttk.Treeview(tree_frame, columns=("Category", "Name", "Price", "Stock"), show="headings", selectmode="browse")
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.product_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.product_tree.xview)
        self.product_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Pack scrollbars
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.product_tree.pack(fill="both", expand=True)
        
        # Configure columns
        self.product_tree.heading("Category", text="Category")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Stock", text="Stock")
        
        self.product_tree.column("Category", width=150)
        self.product_tree.column("Name", width=200)
        self.product_tree.column("Price", width=100)
        self.product_tree.column("Stock", width=100)
        
        # Bind selection event
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        self.refresh_products()
        
    def _init_cashiers_tab(self):
        # Left panel - Cashier Management
        left_frame = ttk.LabelFrame(self.cashiers_tab, text="Add/Edit Cashier", padding=20)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Cashier details
        ttk.Label(left_frame, text="Username:").pack(anchor="w", pady=(0, 5))
        self.cashier_username = ttk.Entry(left_frame)
        self.cashier_username.pack(fill="x", pady=(0, 15))
        
        ttk.Label(left_frame, text="Password:").pack(anchor="w", pady=(0, 5))
        self.cashier_password = ttk.Entry(left_frame, show="•")
        self.cashier_password.pack(fill="x", pady=(0, 15))
        
        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(btn_frame, text="Add Cashier", command=self.add_cashier, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Cashier", command=self.update_cashier).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Cashier", command=self.delete_cashier, style="Warning.TButton").pack(side="left", padx=5)
        
        # Right panel - Cashier List
        right_frame = ttk.LabelFrame(self.cashiers_tab, text="Cashier List", padding=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Cashier list with scrollbar
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill="both", expand=True)
        
        self.cashier_tree = ttk.Treeview(tree_frame, columns=("Username",), show="headings", selectmode="browse")
        
        # Scrollbar
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.cashier_tree.yview)
        self.cashier_tree.configure(yscrollcommand=y_scroll.set)
        
        # Pack scrollbar
        y_scroll.pack(side="right", fill="y")
        self.cashier_tree.pack(fill="both", expand=True)
        
        # Configure column
        self.cashier_tree.heading("Username", text="Username")
        self.cashier_tree.column("Username", width=200)
        
        # Bind selection event
        self.cashier_tree.bind('<<TreeviewSelect>>', self.on_cashier_select)
        
        self.refresh_cashiers()
    
    def on_product_select(self, event=None):
        selected = self.product_tree.selection()
        if selected:
            values = self.product_tree.item(selected)['values']
            self.category_var.set(values[0])
            self.product_name.delete(0, tk.END)
            self.product_name.insert(0, values[1])
            self.price.delete(0, tk.END)
            self.price.insert(0, values[2].replace('$', ''))
            self.quantity.delete(0, tk.END)
            self.quantity.insert(0, values[3])
    
    def on_cashier_select(self, event=None):
        selected = self.cashier_tree.selection()
        if selected:
            values = self.cashier_tree.item(selected)['values']
            self.cashier_username.delete(0, tk.END)
            self.cashier_username.insert(0, values[0])
            self.cashier_password.delete(0, tk.END)
    
    def refresh_products(self):
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get products from controller and populate
        products = self.controller.get_all_products()
        for category, items in products.items():
            for name, price, qty in items:
                self.product_tree.insert("", "end", values=(category, name, f"${price:.2f}", qty))
    
    def refresh_cashiers(self):
        # Clear existing items
        for item in self.cashier_tree.get_children():
            self.cashier_tree.delete(item)
        
        # Get cashiers from controller and populate
        cashiers = self.controller.get_all_cashiers()
        for username in cashiers:
            self.cashier_tree.insert("", "end", values=(username,))
    
    def add_product(self):
        try:
            category = self.category_var.get()
            name = self.product_name.get().strip()
            price = float(self.price.get())
            quantity = int(self.quantity.get())
            
            if not all([category, name, price > 0, quantity >= 0]):
                messagebox.showerror("Error", "Please fill all fields with valid values")
                return
            
            self.controller.add_product(category, name, price, quantity)
            self.refresh_products()
            messagebox.showinfo("Success", "Product added successfully")
            
            # Clear fields
            self.product_name.delete(0, tk.END)
            self.price.delete(0, tk.END)
            self.quantity.delete(0, tk.END)
            self.category_combo.set('')
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def update_product(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product to update")
            return
            
        try:
            category = self.category_var.get()
            name = self.product_name.get().strip()
            price = float(self.price.get())
            quantity = int(self.quantity.get())
            
            if not all([category, name, price > 0, quantity >= 0]):
                messagebox.showerror("Error", "Please fill all fields with valid values")
                return
            
            self.controller.update_product(category, name, price, quantity)
            self.refresh_products()
            messagebox.showinfo("Success", "Product updated successfully")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def delete_product(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            values = self.product_tree.item(selected)['values']
            category, name = values[0], values[1]
            
            self.controller.delete_product(category, name)
            self.refresh_products()
            messagebox.showinfo("Success", "Product deleted successfully")
    
    def add_cashier(self):
        username = self.cashier_username.get().strip()
        password = self.cashier_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill both username and password")
            return
        
        try:
            self.controller.add_cashier(username, password)
            self.refresh_cashiers()
            messagebox.showinfo("Success", "Cashier added successfully")
            
            # Clear fields
            self.cashier_username.delete(0, tk.END)
            self.cashier_password.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def update_cashier(self):
        selected = self.cashier_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a cashier to update")
            return
        
        username = self.cashier_username.get().strip()
        password = self.cashier_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill both username and password")
            return
        
        try:
            self.controller.update_cashier(username, password)
            self.refresh_cashiers()
            messagebox.showinfo("Success", "Cashier updated successfully")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def delete_cashier(self):
        selected = self.cashier_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a cashier to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this cashier?"):
            username = self.cashier_tree.item(selected)['values'][0]
            
            self.controller.delete_cashier(username)
            self.refresh_cashiers()
            messagebox.showinfo("Success", "Cashier deleted successfully")

if __name__ == "__main__":
    AdminView()
