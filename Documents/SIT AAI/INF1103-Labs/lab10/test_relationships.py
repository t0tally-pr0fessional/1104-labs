from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

passed = 0
failed = 0


def check(description: str, condition: bool) -> None:
    global passed, failed
    if condition:
        passed += 1
        print("  [PASS] " + description)
    else:
        failed += 1
        print("  [FAIL] " + description)


def print_heading(title: str) -> None:
    print()
    print("================================================")
    print(title)
    print("================================================")


def test_association() -> None:
    print_heading("SECTION 2: ASSOCIATION (Supplier - Product)")
    supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.0)
    antivirus = DigitalProduct("D001", "Antivirus", 49.9, 100, supplier, 850.5)

    print("Supplier information through each Product:")
    for product in [laptop, antivirus]:
        print(product.get_name() + " ->", end=" ")
        product.get_supplier().display_information()

    check("Both products refer to the same Supplier object",
          laptop.get_supplier() is supplier and antivirus.get_supplier() is supplier)
    check("Supplier and Product are separate objects", laptop is not supplier)

    print()
    print("PREDICT FIRST: del supplier, then display supplier through each Product")
    del supplier
    for product in [laptop, antivirus]:
        print(product.get_name() + " ->", end=" ")
        product.get_supplier().display_information()
    check("Products still reach their Supplier after 'del supplier'",
          laptop.get_supplier().get_name() == "TechCorp")


def test_aggregation() -> None:
    print_heading("SECTION 3: AGGREGATION (Inventory - Product)")
    supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")
    monitor = PhysicalProduct("P010", "Monitor", 199.0, 10, supplier, 4.5)
    print("Product created before any Inventory exists:")
    monitor.display_information()

    inventory_a = Inventory()
    inventory_b = Inventory()
    check("Product added to Inventory A", inventory_a.add_product(monitor))
    check("Inventory A finds the same Product object",
          inventory_a.find_product("P010") is monitor)

    print()
    print("PREDICT FIRST: does the Product still work after removal from Inventory A?")
    check("Product removed from Inventory A", inventory_a.remove_product("P010"))
    check("Inventory A no longer contains the Product",
          inventory_a.find_product("P010") is None)
    monitor.display_information()
    check("Product can still be used (update_stock to 7)",
          monitor.update_stock(7) and monitor.get_stock() == 7)

    check("Same Product object added to Inventory B", inventory_b.add_product(monitor))
    check("Inventory B holds the same object", inventory_b.find_product("P010") is monitor)

    inventory_b.remove_product("P010")
    inventory_b.display_all()
    check("Emptying Inventory B does not destroy the Product",
          monitor.get_name() == "Monitor")


def test_composition() -> None:
    print_heading("SECTION 4: COMPOSITION (Order - OrderLine)")
    supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.0)
    mouse = PhysicalProduct("P002", "Mouse", 25.5, 40, supplier, 0.1)
    antivirus = DigitalProduct("D001", "Antivirus", 49.9, 100, supplier, 850.5)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 2)
    order_1.add_order_line(mouse, 3)
    order_1.add_order_line(antivirus, 1)
    order_1.display_order()
    check("Order total is calculated from its OrderLines (2526.40)",
          round(order_1.calculate_total(), 2) == 2526.40)

    print()
    print("PREDICT FIRST: same Product in two Orders - how many OrderLines and Products?")
    order_2 = Order("O002")
    order_2.add_order_line(laptop, 1)
    order_2.display_order()
    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print("id(OrderLine in O001) = " + str(id(line_1)))
    print("id(OrderLine in O002) = " + str(id(line_2)))
    print("id(Product in O001)   = " + str(id(line_1.get_product())))
    print("id(Product in O002)   = " + str(id(line_2.get_product())))
    check("Each Order created its own OrderLine (2 OrderLine objects)", line_1 is not line_2)
    check("Both OrderLines refer to the same Product (1 Product object)",
          line_1.get_product() is line_2.get_product() is laptop)

    print()
    print("Removing the Mouse line through an Order method:")
    check("Order removes its own OrderLine", order_1.remove_order_line("P002"))
    order_1.display_order()
    check("Changing the copy from get_order_lines() does not change the Order",
          len(order_1.get_order_lines()) == 2)

    print()
    print("Removing Order O002 from the scenario:")
    del order_2
    laptop.display_information()
    check("Product still exists after its Order is removed", laptop.get_name() == "Laptop")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp() -> None:
    print_heading("SECTION 6: LISKOV SUBSTITUTION PRINCIPLE")
    supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")
    products: list[Product] = [
        PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.0),
        DigitalProduct("D001", "Antivirus", 49.9, 100, supplier, 850.5),
    ]

    print("show_product_details() called with each subclass:")
    for product in products:
        show_product_details(product)
        print()

    print("Expectation from Product: update_stock() accepts quantities >= 0 "
          "and rejects negatives")
    for product in products:
        name = type(product).__name__
        check(name + ".update_stock(20) returns True and sets stock",
              product.update_stock(20) is True and product.get_stock() == 20)
        check(name + ".update_stock(0) is accepted",
              product.update_stock(0) is True and product.get_stock() == 0)
        check(name + ".update_stock(-5) returns False and keeps stock",
              product.update_stock(-5) is False and product.get_stock() == 0)

    inventory = Inventory()
    for product in products:
        check(type(product).__name__ + " added to Inventory", inventory.add_product(product))
    check("Inventory finds both product types",
          inventory.find_product("P001") is products[0]
          and inventory.find_product("D001") is products[1])
    inventory.display_all()


def test_polymorphism() -> None:
    print_heading("SECTION 7: POLYMORPHISM")
    supplier = Supplier("S001", "TechCorp", "sales@techcorp.com")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.0))
    inventory.add_product(DigitalProduct("D001", "Antivirus", 49.9, 100, supplier, 850.5))

    print("PREDICT FIRST: get_fulfilment_info() for each product")
    print("One loop over the Product collection, no isinstance():")
    results = []
    for product in inventory.get_products():
        product.display_information()
        info = product.get_fulfilment_info()
        print(info)
        print()
        results.append(info)
    check("PhysicalProduct used its own get_fulfilment_info()",
          results[0] == "This product requires physical shipping.")
    check("DigitalProduct used its own get_fulfilment_info()",
          results[1] == "This product is delivered digitally.")


test_association()
test_aggregation()
test_composition()
test_lsp()
test_polymorphism()

print_heading("RESULTS: " + str(passed) + " passed, " + str(failed) + " failed")
