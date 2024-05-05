# test_connection.py
from pymongo import MongoClient
import os

def main():
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()

    # Connect to MongoDB
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/reviewDatabase')
    client = MongoClient(mongo_uri)
    db = client.reviewDatabase

    # Perform a test insert
    result = db.test_collection.insert_one({"name": "Test", "value": 123})
    print(f"Inserted Document ID: {result.inserted_id}")

    # Fetch the inserted document
    document = db.test_collection.find_one({"_id": result.inserted_id})
    print(f"Fetched Document: {document}")

    # Clean up (remove the test document)
    db.test_collection.delete_one({"_id": result.inserted_id})

if __name__ == "__main__":
    main()
