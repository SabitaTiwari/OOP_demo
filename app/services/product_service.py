from app.models.product import Product
from app.repositories.base import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductNotFoundError(Exception):
    """Custom exception for product not found."""


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self) -> list[Product]:
        return self.repository.get_all()

    def get_product(self, product_id: str) -> Product:
        product = self.repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError("Product not found")

        return product

    def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            _price=product_data.price,
            _stock=product_data.stock,
        )

        return self.repository.create(product)

    def update_product(self, product_id: str, product_data: ProductUpdate) -> Product:
        product = self.get_product(product_id)

        if product_data.name is not None:
            product.name = product_data.name

        if product_data.description is not None:
            product.description = product_data.description

        if product_data.price is not None:
            product.price = product_data.price

        if product_data.stock is not None:
            product.stock = product_data.stock

        return self.repository.update(product)

    def delete_product(self, product_id: str) -> None:
        product_exists = self.repository.delete(product_id)

        if not product_exists:
            raise ProductNotFoundError("Product not found")

    def purchase_product(self, product_id: str, quantity: int) -> Product:
        product = self.get_product(product_id)
        product.reduce_stock(quantity)
        return self.repository.update(product)

    def apply_discount(self, product_id: str, percentage: float) -> Product:
        product = self.get_product(product_id)
        product.apply_discount(percentage)
        return self.repository.update(product)