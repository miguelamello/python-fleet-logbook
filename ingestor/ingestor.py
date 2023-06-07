# Data Ingestor
# This module is responsible for ingesting data from 
# the data source and storing it in the database.

import time
from datetime import datetime, timezone
import csv
import random

class Ingestor:
  def __init__(self):
    self.vdr_data = []
    self.poll_vdr_data()

  # Handles errors output
  def error_handler(err):
    # Print the error message to the console 
    # but in production you would probably 
    # want to log to a database instead
    print(err)

  # Read nmea data from file and store in a list
  # to simulate data from the VDR
  def poll_vdr_data(self):
    filename = "nmeadata.log"
    with open(filename, "r") as file:
      reader = csv.reader(file)
      self.vdr_data = list(reader)

  # Get a random line from the list of VDR data
  def get_vdr_sentence(self):
    index = random.randint(0, len(self.vdr_data) - 1)
    data = {
      "source": self.vdr_data[index][0],
      "latitude": self.vdr_data[index][1] + self.vdr_data[index][2],
      "longitude": self.vdr_data[index][3] + self.vdr_data[index][4],
      "utctime": self.vdr_data[index][5]
    }
    return data

  def format_sentence(self, sentence):
    timestamp = datetime.now().isoformat()
    data = {
      'timestamp': timestamp,
      'metadata': sentence
    }
    return data

  def start(self):
    while True:
      sentence = self.get_vdr_sentence()
      if sentence: 
        timeserie = self.format_sentence(sentence)
        if timeserie:
          print(timeserie)
          # Insert the timeseries into the database
          #self.mongo.insert_one(timeserie)
      time.sleep(10)  # Sleep for 10 second before collecting the next reading

  def stop(self):
    pass
    # Close the connection to the MongoDB server
    #self.mongo.close()