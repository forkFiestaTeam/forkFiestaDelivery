import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv(find_dotenv())

# MongoDB Configuration
mdb_client = MongoClient(os.environ.get("MONGODB_SRV"))
