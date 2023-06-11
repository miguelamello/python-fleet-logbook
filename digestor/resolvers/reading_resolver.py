from logger import Logger
from mongo import Mongo

logger = Logger()
mongo = Mongo()

def get_readings(_, info):
  return mongo.find_all('vdr_readings')

def get_readings_by_time_range(_, info, start, end):
  return mongo.find_by_time_range('vdr_readings', start, end)