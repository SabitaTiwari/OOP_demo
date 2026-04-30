from app.repositories.product_repository import InMemoryProductRepository
from app.services.product_service import ProductService


_product_repository = InMemoryProductRepository()


def get_product_service() -> ProductService:
    return ProductService(repository=_product_repository)