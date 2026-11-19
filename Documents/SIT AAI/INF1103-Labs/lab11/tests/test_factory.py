import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, self.supplier, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_weight(), 1.2)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100, self.supplier, 300)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 300)

    def test_product_type_ignores_case_and_spaces(self):
        product = ProductFactory.create("  Digital ", "D002", "Game", 59.0, 5, self.supplier)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")


if __name__ == "__main__":
    unittest.main()
