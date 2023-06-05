# Data Ingestor
# This module is responsible for ingesting data from 
# the data source and storing it in the database.

import os
import socket
import threading
import queue
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

# Load environment variables from .env file
load_dotenv()

class DataIngestor:
  def __init__(self):
    self.vdr_host = os.getenv("VDR_HOST")
    self.vdr_port = int(os.getenv("VDR_PORT"))
    self.db_host = os.getenv("DB_HOST")
    self.db_port = int(os.getenv("DB_PORT"))
    self.db_name = os.getenv("DB_NAME")
    self.db_collection = os.getenv("DB_COLLECTION")
    self.mongo = None
    self.collection = None
    self.socket = None
    self.stop_event = threading.Event()
    self.data_queue = queue.Queue()

  def connect_to_vdr(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.host, self.port))

  def disconnect_from_vdr(self):
    self.socket.close()

  def parse_nmea_sentence(self, sentence):
    ## to be implemented
    pass

  def store_reading(self, reading):
    try:
        self.collection.insert_one(reading)
    except Exception as e:
        print("Error storing reading in the database:", e)

  def ingest_data(self):
    while not self.stop_event.is_set():
      try:
        sentence = self.socket.recv(1024).decode().strip()
        reading = self.parse_nmea_sentence(sentence)
        if reading:
            self.store_reading(reading)
      except socket.error as e:
        print("Error receiving data from VDR:", e)
        self.disconnect_from_vdr()
        self.connect_to_vdr()

  def start_ingestor(self):
    print("Starting the ingestor...")

    #self.connect_to_vdr()
    #self.socket.settimeout(10.0)  # Set a timeout for receiving data
    #self.socket.sendall(b"VDR_CONNECTION_REQUEST")  # Send a connection request to the VDR

    # Connect to the MongoDB server and select the database and collection
    self.mongo = MongoClient(self.db_host, self.db_port)
    db = self.mongo[self.db_name]
    self.collection = db[self.db_collection]

    #ingest_thread = threading.Thread(target=self.ingest_data)
    #ingest_thread.start()

  def stop_ingestor(self):
    print("Stopping the ingestor...")
    #self.stop_event.set()

    # Wait for the ingest thread to finish
    #ingest_thread.join()

    #self.disconnect_from_vdr()
    self.mongo.close()