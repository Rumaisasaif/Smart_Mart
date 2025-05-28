import os
import json

class ProductModel:
    PRODUCTS_FILE = "products.txt"

    @classmethod
    def _load_products(cls):
        if not os.path.exists(cls.PRODUCTS_FILE):
            return {}
        try:
            with open(cls.PRODUCTS_FILE, "r") as f:
                return json.loads(f.read() or "{}")
        except:
            return {}

    @classmethod
    def _save_products(cls, products):
        with open(cls.PRODUCTS_FILE, "w") as f:
            json.dump(products, f, indent=2)

    @classmethod
    def add_product(cls, category, name, price, quantity):
        if not category or not name or price <= 0 or quantity < 0:
            raise ValueError("Invalid product data")

        products = cls._load_products()
        
        if category not in products:
            products[category] = []
            
        # Check if product already exists
        for item in products[category]:
            if item[0].lower() == name.lower():
                raise ValueError(f"Product '{name}' already exists in category '{category}'")
                
        products[category].append([name, price, quantity])
        cls._save_products(products)
        return True

    @classmethod
    def update_product(cls, category, name, new_price, new_quantity):
        if not category or not name or new_price <= 0 or new_quantity < 0:
            raise ValueError("Invalid product data")

        products = cls._load_products()
        
        if category not in products:
            raise ValueError(f"Category '{category}' not found")
            
        for item in products[category]:
            if item[0].lower() == name.lower():
                item[1] = new_price
                item[2] = new_quantity
                cls._save_products(products)
                return True
                
        raise ValueError(f"Product '{name}' not found in category '{category}'")

    @classmethod
    def delete_product(cls, category, name):
        products = cls._load_products()
        
        if category not in products:
            raise ValueError(f"Category '{category}' not found")
            
        for i, item in enumerate(products[category]):
            if item[0].lower() == name.lower():
                products[category].pop(i)
                if not products[category]:  # If category is empty
                    del products[category]
                cls._save_products(products)
                return True
                
        raise ValueError(f"Product '{name}' not found in category '{category}'")

    @classmethod
    def get_all_products(cls):
        return cls._load_products()

    @classmethod
    def get_products_by_category(cls, category):
        """Get all products in a category"""
        products = cls.get_all_products()
        if category in products:
            return [tuple(product) for product in products[category]]  # Convert lists to tuples
        return []

    @classmethod
    def get_product(cls, category, name):
        """Get a specific product"""
        products = cls.get_all_products()
        if category in products:
            for product in products[category]:
                if product[0] == name:
                    return tuple(product)  # Convert list to tuple
        return None

    @classmethod
    def reduce_stock(cls, category, name, quantity):
        products = cls._load_products()
        if category in products:
            for item in products[category]:
                if item[0].lower() == name.lower():
                    if item[2] >= quantity:
                        item[2] -= quantity
                        cls._save_products(products)
                        return True
                    else:
                        raise ValueError(f"Insufficient stock for '{name}'")
        raise ValueError(f"Product '{name}' not found in category '{category}'")

    @classmethod
    def get_price(cls, name):
        """Get the price of a product by name"""
        products = cls.get_all_products()
        for category in products.values():
            for product in category:
                if product[0] == name:
                    return product[1]
        raise ValueError(f"Product {name} not found")
