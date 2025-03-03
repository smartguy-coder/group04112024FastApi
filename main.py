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


@app.get("/map_route")
def map_route(request: Request):

    context = {"request": request}
    return templates.TemplateResponse(
        "map.html",
        context=context,
    )


@app.get("/video")
def video(request: Request):

    context = {"request": request}
    return templates.TemplateResponse(
        "video.html",
        context=context,
    )


@app.get("/{product_id}")
def get_book_info(request: Request, product_id: str):
    book = storage.get_product(product_id=product_id, with_raise=False)
    if not book:
        return templates.TemplateResponse(
            "404.html",
            context={"request": request},
        )

    context = {"request": request, "book": book}
    return templates.TemplateResponse(
        "details.html",
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
