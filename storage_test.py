from pymongo import MongoClient
from settings import settings


client = MongoClient(settings.URI)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)