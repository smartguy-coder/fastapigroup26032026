from fastapi import APIRouter, status

from schemas import BookCreateSchema

api_router = APIRouter(
    prefix='/api/books'
)


@api_router.get('')
def index_books():
    return 2222


@api_router.post('', status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema) -> BookCreateSchema:
    """the single endpoint for creating book in storage"""
    print(book)
    print(type(book))
    return book