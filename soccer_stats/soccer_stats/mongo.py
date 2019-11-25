from pymongo import MongoClient
from soccer_stats.settings import MONGO_URI, MONGO_DATABASE


class StatsMongoClient:

    def __init__(self, uri, database):
        self.__connection = MongoClient(uri)
        self.__database = self.__connection[database]

    @property
    def collection(self):
        if self.__collection:
            return self.__collection
        return None
    
    @collection.setter
    def collection(self, collection: str):
        self.__collection = self.__database[collection]

    @property
    def db(self):
        return self.__database

    def close(self):
        self.__connection.close()


mongo_client = StatsMongoClient(MONGO_URI, MONGO_DATABASE)