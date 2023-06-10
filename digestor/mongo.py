import os
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
      data = self.collection.find().limit(100)
      return list(data)
    except Exception:
      self.logger.store()

  def __del__(self):
    try:
      self.mongo.close()
    except Exception:
      self.logger.store()
