# Data Ingestor
# This module is responsible for ingesting data from 
# the data source and storing it in the database.

import time
from datetime import datetime, timezone
import csv
import random
import json
from logger import Logger
from mongo import Mongo

class Ingestor:
  def __init__(self):
    self.logger = Logger()
    self.mongo = Mongo()
    self.vdr_data = []
    self.poll_vdr_data()

  # Read nmea data from file and store in a list
  # to simulate data from the VDR
  def poll_vdr_data(self):
    try:
      filename = "nmeadata.log"
      with open(filename, "r") as file:
        reader = csv.reader(file)
        self.vdr_data = list(reader)
    except Exception:
      self.logger.store()

  # Get a random line from the list of VDR data
  def get_vdr_sentence(self): 
    if len(self.vdr_data) == 0:
      return None
    else:
      index = random.randint(0, len(self.vdr_data) - 1)
      data = {
        "source": self.vdr_data[index][0],
        "latitude": self.vdr_data[index][1] + self.vdr_data[index][2],
        "longitude": self.vdr_data[index][3] + self.vdr_data[index][4],
        "utctime": self.vdr_data[index][5]
      }
      return data

  def format_sentence(self, sentence):
    if len(sentence) == 0:
      return None
    else:
      timestamp = datetime.utcnow()
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
          # Insert the timeseries into the database
          self.mongo.store_one(timeserie)
      time.sleep(10)  # Sleep for 10 second before collecting the next reading

  def stop(self):
    # Close the connection to the MongoDB server
    self.mongo.close()

    