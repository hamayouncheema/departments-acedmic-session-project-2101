from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.get_database()

    def get_departments_collection(self):
        return self.db.departments
