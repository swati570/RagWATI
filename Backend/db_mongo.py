from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["rag_chatbot"]

users_col = db["users"]
projects_col = db["projects"]
pdfs_col = db["pdfs"]
chunks_col = db["chunks"]

