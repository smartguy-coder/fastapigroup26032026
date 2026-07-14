from fastapi import APIRouter, status, Query

from schemas import BookCreateSchema, BookSavedSchema, BookPriceSchema
from storage import storage

api_router = APIRouter(
    prefix='/api/books'
)


@api_router.get('')
def get_books(
        page: int = Query(qt=0, default=1),
        q: str = Query(default='')
) -> list[BookSavedSchema]:
    return storage.get_books(page=page, q=q)


@api_router.get('/{book_id}')
def get_book(book_id: str) -> BookSavedSchema:
    book = storage.get_book(book_id)
    return book


@api_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str):
    storage.delete_book(book_id)


@api_router.post('', status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema) -> BookSavedSchema:
    """the single endpoint for creating book in storage"""
    created_book = storage.create_book(book)
    return created_book


@api_router.put('/{book_id}')
def update_book(book_id: str, data: BookCreateSchema) -> BookSavedSchema:

    return storage.update_book(book_id, data)


@api_router.patch('/{book_id}')
def update_book_price(book_id: str, patch_data: BookPriceSchema) -> BookSavedSchema:
    return storage.update_book(book_id, patch_data)
