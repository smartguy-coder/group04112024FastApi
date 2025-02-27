from fastapi import FastAPI, status, Request, Form
from fastapi.templating import Jinja2Templates

from schemas import NewProduct, SavedProduct, PatchProduct

from storage.base_storage import storage


app = FastAPI()

templates = Jinja2Templates(directory="templates")


# WEB
@app.get("/")
@app.post("/")
def index(request: Request, q: str = Form(default="")):
    books = storage.get_products(q=q)
    context = {"request": request, "books": books}
    return templates.TemplateResponse(
        "index.html",
        context=context,
    )


# API
@app.post("/books/", tags=["Книги"], status_code=status.HTTP_201_CREATED)
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
def edit_book(book_id: str, data: PatchProduct) -> SavedProduct:
    product = storage.patch_product(book_id, data)
    return product


@app.delete("/books/{book_id}")
def delete_book(book_id: str) -> dict:
    storage.delete_product(book_id)
    return {}
