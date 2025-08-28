from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=0, lt=5.01)
    published_date: int = Field(gt=1999, lt=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "meowmeowmeowmeowm",
                "rating": 5,
                "published_date": 2012,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "meow", "A very nice book about cs", 4.5, 2011),
    Book(2, "Environment Science Pro", "meow1", "A very nice book about evs", 4, 2011),
    Book(3, "FastAPI", "meowmeow", "A very nice book about fastapi", 3.5, 2011),
    Book(4, "DSA", "Charles", "A very nice book about dsa", 5, 2010),
    Book(5, "HP1", "Author 1", "Book description", 2, 2020),
]


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    
    raise HTTPException(status_code=404, detail='Item not found')


@app.get("/books/")
async def read_book_by_rating(book_rating: float = Query(gt=0, lt=5.01)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.get("/books/publish/")
async def read_book_by_date(publish_date: int = Query(gt=1999, lt=2026)):
    books_to_return = []

    for book in BOOKS:
        if book.published_date == publish_date:
            books_to_return.append(book)

    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book added successfully!"}


@app.put("/books/update_book")
async def update_book(updated_book: BookRequest):
    book_changed = False
    new_book = Book(**updated_book.model_dump())
    for i, book in enumerate(BOOKS):
        if book.id == updated_book.id:
            BOOKS[i] = new_book
            book_changed = True
    
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break

    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found')

