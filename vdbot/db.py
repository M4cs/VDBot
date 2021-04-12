from pymongo import MongoClient
from vdbot.config import config

client = MongoClient(config.db.url)
db = client.vdbot