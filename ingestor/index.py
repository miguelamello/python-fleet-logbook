import socket
import signal
import sys
import os
import threading
import queue
from dotenv import load_dotenv
from datetime import datetime
from pymongo.mongo_client import MongoClient

class DataIngestor:
  def __init__(self, host, port, database_name, collection_name):
    self.host = host
    self.port = port
    self.database_name = database_name
    self.collection_name = collection_name
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
    self.connect_to_vdr()
    self.socket.settimeout(10.0)  # Set a timeout for receiving data
    self.socket.sendall(b"VDR_CONNECTION_REQUEST")  # Send a connection request to the VDR

    # Connect to the MongoDB server and select the database and collection
    self.mongo = MongoClient(self.host, self.port)
    db = self.mongo[self.database_name]
    self.collection = db[self.collection_name]

    ingest_thread = threading.Thread(target=self.ingest_data)
    ingest_thread.start()

  def stop_ingestor(self):
    self.stop_event.set()

    # Wait for the ingest thread to finish
    ingest_thread.join()

    self.disconnect_from_vdr()
    self.mongo.close()

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":

  # Read environment variables
  host = os.getenv("HOST")
  port = int(os.getenv("PORT"))
  database_name = os.getenv("DATABASE_NAME")
  collection_name = os.getenv("COLLECTION_NAME")

  ingestor = DataIngestor(host, port, database_name, collection_name)
  ingestor.start_ingestor()

  # Register signal handlers for termination signals
  def signal_handler(signal, frame):
    print("Termination signal received. Stopping the ingestor...")
    ingestor.stop_ingestor()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)  # SIGINT: Ctrl+C
  signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM: Termination signal

  