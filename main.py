from fastapi import FastAPI

from schemas import NewProduct, SavedProduct

from storage.base_storage import storage


app = FastAPI()


@app.get("/")
def index():
    return {"status": "OK"}


@app.post("/books/", tags=["Книги"])
def create_book(new_book: NewProduct) -> SavedProduct:
    product = storage.create_product(new_book)
    return product


@app.get("/books/{book_id}")
def get_book(book_id: str) -> SavedProduct:
    book = storage.get_product(book_id)
    return book


@app.get("/books/")
def get_books(query: str = "", limit: int = 10, skip: int = 0) -> list[SavedProduct]:
    books = storage.get_products(q=query, limit=limit, skip=skip)
    return books


@app.patch("/books/{book_id}")
def edit_book(book_id: str, data: dict):
    pass


@app.delete("/books/{book_id}")
def delete_book(book_id: str) -> dict:
    storage.delete_product(book_id)
    return {}
