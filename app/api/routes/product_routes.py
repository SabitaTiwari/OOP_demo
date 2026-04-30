from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_product_service
from app.schemas.product_schema import (
    DiscountRequest,
    MessageResponse,
    ProductCreate,
    ProductRead,
    ProductUpdate,
    PurchaseRequest,
)
from app.services.product_service import ProductNotFoundError, ProductService

router = APIRouter(prefix="/products", tags=["Products"])


def product_to_response(product) -> ProductRead:
    return ProductRead(**product.to_dict())


@router.get("", response_model=list[ProductRead])
def list_products(
    service: Annotated[ProductService, Depends(get_product_service)],
):
    products = service.list_products()
    return [product_to_response(product) for product in products]


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: str,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        product = service.get_product(product_id)
        return product_to_response(product)

    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    product = service.create_product(product_data)
    return product_to_response(product)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        product = service.update_product(product_id, product_data)
        return product_to_response(product)

    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product(
    product_id: str,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        service.delete_product(product_id)
        return MessageResponse(message="Product deleted successfully")

    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.post("/{product_id}/purchase", response_model=ProductRead)
def purchase_product(
    product_id: str,
    purchase_data: PurchaseRequest,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        product = service.purchase_product(product_id, purchase_data.quantity)
        return product_to_response(product)

    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.post("/{product_id}/discount", response_model=ProductRead)
def apply_discount(
    product_id: str,
    discount_data: DiscountRequest,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        product = service.apply_discount(product_id, discount_data.percentage)
        return product_to_response(product)

    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )