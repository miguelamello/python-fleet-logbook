# Data Ingestor
# This module is responsible for ingesting data from 
# the data source and storing it in the database.

import os
import queue
import time
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pynmeagps import NMEAReader

# Load environment variables from .env file
load_dotenv()

class Ingestor:
  def __init__(self):
    self.vdr_host = os.getenv("VDR_HOST")
    self.vdr_port = int(os.getenv("VDR_PORT"))
    self.db_host = os.getenv("DB_HOST")
    self.db_port = int(os.getenv("DB_PORT"))
    self.db_name = os.getenv("DB_NAME")
    self.db_collection = os.getenv("DB_COLLECTION")
    self.mongo = None
    self.collection = None
    self.vdr_queue = queue.Queue()

  def get_vdr_data(self):
    stream = open('nmeadata.log', 'rb')
    nmr = NMEAReader(stream, nmeaonly=True)
    for (raw_data, parsed_data) in nmr: 
      self.vdr_queue.put(parsed_data) # Add data to the queue
      time.sleep(3)  # Sleep for a short duration to simulate a delay in receiving data

  def parse_nmea_sentence(self, sentence):
    ## to be implemented
    pass

  def store_reading(self, reading):
    try:
        self.collection.insert_one(reading)
    except Exception as e:
        print("Error storing reading in the database:", e)

  def collect_vdr_data(self):
    while True:
      if not self.vdr_queue.empty():
        reading = self.vdr_queue.get()
        print(reading)
        break  # Exit the loop after processing the data
      else:
        time.sleep(1)  # Sleep for a short duration before checking the queue again

  def start(self):
    print("Starting the ingestor...")
    while True:
      if self.get_vdr_data(): 
        #self.store_reading(reading)

      time.sleep(5)  # Sleep for 10 second before collecting the next reading

  def startxx(self):

    # Connect to the MongoDB server and select the database and collection
    self.mongo = MongoClient(self.db_host, self.db_port)
    db = self.mongo[self.db_name]
    self.collection = db[self.db_collection]

  def stop(self):
    print("Stopping the ingestor...")

    # Close the connection to the MongoDB server
    #self.mongo.close()