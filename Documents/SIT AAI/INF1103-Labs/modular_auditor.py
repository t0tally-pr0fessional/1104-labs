print("Inventory system")
totalInventory= 0
failedEntires = 0
unitsProcessed = 0

def get_valid_input():
    userInput = input("Enter delivery ammount(type 'quit' to end): ")

    if userInput =="quit":
         return "quit"
    
    if userInput.lstrip("-").isdigit() == False:
            print("Please input a valid number not text.")
            return None
    
    if int(userInput) <0:
            print("Please input a positive number")
            return None
    new_value = int(userInput)      
    return new_value

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.1

def generate_report(total_units, failed_attempts):
    print("Thank you for inputing inventory")
    print("total units processed: " + str(total_units))
    print("total failed/rejected entries: " + str(failed_attempts))

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


    # if userInput == "quit":
    #     print("Thank you for inputing inventory")
    #     print("total units processed: " + str(totalInventory))
    #     print("total failed/rejected entries: " + str(failedEntires))
    #     break

    # if userInput.lstrip("-").isdigit() == False:
    #     print("Please input a valid number not text.")
    #     failedEntires += 1
    #     continue
    # else: 
    #     pass
    # Inventory = int(userInput)
    # if Inventory <0:
    #     print("Please input a positive number")
    #     failedEntires += 1
    # else:
    #     totalInventory = totalInventory + Inventory
    #     print("New total inventory: " + str(totalInventory))
    #     if totalInventory > 500:
    #         print("WARNING: INVENTORY HAS EXCEEDED 500 UNITS")
    #         break
    #     elif totalInventory <= 500:
    #         pass
    #     continue
        