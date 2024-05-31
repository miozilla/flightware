from pymongo import MongoClient, DESCENDING

class MongoDBClient:
    def __init__(self, db_name, collection_name, uri='mongodb://localhost:27017/'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def find_one_document(self, query=None):
        return self.collection.find_one(query)
    
    def find_documents_sorted_by_timestamp(self, query=None, limit=1):
        return self.collection.find(query).sort("timestamp", DESCENDING).limit(limit)
    
    def close_connection(self):
        self.client.close()


