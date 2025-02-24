import os
import uuid
from abc import ABC, abstractmethod
import json
from fastapi import HTTPException, status

from pymongo import MongoClient

from schemas import NewProduct, SavedProduct, ProductId
from settings import settings


class BaseStorage(ABC):
    @abstractmethod
    def create_product(self, new_product: NewProduct) -> SavedProduct:
        pass

    @abstractmethod
    def get_product(self, product_id: str) -> SavedProduct:
        pass

    @abstractmethod
    def get_products(
        self, q: str = "", limit: int = 10, skip: int = 0
    ) -> list[SavedProduct]:
        pass

    @abstractmethod
    def delete_product(self, product_id: str) -> None:
        pass


class MongoStorage(BaseStorage):
    def __init__(self, uri: str):
        client = MongoClient(uri)
        db = client.products
        collection_product = db.products
        self.collection_product = collection_product

    def create_product(self, new_product: NewProduct) -> SavedProduct:

        payload = {
            "title": new_product.title,
            "price": new_product.price,
            "description": new_product.description,
            "cover": new_product.cover,
            "id": uuid.uuid4().hex,
        }
        self.collection_product.insert_one(payload)
        saved_product = SavedProduct(**payload)
        return saved_product

    def get_product(self, product_id: str) -> SavedProduct:
        query = {"id": product_id}
        book = self.collection_product.find_one(query)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return book

    def get_products(
        self, q: str = "", limit: int = 10, skip: int = 0
    ) -> list[SavedProduct]:
        query = {}
        if q:
            query = {
                "$or": [
                    {
                        "title": {
                            "$regex": q,
                            "$options": "i",
                        }
                    },
                    {
                        "description": {
                            "$regex": q,
                            "$options": "i",
                        }
                    },
                ]
            }
        books = self.collection_product.find(query).limit(limit).skip(skip)
        return books or []

    def delete_product(self, product_id: str) -> None:
        query = {"id": product_id}
        self.collection_product.delete_many(query)


class FileStorage(BaseStorage):
    def __init__(self, file_name: str):
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(self.file_name, mode="w") as file:
                json.dump([], file, indent=4)

    def create_product(self, new_product: NewProduct) -> SavedProduct:
        with open(self.file_name, mode="r") as file:
            content: list[dict] = json.load(file)
        payload = {
            "title": new_product.title,
            "price": new_product.price,
            "description": new_product.description,
            "cover": new_product.cover,
            "id": uuid.uuid4().hex,
        }
        content.append(payload)
        with open(self.file_name, mode="w") as file:
            json.dump(content, file, indent=4)
        # saved_product = SavedProduct(title=payload['title']...)
        saved_product = SavedProduct(**payload)
        return saved_product


# storage: BaseStorage = FileStorage("storage.json")
storage: BaseStorage = MongoStorage(settings.MONGO_URI)
