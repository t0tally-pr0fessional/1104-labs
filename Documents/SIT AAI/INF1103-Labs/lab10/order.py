from product import Product


class OrderLine:
    # Only Order creates OrderLine objects; a line belongs to exactly one Order
    def __init__(self, product: Product, quantity: int):
        # Association: the line refers to the Product but does not own it
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(self.__product.get_product_id() + " | " + self.__product.get_name()
              + " | Qty: " + str(self.__quantity)
              + " x $" + format(self.__product.get_price(), ".2f")
              + " = $" + format(self.calculate_subtotal(), ".2f"))


class Order:
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        # Composition: the Order creates and owns its OrderLine objects
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        # Return a copy so lines cannot be added to or moved from outside the Order
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> bool:
        if quantity <= 0:
            return False
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)
        return True

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().lower() == product_id.lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print("Order " + self.__order_id)
        print("------------------------------------------------")
        if len(self.__order_lines) == 0:
            print("Order is empty.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("------------------------------------------------")
        print("Total: $" + format(self.calculate_total(), ".2f"))
