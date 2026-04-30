from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=300)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
   
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=5, max_length=300)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class ProductRead(BaseModel):

    id: str
    name: str
    description: str
    price: float
    stock: int


class PurchaseRequest(BaseModel):
    quantity: int = Field(..., gt=0)


class DiscountRequest(BaseModel):
    percentage: float = Field(..., gt=0, lt=100)


class MessageResponse(BaseModel):
    message: str