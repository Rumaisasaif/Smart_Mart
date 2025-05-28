from model.product_model import ProductModel

def test_add_and_get_price(tmp_path):
    test_file = tmp_path / "products.txt"
    ProductModel.add_product("Soap", "10.5")
    price = ProductModel.get_price("Soap")
    assert price == 10.5