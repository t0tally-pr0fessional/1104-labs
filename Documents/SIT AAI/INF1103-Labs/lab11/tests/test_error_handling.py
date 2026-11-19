import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from input_helpers import get_positive_float
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

PRODUCTS_CSV = os.path.join(os.path.dirname(__file__), "..", "products.csv")


class TestGetPositiveFloat(unittest.TestCase):
    def test_reasks_until_valid_number(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        lines = output.getvalue().splitlines()
        self.assertEqual(lines, ["Please enter a valid number, e.g. 12.50",
                                 "Please enter a number greater than zero."])


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")

    def load(self, path: str) -> str:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        output = self.load(PRODUCTS_CSV)
        loaded_ids = [product.get_product_id() for product in self.inventory.get_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("could not convert string to float: 'abc'", output)
        self.assertIn("3 products loaded.", output)

    def test_missing_file_handled_gracefully(self):
        output = self.load("does_not_exist.csv")
        self.assertIn("Products file not found: does_not_exist.csv", output)
        self.assertEqual(len(self.inventory.get_products()), 0)

    def test_finally_always_runs(self):
        self.assertTrue(self.load(PRODUCTS_CSV).strip().endswith("Load attempt finished."))
        self.assertTrue(self.load("does_not_exist.csv").strip().endswith("Load attempt finished."))

    def test_invalid_price_and_duplicate_rows_skipped(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as file:
            file.write("product_type,product_id,name,price,stock_quantity\n"
                       "physical,P1,Lamp,10,1\n"
                       "physical,P1,Lamp Copy,10,1\n"
                       "digital,D1,Editor,0,1\n")
        try:
            output = self.load(file.name)
        finally:
            os.remove(file.name)
        self.assertEqual(len(self.inventory.get_products()), 1)
        self.assertIn("duplicate product ID P1", output)
        self.assertIn("Price must be greater than zero.", output)


if __name__ == "__main__":
    unittest.main()
