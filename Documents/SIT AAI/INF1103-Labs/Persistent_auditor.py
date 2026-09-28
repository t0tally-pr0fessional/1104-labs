print("Inventory system")

failedEntires = 0
unitsProcessed = 0
INVENTORY_FILE = "inventory.txt"

def load_inventory():
    orders = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            for line in file.read().splitlines():
                if line.strip() == "":
                    continue
                order_id, name, quantity = [part.strip() for part in line.split(",")]
                orders.append((int(order_id), name, int(quantity)))
    except FileNotFoundError:
        pass
    return orders

def save_inventory(orders):
    with open(INVENTORY_FILE, "w") as file:
        for order_id, name, quantity in orders:
            file.write(str(order_id) + ", " + name + ", " + str(quantity) + "\n")

def get_valid_input():
    itemInput = input("Enter product name(type 'quit' to end): ").strip()
    

    if str(itemInput).lower() =="quit":
         return "quit"
    elif itemInput == "":
         print("Please input a valid name")
         return None
    
    userInput = input("Enter delivery ammount: ")
    if userInput.lstrip("-").isdigit() == False:
            print("Please input a valid number not text.")
            return None
    if int(userInput) > 500:
         print("Please input a valid number not text.")
         return None
    if int(userInput) <0:
            print("Please input a positive number")
            return None
    new_value = int(userInput)      
    return itemInput, new_value

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.1

def generate_report(total_units, failed_attempts):
    print("Thank you for inputing inventory")
    print("total units processed: " + str(total_units))
    print("total failed/rejected entries: " + str(failed_attempts))

def print_orders(orders):
    print("Current Orders:")
    print()
    for order_id, name, quantity in orders:
        print(str(order_id) + ", " + name + ", " + str(quantity))
    print()

orders = load_inventory()
totalInventory= 0
for order in orders:
    totalInventory = process_delivery(totalInventory, order[2])

print_orders(orders)

while True:
    userInput = get_valid_input()

    if userInput == "quit":
         save_inventory(orders)
         generate_report(totalInventory, failedEntires)
         break

    if userInput is None:
         failedEntires += 1
         continue

    name, quantity = userInput
    if len(orders) > 0:
            order_id = orders[-1][0] + 1
    else:
            order_id = 1001
    orders.append((order_id, name, quantity))
    totalInventory = process_delivery(totalInventory, quantity)

    tax = calculate_tax(quantity)
    print("New total inventory: " + str(totalInventory))
    print("Tax for this delivery: " + str(tax))
    
    print()
    print("New Order Added:")
    print(str(order_id) + "," + name + "," + str(quantity))
    print("Tax for this order: " + str(calculate_tax(quantity)))
    print()
    continue
    