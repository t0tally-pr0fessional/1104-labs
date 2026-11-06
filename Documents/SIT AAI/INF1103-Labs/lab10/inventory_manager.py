import json
import os

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")
print()

INVENTORY_FILE = "inventory.json"
BACKUP_FILE = "inventory_corrupted.json"
DEFAULT_SUPPLIER_ID = "S000"


def default_suppliers() -> dict[str, Supplier]:
    # Products saved before suppliers existed are linked to this placeholder
    return {DEFAULT_SUPPLIER_ID: Supplier(DEFAULT_SUPPLIER_ID, "Unknown Supplier", "N/A")}


def create_product(item: dict, suppliers: dict[str, Supplier]) -> Product:
    supplier = suppliers.get(item.get("supplier_id", DEFAULT_SUPPLIER_ID), suppliers[DEFAULT_SUPPLIER_ID])
    if item["type"] == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"], item["stock"],
                               supplier, item["weight"])
    if item["type"] == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"], item["stock"],
                              supplier, item["download_size"])
    raise ValueError("Unknown product type: " + str(item["type"]))


def load_inventory() -> tuple[Inventory, list[dict], dict[str, Supplier]]:
    inventory = Inventory()
    suppliers = default_suppliers()
    if os.path.exists(INVENTORY_FILE):
        print(INVENTORY_FILE + " found.")
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
            for item in data.get("suppliers", []):
                suppliers[item["id"]] = Supplier(item["id"], item["name"], item["email"])
            for item in data.get("products", []):
                inventory.add_product(create_product(item, suppliers))
            print("Inventory loaded successfully.")
            return inventory, data.get("history", []), suppliers
        except (ValueError, AttributeError, KeyError, TypeError):
            # Keep the unreadable file so saving an empty inventory cannot destroy it
            os.replace(INVENTORY_FILE, BACKUP_FILE)
            print(INVENTORY_FILE + " is corrupted. It was moved to " + BACKUP_FILE + ".")
            print("Starting with an empty inventory.")
            return Inventory(), [], default_suppliers()
    print(INVENTORY_FILE + " not found. Starting with an empty inventory.")
    return inventory, [], suppliers


def save_inventory(inventory: Inventory, transactions: list[dict],
                   suppliers: dict[str, Supplier]) -> None:
    products = []
    for product in inventory.get_products():
        products.append(product.to_dict())
    supplier_list = []
    for supplier in suppliers.values():
        supplier_list.append(supplier.to_dict())
    with open(INVENTORY_FILE, "w") as file:
        json.dump({"suppliers": supplier_list, "products": products,
                   "history": transactions}, file, indent=4)


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    print()
    print("Suppliers:")
    for supplier in suppliers.values():
        supplier.display_information()
    supplier_id = input("Supplier ID (enter a new ID to add a supplier): ").strip().upper()
    if supplier_id == "":
        print("Please input a valid supplier ID")
        return None
    if supplier_id in suppliers:
        return suppliers[supplier_id]

    name = input("New Supplier Name: ").strip()
    email = input("New Supplier Email: ").strip()
    if name == "" or email == "":
        print("Please input a valid supplier name and email")
        return None
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    return supplier


def get_number(prompt: str, number_type: type) -> int | float:
    while True:
        userInput = input(prompt).strip()
        try:
            value = number_type(userInput)
        except ValueError:
            print("Please input a valid number not text.")
            continue
        if value < 0:
            print("Please input a positive number")
            continue
        return value


def add_product(inventory: Inventory, transactions: list[dict],
                suppliers: dict[str, Supplier]) -> None:
    print()
    print("Add New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Please input a valid ID")
        return
    if inventory.find_product(product_id) is not None:
        print("Product ID already exists.")
        return
    product_type = input("Product Type (physical/digital): ").strip().lower()
    if product_type != "physical" and product_type != "digital":
        print("Please input physical or digital")
        return
    name = input("Product Name: ").strip()
    if name == "":
        print("Please input a valid name")
        return
    price = get_number("Price: ", float)
    stock = get_number("Stock Quantity: ", int)
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    if product_type == "physical":
        weight = get_number("Weight (kg): ", float)
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = get_number("Download Size (MB): ", float)
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(product)
    transactions.append({"type": "add", "id": product_id, "amount": stock})
    print()
    print("Product added successfully!")


def update_stock(inventory: Inventory, transactions: list[dict]) -> None:
    print()
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print()
        print("Product not found.")
        return

    print()
    print("Product Found:")
    print("Name: " + product.get_name())
    print("Current Stock: " + str(product.get_stock()))
    print()
    new_stock = get_number("New Stock Quantity: ", int)

    transactions.append({"type": "update", "id": product.get_product_id(),
                         "amount": new_stock - product.get_stock()})
    product.update_stock(new_stock)
    print()
    print("Stock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print()
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    print()
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("------------------------------------------------")
    product.display_information()
    product.get_supplier().display_information()
    print("Fulfilment: " + product.get_fulfilment_info())
    if isinstance(product, CanBeShipped):
        print("Shipping Cost: $" + format(product.calculate_shipping_cost(), ".2f"))
    print("------------------------------------------------")


def create_order(inventory: Inventory, orders: list[Order]) -> None:
    print()
    print("Create Order")
    order = Order("O" + format(len(orders) + 1, "03d"))
    while True:
        product_id = input("Product ID (leave blank to finish): ").strip()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_number("Quantity: ", int)
        if not order.add_order_line(product, quantity):
            print("Quantity must be at least 1.")

    print()
    if len(order.get_order_lines()) == 0:
        print("No products added. Order cancelled.")
        return
    orders.append(order)
    order.display_order()


def print_menu() -> None:
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Create Order")
    print("6. Save Inventory")
    print("7. Exit")
    print("----------------------------")


# inventory is an Inventory object holding PhysicalProduct and DigitalProduct objects
# history keeps every transaction amount, not just the running total
# suppliers maps supplier ID to the Supplier object that products refer to
# orders only last for the current session and are not saved
inventory, history, suppliers = load_inventory()
orders: list[Order] = []
print_menu()

while True:
    print()
    try:
        option = input("Enter option: ").strip()
    except EOFError:
        option = "7"

    if option == "1":
        inventory.display_all()
    elif option == "2":
        add_product(inventory, history, suppliers)
    elif option == "3":
        update_stock(inventory, history)
    elif option == "4":
        search_product(inventory)
    elif option == "5":
        create_order(inventory, orders)
    elif option == "6":
        print()
        print("Saving inventory...")
        save_inventory(inventory, history, suppliers)
        print("Inventory saved successfully to " + INVENTORY_FILE + ".")
    elif option == "7":
        print()
        print("Saving inventory before exit...")
        save_inventory(inventory, history, suppliers)
        print("Inventory saved successfully.")
        print()
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break
    else:
        print("Invalid option. Please enter 1-7.")
        print_menu()
