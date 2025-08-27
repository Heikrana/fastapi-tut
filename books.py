from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: float

BOOKS = [
    Book(1, "Computer Science Pro", "meow", "A very nice book about cs", 4.5),
    Book(2, "Environment Science Pro", "meow1", "A very nice book about evs", 4),
    Book(3, "FastAPI", "meowmeow", "A very nice book about fastapi", 3.5),
    Book(4, "DSA", "Charles", "A very nice book about dsa", 5),
    Book(5, "HP1", "Author 1", "Book description", 2)
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
    return {"message": "Book added successfully!"}