import csv
import sys

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print("Products file not found: " + path)
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row_number, row in enumerate(reader, start=2):
                # Each row gets its own try so one bad row does not stop the rest
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                except ValueError as error:
                    print("Skipped row " + str(row_number) + ": " + str(error))
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print("Skipped row " + str(row_number) + ": duplicate product ID " + product_id)
        print(str(loaded) + " products loaded.")
    finally:
        print("Load attempt finished.")


if __name__ == "__main__":
    # Run directly to try it: python product_loader.py [path]
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "products.csv"
    demo_inventory = Inventory()
    load_products(csv_path, demo_inventory, Supplier("S001", "TechCorp", "sales@techcorp.com"))
    demo_inventory.display_all()
