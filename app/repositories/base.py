from abc import ABC, abstractmethod

from app.models.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: str) -> Product | None:
        pass

    @abstractmethod
    def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        pass