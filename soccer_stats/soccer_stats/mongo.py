from pymongo import MongoClient


class StatsMongoClient:

    def __init__(self, uri, database, collection):
        self.__connection = MongoClient(uri)
        self.__database = self.__connection[database]
        self.__collection = self.__database[collection]

    @property
    def collection(self):
        return self.__collection
    
    @collection.setter
    def collection(self, collection: str):
        self.__collection = collection

    @property
    def db(self):
        return self.__database

    def close(self):
        self.__connection.close()
