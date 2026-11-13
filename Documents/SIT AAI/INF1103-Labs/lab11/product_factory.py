from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    # The only place that knows which concrete Product class to build.
    # Adding a new product type means changing this method (a known OCP trade-off).
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, size: float = 0.0) -> Product:
        # size is the weight in kg for physical products, or the download size in MB for digital
        product_type = product_type.strip().lower()
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, size)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, size)
        else:
            raise ValueError("Unknown product type: " + product_type)
