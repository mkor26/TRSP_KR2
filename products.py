# products.py
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from sample_products import sample_products

router = APIRouter()


# Модель для POST запроса поиска
class SearchRequest(BaseModel):
    keyword: str
    category: Optional[str] = None
    limit: int = 10


# Задание 3.2 – GET /product/{product_id}
@router.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


# Задание 3.2 – GET /products/search (оригинальный метод из задания)
@router.get("/products/search")
async def search_products_get(
        keyword: str = Query(..., min_length=1, description="Ключевое слово для поиска"),
        category: Optional[str] = Query(None, description="Категория для фильтрации"),
        limit: int = Query(10, ge=1, le=50, description="Максимальное количество результатов")
):

    results: List[Dict[str, Any]] = []

    for product in sample_products:
        # Проверяем наличие ключевого слова в названии
        if keyword.lower() in product["name"].lower():
            # Проверяем категорию, если она указана
            if category is None or product["category"].lower() == category.lower():
                results.append(product)
                if len(results) >= limit:
                    break

    return results





