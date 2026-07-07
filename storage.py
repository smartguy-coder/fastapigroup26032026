from pymongo import MongoClient
from bson import ObjectId
from settings import settings


client = MongoClient(settings.URI)

database = client[settings.SHOP_NAME_DB]
collection = database[settings.BOOKS_COLLECTION]

# CREATE
book = {
    'title': '10 negro',
    'price': 345,
    'pages': 345
}
# result = collection.insert_one(document=book)
# print(result.inserted_id)

many = [
    {
        'title': 'laptop 16Gb',
        'price': 345,
        'pages': 345
    },
    {
        'title': 'super laptop lenovo 32Gb',
        'price': 345,
        'pages': 345,
        'description': 'bla-bla'
    },
]
#
# result = collection.insert_many(many)
# print(result)

# READ
# query = {
#      '_id': ObjectId('6a47e78801643a4020beee0f')
# }
# first_book = collection.find_one(query)
# print(first_book)

query = {
    # "title": "10 negro",
    # 'price': 345,
    # 'price': {'$gt': 340}
    # 'price': {'$gte': 340}
    # 'price': {'$lt': 341}
    # 'price': {'$lte': 341}
    # 'price': {'$lte': 341}
    # 'price': {'$ne': 345}
    # 'title': {'$regex': 'laptop lenovo', "$options": "i"}


    '$and': [
    # '$or': [
            {'title': {'$regex': 'lenovo', "$options": "i"}},
            {'title': {'$regex': 'laptop', "$options": "i"}},
        ]
    }


books = collection.find(query).limit(6).sort('price', -1)#.skip(1)
# print(books)
# for book in books:
#     print(book)


# UPDATE#
query = {
    # '_id': ObjectId('6a47e78801643a4020beee0f')
}
new_data = {
    # '$set': {'is_new': True}
    # '$inc': {'price': -0.8}
    '$mul': {'price': 1.2}
}
# collection.update_one()
# result = collection.update_many(query, new_data)
# print(result)

# delete
query = {
    '_id': ObjectId('6a47e78801643a4020beee0f')
}
result = collection.delete_one(query)
print(result)