from datetime import datetime, timedelta

class MongoUtils:
    def __init__(self, database):
        self.user_collection = database["UserData"]

    def insert_new_record(self, record):
        self.user_collection.insert_one(record)

    def update_data(self, public_id, data):
        query = {'publicId': public_id}
        value = {'$set': {'data': [data]}}
        self.user_collection.update_one(query, value)

    def get_record(self, query):
        return self.user_collection.find_one(query, {'_id': 0})

    def get_record_by_public_id(self, public_id):
        query = {'publicId': public_id}
        return self.get_record(query)

    def get_record_by_username(self, username):
        query = {'userName': username}
        return self.get_record(query)
