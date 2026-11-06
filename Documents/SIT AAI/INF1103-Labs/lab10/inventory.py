from product import Product


class Inventory:
    def __init__(self):
        # Aggregation: products are created elsewhere and only referenced here
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        # Removes the reference only; the Product object itself still exists
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def display_all(self) -> None:
        print()
        print("Current Inventory")
        print("------------------------------------------------")
        if len(self.__products) == 0:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("------------------------------------------------")

    def get_products(self) -> list[Product]:
        return self.__products
