import json
import os

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")
print()

INVENTORY_FILE = "inventory.json"


def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        print(INVENTORY_FILE + " found.")
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
            print("Inventory loaded successfully.")
            return data.get("products", []), data.get("history", [])
        except (json.JSONDecodeError, AttributeError):
            print(INVENTORY_FILE + " is corrupted. Starting with an empty inventory.")
            return [], []
    print(INVENTORY_FILE + " not found. Starting with an empty inventory.")
    return [], []


def find_product(products, product_id):
    for product in products:
        if product["id"].lower() == product_id.lower():
            return product
    return None


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


def display_all(products):
    print()
    print("Current Inventory")
    print("------------------------------------------------")
    if len(products) == 0:
        print("Inventory is empty.")
    for product in products:
        print("ID: " + product["id"] + " | Name: " + product["name"]
              + " | Price: $" + format(product["price"], ".2f")
              + " | Stock: " + str(product["stock"]))
    print("------------------------------------------------")


def add_product(products, transactions):
    print()
    print("Add New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Please input a valid ID")
        return
    if find_product(products, product_id) is not None:
        print("Product ID already exists.")
        return
    name = input("Product Name: ").strip()
    if name == "":
        print("Please input a valid name")
        return
    price = get_number("Price: ", float)
    stock = get_number("Stock Quantity: ", int)

    products.append({"id": product_id, "name": name, "price": price, "stock": stock})
    transactions.append({"type": "add", "id": product_id, "amount": stock})
    print()
    print("Product added successfully!")


def update_stock(products, transactions):
    print()
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(products, product_id)
    if product is None:
        print()
        print("Product not found.")
        return

    print()
    print("Product Found:")
    print("Name: " + product["name"])
    print("Current Stock: " + str(product["stock"]))
    print()
    new_stock = get_number("New Stock Quantity: ", int)

    transactions.append({"type": "update", "id": product["id"],
                         "amount": new_stock - product["stock"]})
    product["stock"] = new_stock
    print()
    print("Stock updated successfully!")


def search_product(products):
    print()
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(products, product_id)
    print()
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("------------------------------------------------")
    print("ID: " + product["id"])
    print("Name: " + product["name"])
    print("Price: $" + format(product["price"], ".2f"))
    print("Stock: " + str(product["stock"]))
    print("------------------------------------------------")


def print_menu():
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("6. Exit")
    print("----------------------------")


# Each product is a dictionary, all products are stored in a list
# history keeps every transaction amount, not just the running total
inventory, history = load_inventory()
print_menu()

while True:
    print()
    option = input("Enter option: ").strip()

    if option == "1":
        display_all(inventory)
    elif option == "2":
        add_product(inventory, history)
    elif option == "3":
        update_stock(inventory, history)
    elif option == "4":
        search_product(inventory)
    elif option == "6":
        print()
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break
    else:
        print("Invalid option. Please enter 1-4 or 6.")
        print_menu()
