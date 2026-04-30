from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Product:
    name: str
    description: str
    _price: float
    _stock: int
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        self.price = self._price
        self.stock = self._stock

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Product price must be greater than 0")
        self._price = value

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError("Product stock cannot be negative")
        self._stock = value

    def reduce_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if quantity > self.stock:
            raise ValueError("Not enough stock available")

        self.stock -= quantity

    def add_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        self.stock += quantity

    def apply_discount(self, percentage: float) -> None:
       
        if percentage <= 0 or percentage >= 100:
            raise ValueError("Discount percentage must be between 0 and 100")

        discount_amount = self.price * (percentage / 100)
        self.price = self.price - discount_amount

    def to_dict(self) -> dict:
       
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        
        return f"{self.name} - Price: {self.price}, Stock: {self.stock}"