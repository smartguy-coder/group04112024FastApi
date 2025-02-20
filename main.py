from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"status": "OK"}


@app.post("/books/", tags=["Книги"])
def create_book():
    pass


@app.get("/books/{book_id}")
def get_book(book_id: str):
    return book_id


@app.get("/books/")
def get_books(query: str = "", limit: int = 10, skip: int = 0):
    return {"query": query, "limit": limit, "skip": skip}


@app.patch("/books/{book_id}")
def edit_book(book_id: str, data: dict):
    pass


@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    pass
