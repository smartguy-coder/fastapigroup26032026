
from pymongo import MongoClient
from bson import ObjectId

from schemas import BookCreateSchema, BookSavedSchema, BookPriceSchema
from settings import settings
from abc import ABC, abstractmethod
from datetime import datetime
from fastapi import HTTPException, status

class BaseStorage(ABC):

    @abstractmethod
    def create_book(self, book: BookCreateSchema) -> BookSavedSchema:
        return

    @abstractmethod
    def get_book(self, book_id: str) -> BookSavedSchema:
        return

    @abstractmethod
    def get_books(self, page: int, q: str) -> list[BookSavedSchema]:
        return

    @abstractmethod
    def delete_book(self, book_id: str) -> None:
        return

    @abstractmethod
    def update_book(self, book_id: str, update_data: BookCreateSchema | BookPriceSchema) -> BookSavedSchema:
        return


class MongoStorage(BaseStorage):
    def __init__(self):
        client = MongoClient(settings.URI)
        database = client[settings.SHOP_NAME_DB]
        self.collection = database[settings.BOOKS_COLLECTION]

    def get_books(self, page: int, q: str) -> list[BookSavedSchema]:
        query = {}
        if q.strip():
            search_words = q.replace(',', ' ').split()
            query_search_words = []
            for search_word in search_words:
                if len(search_word) > 1:
                    query_search_words.append(search_word)

            if query_search_words:
                print(query_search_words)

                query_search_dicts = []
                for query_search_word in query_search_words:
                    query_search_dicts.append(
                        {'title': {'$regex': query_search_word, "$options": "i"}}
                    )

                query = {'$and': query_search_dicts}

        skip = (page - 1) * settings.PAGE_SIZE
        books = self.collection.find(query).limit(settings.PAGE_SIZE).skip(skip)
        prepared_books = []
        for raw_book in books:
            prepared_books.append(   BookSavedSchema(id=str(raw_book['_id']),  **raw_book)    )
        return prepared_books

    def get_book(self, book_id: str | ObjectId) -> BookSavedSchema:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(
                detail=f"Invalid book id '{book_id}'",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        query = {
             '_id': ObjectId(book_id)
        }
        raw_book = self.collection.find_one(query)
        if not raw_book:
            raise HTTPException(
                detail=f"Book with id '{book_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        book = BookSavedSchema(
            id=str(raw_book['_id']),
            **raw_book
        )
        return book

    def create_book(self, book: BookCreateSchema) -> BookSavedSchema:
        book_dict = book.model_dump()
        book_dict['created_at'] = datetime.now()

        result = self.collection.insert_one(document=book_dict)
        book_id = result.inserted_id
        # print(book_id)
        # saved = BookSavedSchema(
        #     id=str(book_id),
        #     **book_dict
        # )
        saved = self.get_book(book_id)
        return saved

    def delete_book(self, book_id: str) -> None:
        self.get_book(book_id)
        query = {
            '_id': ObjectId(book_id)
        }
        self.collection.delete_one(query)

    def update_book(self, book_id: str, update_data: BookCreateSchema | BookPriceSchema) -> BookSavedSchema:
        self.get_book(book_id)
        new_data = update_data.model_dump()
        payload = {"$set": new_data}
        self.collection.update_one(
            {'_id': ObjectId(book_id)},
            payload
        )
        return self.get_book(book_id)

storage: BaseStorage = MongoStorage()



#
# # READ
# # query = {
# #      '_id': ObjectId('6a47e78801643a4020beee0f')
# # }
# # first_book = collection.find_one(query)
# # print(first_book)
#
# query = {
#     # "title": "10 negro",
#     # 'price': 345,
#     # 'price': {'$gt': 340}
#     # 'price': {'$gte': 340}
#     # 'price': {'$lt': 341}
#     # 'price': {'$lte': 341}
#     # 'price': {'$lte': 341}
#     # 'price': {'$ne': 345}
#     # 'title': {'$regex': 'laptop lenovo', "$options": "i"}
#
#
#     '$and': [
#     # '$or': [
#             {'title': {'$regex': 'lenovo', "$options": "i"}},
#             {'title': {'$regex': 'laptop', "$options": "i"}},
#         ]
#     }
#
#
# books = collection.find(query).limit(6).sort('price', -1)#.skip(1)
# # print(books)
# # for book in books:
# #     print(book)
#
#
# # UPDATE#
# query = {
#     # '_id': ObjectId('6a47e78801643a4020beee0f')
# }
# new_data = {
#     # '$set': {'is_new': True}
#     # '$inc': {'price': -0.8}
#     '$mul': {'price': 1.2}
# }
# # collection.update_one()
# # result = collection.update_many(query, new_data)
# # print(result)
#
# # delete
# query = {
#     '_id': ObjectId('6a47e78801643a4020beee0f')
# }
# result = collection.delete_one(query)
# print(result)