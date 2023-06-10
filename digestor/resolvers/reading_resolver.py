from logger import Logger
from mongo import Mongo

logger = Logger()
mongo = Mongo()

def get_readings(_, info):
  return mongo.find_all('vdr_readings')
