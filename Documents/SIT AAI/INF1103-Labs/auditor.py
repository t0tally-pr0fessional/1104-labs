print("Inventory system")
totalInventory= 0
failedEntires = 0
unitsProcessed = 0

while True:
    userInput = input("Enter delivery ammount(type 'quit' to end): ")

    if userInput == "quit":
        print("Thank you for inputing inventory")
        print("total units processed: " + str(totalInventory))
        print("total failed/rejected entries: " + str(failedEntires))
        break

    if userInput.lstrip("-").isdigit() == False:
        print("Please input a valid number not text.")
        failedEntires += 1
        continue
    else: 
        pass
    Inventory = int(userInput)
    if Inventory <0:
        print("Please input a positive number")
        failedEntires += 1
    else:
        totalInventory = totalInventory + Inventory
        print("New total inventory: " + str(totalInventory))
        if totalInventory > 500:
            print("WARNING: INVENTORY HAS EXCEEDED 500 UNITS")
            break
        elif totalInventory <= 500:
            pass
        continue
        