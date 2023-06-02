import socket
import signal
import sys
import threading
import queue
from datetime import datetime
from pymongo import MongoClient

class DataIngestor:
    def __init__(self, host, port, database_file):
        self.host = host
        self.port = port
        self.database_file = database_file
        self.connection = None
        self.cursor = None
        self.stop_event = threading.Event()
        self.data_queue = queue.Queue()

    def connect_to_vdr(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))

    def disconnect_from_vdr(self):
        self.connection.close()

    def parse_nmea_sentence(self, sentence):
        # Implement your NMEA sentence parsing logic here
        # Extract relevant data from the sentence and return it as a dictionary
        # Example: {'timestamp': '123519', 'latitude': '4807.038', 'longitude': '01131.000', ...}
        pass

    def store_reading(self, reading):
        try:
            self.collection.insert_one(reading)
        except Exception as e:
            print("Error storing reading in the database:", e)

    def ingest_data(self):
        while not self.stop_event.is_set():
            try:
                sentence = self.connection.recv(1024).decode().strip()
                reading = self.parse_nmea_sentence(sentence)
                if reading:
                    self.store_reading(reading)
            except socket.error as e:
                print("Error receiving data from VDR:", e)
                self.disconnect_from_vdr()
                self.connect_to_vdr()

    def start_ingestor(self):
        self.connect_to_vdr()
        self.connection.settimeout(10.0)  # Set a timeout for receiving data
        self.connection.sendall(b"VDR_CONNECTION_REQUEST")  # Send a connection request to the VDR

        # Create the database table if it doesn't exist
        self.connection = sqlite3.connect(self.database_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS readings (timestamp TEXT, latitude REAL, longitude REAL, ...)"
        )

        ingest_thread = threading.Thread(target=self.ingest_data)
        ingest_thread.start()

    def stop_ingestor(self):
        self.stop_event.set()

        # Wait for the ingest thread to finish
        ingest_thread.join()

        self.disconnect_from_vdr()
        self.connection.close()

if __name__ == "__main__":
  ingestor = DataIngestor("localhost", 5000, "ship_logbook.db")
  ingestor.start_ingestor()

  # Register signal handlers for termination signals
  def signal_handler(signal, frame):
      print("Termination signal received. Stopping the ingestor...")
      ingestor.stop_ingestor()
      sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)  # SIGINT: Ctrl+C
  signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM: Termination signal

  