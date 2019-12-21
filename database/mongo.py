import logging
import pymongo
from config import MONGO_URI

cli = pymongo.MongoClient(MONGO_URI)
