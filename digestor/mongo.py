import os
from datetime import datetime
from dotenv import load_dotenv
from logger import Logger
from pymongo.mongo_client import MongoClient

# Load environment variables from .env file
load_dotenv()


class Mongo:
    def __init__(self):
        self.logger = Logger()
        self.db_host = os.getenv("DB_HOST")
        self.db_port = int(os.getenv("DB_PORT"))
        self.db_name = os.getenv("DB_NAME")
        self.mongo = None
        self.collection = None
        self.connect()

    def connect(self):
        try:
            self.mongo = MongoClient(self.db_host, self.db_port)

        except Exception:
            self.logger.store()

    def store_one(self, data):
        try:
            self.collection.insert_one(data)

        except Exception:
            self.logger.store()

    def find_all(self, collection):
        try:
            self.collection = self.mongo[self.db_name][collection]
            items = self.collection.find().limit(1000)
            return list(items)

        except Exception:
            self.logger.store()

    def find_by_time_range(self, collection, start, end):
        try:
          self.collection = self.mongo[self.db_name][collection]

          # Convert start and end timestamps to datetime objects
          start_datetime = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
          end_datetime = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")

          # Query MongoDB for items within the specified time range
          items = self.collection.find({
              'timestamp': {
                  '$gte': start_datetime,
                  '$lte': end_datetime
              }
          }).limit(1000)

          return list(items)

        except Exception:
            self.logger.store()

    def __del__(self):
        try:
            self.mongo.close()
        except Exception:
            self.logger.store()
