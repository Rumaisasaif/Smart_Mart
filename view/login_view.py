import tkinter as tk
from tkinter import ttk, messagebox
from controller.main_controller import MainController
from view.admin_view import AdminView
from view.cashier_view import CashierView
from view.theme_manager import ThemeManager

class LoginView:
    def __init__(self):
        self.controller = MainController()
        
        self.root = tk.Tk()
        self.root.title("Smart Mart - Login")
        self.root.geometry("400x500")
        
        # Apply theme
        ThemeManager.apply_theme()
        ThemeManager.configure_window(self.root)
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 500) // 2
        self.root.geometry(f"400x500+{x}+{y}")
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill="both", expand=True)
        
        # Logo/Title section
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 30))
        
        title_label = ttk.Label(title_frame, text="SMART MART", style="Title.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Point of Sale System", style="Subtitle.TLabel")
        subtitle_label.pack()
        
        # Login form
        form_frame = ttk.LabelFrame(main_frame, text="Login", padding=20)
        form_frame.pack(fill="x", pady=20)
        
        # Username
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill="x", pady=5)
        
        ttk.Label(username_frame, text="Username:").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(fill="x")
        
        # Password
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill="x", pady=15)
        
        ttk.Label(password_frame, text="Password:").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(password_frame, show="•")
        self.password_entry.pack(fill="x")
        
        # Login button
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        login_btn = ttk.Button(button_frame, text="LOGIN", command=self.login)
        login_btn.pack(fill="x")
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=20)
        
        footer_text = ttk.Label(footer_frame, 
                              text="© 2024 Smart Mart. All rights reserved.",
                              font=("Helvetica", 8))
        footer_text.pack()
        
        # Set focus to username entry
        self.username_entry.focus()
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        self.root.mainloop()
        
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        try:
            user_type = self.controller.validate_login(username, password)
            
            if user_type == "admin":
                self.root.destroy()
                AdminView()
            elif user_type == "cashier":
                self.root.destroy()
                CashierView(username)
            else:
                messagebox.showerror("Error", "Invalid username or password")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

if __name__ == "__main__":
    LoginView()
