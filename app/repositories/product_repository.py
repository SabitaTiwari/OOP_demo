from app.models.product import Product
from app.repositories.base import ProductRepository


class InMemoryProductRepository(ProductRepository):

    def __init__(self):
        self.__products: dict[str, Product] = {}
        self.__seed_products()

    def __seed_products(self) -> None:
        laptop = Product(
            name="Laptop",
            description="Development laptop for backend work",
            _price=1200.0,
            _stock=5,
        )

        keyboard = Product(
            name="Keyboard",
            description="Mechanical keyboard",
            _price=80.0,
            _stock=20,
        )

        self.__products[laptop.id] = laptop
        self.__products[keyboard.id] = keyboard

    def get_all(self) -> list[Product]:
        return list(self.__products.values())

    def get_by_id(self, product_id: str) -> Product | None:
        return self.__products.get(product_id)

    def create(self, product: Product) -> Product:
        self.__products[product.id] = product
        return product

    def update(self, product: Product) -> Product:
        self.__products[product.id] = product
        return product

    def delete(self, product_id: str) -> bool:
        if product_id not in self.__products:
            return False

        del self.__products[product_id]
        return True