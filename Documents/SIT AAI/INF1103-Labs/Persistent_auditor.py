print("Inventory system")
totalInventory= 0
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

def save_inventory():
     return

def get_valid_input():
    itemInput = input("Enter product name(type 'quit' to end): ").strip
    

    if itemInput.lower() =="quit":
         return "quit"
    elif itemInput == "":
         print("Please input a valid name")
         return None
    
    userInput = input("Enter delivery ammount: ")
    if userInput.lstrip("-").isdigit() == False:
            print("Please input a valid number not text.")
            return None
    
    if int(userInput) <0:
            print("Please input a positive number")
            return None
    new_value = int(userInput)      
    return new_value, itemInput

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
for order in orders:
    totalInventory = process_delivery(totalInventory, order[2])

print_orders(orders)

while True:
    userInput = get_valid_input()

    if userInput == "quit":
         generate_report(totalInventory, failedEntires)
         break

    if userInput is None:
         failedEntires += 1
         continue

    tax = calculate_tax(userInput)
    totalInventory = process_delivery(totalInventory,userInput)
    print("New total inventory: " + str(totalInventory))
    print("Tax for this delivery: " + str(tax))

    if totalInventory > 500:
         print("WARNING: INVENTORY HAS EXCEEDED 500 UNITS")
         break
    continue
        