# products.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from sample_products import sample_products

router = APIRouter()

@router.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/products/search")
async def search_products(
        keyword: str = Query(..., min_length=1, description="Ключевое слово для поиска"),
        category: Optional[str] = Query(None, description="Категория для фильтрации"),
        limit: int = Query(10, ge=1, le=50, description="Максимальное количество результатов")
):
    results: List[Dict[str, Any]] = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category is None or product["category"].lower() == category.lower():
                results.append(product)
                if len(results) >= limit:
                    break

    return results