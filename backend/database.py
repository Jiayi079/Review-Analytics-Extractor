import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/reviewDatabase')
db_name = os.getenv('DB_NAME', 'reviewDatabase')
client = MongoClient(mongo_uri)
db = client[db_name]

# Collection names
COLLECTION_REVIEWS = 'reviews'
COLLECTION_POSITIVE_KEYWORDS = 'positive_keywords'
COLLECTION_NEGATIVE_KEYWORDS = 'negative_keywords'

def update_reviews(review_text, sentiment):
    """Inserts a new review with its sentiment."""
    try:
        result = db[COLLECTION_REVIEWS].insert_one({"text": review_text, "sentiment": sentiment})
        logging.info(f"Inserted new review with ID: {result.inserted_id}")
        return result.inserted_id  # Return this ID for reference if needed
    except Exception as e:
        logging.error(f"An error occurred in update_reviews: {e}")

def update_keywords(sentiment, keywords):
    """Updates counts for keywords based on the sentiment."""
    collection_name = COLLECTION_POSITIVE_KEYWORDS if sentiment == 'positive' else COLLECTION_NEGATIVE_KEYWORDS
    try:
        for keyword in keywords:
            result = db[collection_name].update_one({"keyword": keyword}, {"$inc": {"count": 1}}, upsert=True)
            logging.info(f"Updated keyword '{keyword}' in {collection_name}: {result.raw_result}")
    except Exception as e:
        logging.error(f"An error occurred in update_keywords: {e}")

# test performance
if __name__ == "__main__":
    review_id = update_reviews("This product is great!", "positive")
    update_keywords("positive", ["great", "amazing"])
    review_id = update_reviews("This product is not good!", "negative")
    update_keywords("negative", ["not good", "poor"])
