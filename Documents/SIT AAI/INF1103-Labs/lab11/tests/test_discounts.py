import inspect
import unittest

from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class FreeShippingWeek(DiscountStrategy):
    # Defined only in the test, to prove a new strategy works without changing Order
    def apply(self, total: float) -> float:
        return total - 1


class TestDiscountStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_at_or_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(250), 237.5)

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


class TestOrderUsesStrategy(unittest.TestCase):
    def setUp(self):
        supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")
        chair = ProductFactory.create("physical", "P001", "Chair", 125.0, 10, supplier, 5.0)
        self.order = Order("O001")
        self.order.add_order_line(chair, 2)  # subtotal 250

    def test_default_is_no_discount(self):
        self.assertIsInstance(self.order.get_discount(), NoDiscount)
        self.assertEqual(self.order.calculate_total(), 250)

    def test_set_discount_changes_strategy_on_existing_order(self):
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(self.order.calculate_total(), 230)
        self.order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(self.order.calculate_total(), 225)

    def test_new_strategy_works_without_changing_order(self):
        self.order.set_discount(FreeShippingWeek())
        self.assertEqual(self.order.calculate_total(), 249)

    def test_calculate_total_has_no_discount_if_elif(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if ", source)
        self.assertNotIn("elif", source)


if __name__ == "__main__":
    unittest.main()
