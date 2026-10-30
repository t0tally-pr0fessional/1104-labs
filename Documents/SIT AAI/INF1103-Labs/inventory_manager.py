import json
import os

from inventory import Inventory
from product import Product

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")
print()

INVENTORY_FILE = "inventory.json"


def load_inventory():
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        print(INVENTORY_FILE + " found.")
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
            for item in data.get("products", []):
                inventory.add_product(Product(item["id"], item["name"], item["price"], item["stock"]))
            print("Inventory loaded successfully.")
            return inventory, data.get("history", [])
        except (json.JSONDecodeError, AttributeError, KeyError, TypeError):
            print(INVENTORY_FILE + " is corrupted. Starting with an empty inventory.")
            return Inventory(), []
    print(INVENTORY_FILE + " not found. Starting with an empty inventory.")
    return inventory, []


def save_inventory(inventory, transactions):
    products = []
    for product in inventory.get_products():
        products.append({"id": product.get_product_id(), "name": product.get_name(),
                         "price": product.get_price(), "stock": product.get_stock()})
    with open(INVENTORY_FILE, "w") as file:
        json.dump({"products": products, "history": transactions}, file, indent=4)


def get_number(prompt, number_type):
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


def add_product(inventory, transactions):
    print()
    print("Add New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Please input a valid ID")
        return
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return
    name = input("Product Name: ").strip()
    if name == "":
        print("Please input a valid name")
        return
    price = get_number("Price: ", float)
    stock = get_number("Stock Quantity: ", int)

    inventory.add_product(Product(product_id, name, price, stock))
    transactions.append({"type": "add", "id": product_id, "amount": stock})
    print()
    print("Product added successfully!")


def update_stock(inventory, transactions):
    print()
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
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


def search_product(inventory):
    print()
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    print()
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("------------------------------------------------")
    print("ID: " + product.get_product_id())
    print("Name: " + product.get_name())
    print("Price: $" + format(product.get_price(), ".2f"))
    print("Stock: " + str(product.get_stock()))
    print("------------------------------------------------")


def print_menu():
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# inventory is an Inventory object holding Product objects
# history keeps every transaction amount, not just the running total
inventory, history = load_inventory()
print_menu()

while True:
    print()
    try:
        option = input("Enter option: ").strip()
    except EOFError:
        option = "6"

    if option == "1":
        inventory.display_all()
    elif option == "2":
        add_product(inventory, history)
    elif option == "3":
        update_stock(inventory, history)
    elif option == "4":
        search_product(inventory)
    elif option == "5":
        print()
        print("Saving inventory...")
        save_inventory(inventory, history)
        print("Inventory saved successfully to " + INVENTORY_FILE + ".")
    elif option == "6":
        print()
        print("Saving inventory before exit...")
        save_inventory(inventory, history)
        print("Inventory saved successfully.")
        print()
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break
    else:
        print("Invalid option. Please enter 1-6.")
        print_menu()
