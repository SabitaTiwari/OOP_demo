from fastapi import FastAPI

from app.api.routes.product_routes import router as product_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="A demo FastAPI project for learning OOP concepts in Python.",
)

app.include_router(product_router, prefix=settings.API_PREFIX)


@app.get("/")
def health_check():
    return {
        "message": "OOP FastAPI Demo is running",
        "docs": "/docs",
    }