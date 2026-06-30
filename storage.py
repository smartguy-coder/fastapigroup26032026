from pymongo import MongoClient
from settings import settings


client = MongoClient(settings.URI)

database = client[settings.SHOP_NAME_DB]
collection = database[settings.BOOKS_COLLECTION]

book = {
    'title': '10 negro',
    'price': 345
}
result = collection.insert_one(document=book)
print(result)
