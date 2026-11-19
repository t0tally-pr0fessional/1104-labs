import unittest

from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class TestProductValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Lamp", 0, 10, self.supplier)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", -5, 10, self.supplier)

    def test_negative_stock_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Lamp", 25.0, -1, self.supplier)

    def test_zero_stock_allowed(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 0, self.supplier)
        self.assertEqual(product.get_stock(), 0)


class TestOrderLineValidation(unittest.TestCase):
    def setUp(self):
        supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")
        self.product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, supplier)
        self.order = Order("O001")

    def test_zero_quantity_rejected(self):
        with self.assertRaises(ValueError):
            self.order.add_order_line(self.product, 0)

    def test_negative_quantity_rejected(self):
        with self.assertRaises(ValueError):
            self.order.add_order_line(self.product, -2)

    def test_rejected_line_is_not_added(self):
        with self.assertRaises(ValueError):
            self.order.add_order_line(self.product, 0)
        self.assertEqual(len(self.order.get_order_lines()), 0)


if __name__ == "__main__":
    unittest.main()
