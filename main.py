from fastapi import FastAPI, Query, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import uvicorn
import json
import requests

json_data = [
  {
    "id": 1,
    "name": "Смартфон",
    "description": "Современный смартфон",
    "price": 99999.99,
    "currency": "RUB",
    "category": "Электроника",
    "created_at": "2024-11-26T10:00:00",
    "updated_at": "2024-11-26T10:00:00"
  },
  {
    "id": 2,
    "name": "Телевизор",
    "description": "Smart TV с разрешением 4K",
    "price": 55999.99,
    "currency": "RUB",
    "category": "Электроника",
    "created_at": "2024-11-26T10:30:00",
    "updated_at": "2024-11-26T10:30:00"
  },
  {
    "id": 3,
    "name": "Ноутбук",
    "description": "Легкий и мощный ноутбук для работы и игр",
    "price": 89999.99,
    "currency": "RUB",
    "category": "Электроника",
    "created_at": "2024-11-26T11:00:00",
    "updated_at": "2024-11-26T11:00:00"
  },
  {
    "id": 4,
    "name": "Наушники",
    "description": "Беспроводные наушники с шумоподавлением",
    "price": 19999.99,
    "currency": "RUB",
    "category": "Аудиотехника",
    "created_at": "2024-11-26T11:30:00",
    "updated_at": "2024-11-26T11:30:00"
  },
  {
    "id": 5,
    "name": "Робот-пылесос",
    "description": "Автоматический робот для уборки с функцией планирования",
    "price": 14999.99,
    "currency": "RUB",
    "category": "Техника для дома",
    "created_at": "2024-11-26T12:00:00",
    "updated_at": "2024-11-26T12:00:00"
  },
  {
    "id": 6,
    "name": "Графический планшет",
    "description": "Планшет для рисования с высокой чувствительностью",
    "price": 24999.99,
    "currency": "RUB",
    "category": "Электроника",
    "created_at": "2024-11-26T12:30:00",
    "updated_at": "2024-11-26T12:30:00"
  },
  {
    "id": 7,
    "name": "Электрический чайник",
    "description": "Чайник с быстрым нагревом и автоотключением",
    "price": 4999.99,
    "currency": "RUB",
    "category": "Техника для кухни",
    "created_at": "2024-11-26T13:00:00",
    "updated_at": "2024-11-26T13:00:00"
  },
  {
    "id": 8,
    "name": "Кофемашина",
    "description": "Многофункциональная кофемашина для дома",
    "price": 17999.99,
    "currency": "RUB",
    "category": "Техника для кухни",
    "created_at": "2024-11-26T13:30:00",
    "updated_at": "2024-11-26T13:30:00"
  },
  {
    "id": 9,
    "name": "Фитнес-трекер",
    "description": "Умный браслет с мониторингом сердечного ритма",
    "price": 6999.99,
    "currency": "RUB",
    "category": "Спорт и отдых",
    "created_at": "2024-11-26T14:00:00",
    "updated_at": "2024-11-26T14:00:00"
  },
  {
    "id": 10,
    "name": "Камера видеонаблюдения",
    "description": "IP-камера для дома с ночным видением",
    "price": 10999.99,
    "currency": "RUB",
    "category": "Безопасность",
    "created_at": "2024-11-26T14:30:00",
    "updated_at": "2024-11-26T14:30:00"
  }

]

app = FastAPI(
    title="Marketplace API"
)

class GetProducts(BaseModel):
    page: int = 1
    per_page: int = Query(20, ge=1)
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    category: Optional[str] = None
    currency: str = "RUB"

class GetProductsByID(BaseModel):
    product_id: int = None
    currency: Optional[str] = "RUB"


@app.get("/api/v1/products")
def get_products(params: GetProducts = Depends()):
    # Фильтрация товаров
    filtered_products = [
        product for product in json_data
        if (params.min_price is None or product["price"] >= params.min_price) and
           (params.max_price is None or product["price"] <= params.max_price) and
           (params.category is None or product["category"] == params.category)
    ]

    # Проверка на существование категории
    if params.category and not any(product["category"] == params.category for product in json_data):
        raise HTTPException(status_code=404, detail=f"The category '{params.category}' was not found.")

    # Проверка, если товары отсутствуют после фильтрации
    if not filtered_products:
        raise HTTPException(status_code=404, detail="Products matching the specified filters were not found.")


    # Постраничный вывод
    start = (params.page - 1) * params.per_page
    end = start + params.per_page
    paginated_products = filtered_products[start:end]

    # Возвращаем результат
    return {
        "items": paginated_products,
        "total": len(filtered_products),
        "page": params.page,
        "per_page": params.per_page,
        "pages": (len(filtered_products) + params.per_page - 1) // params.per_page
    }

@app.get("/api/v1/products/{product_id}")
def get_product_by_id(params: GetProductsByID = Depends()):
    product = next((item for item in json_data if item['id'] == params.product_id), None)
    
    if product is None:
        return {
            "error": "Product not found"
        }, 404
    
    return product

@app.post("/api/v1/products")
def add_product():
    pass

@app.put("/api/v1/products/{product_id}")
def change_product():
    pass

@app.delete("/api/v1/products/{product_id}")
def delete_product():
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)