from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import sys
import os
# Append the path to the 'model' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
from gemini import Gemini
from database import update_reviews, update_keywords


app = Flask(__name__, template_folder='../frontend/views', static_folder='../frontend/public')
client = MongoClient('mongodb://localhost:27017/')
db = client.reviewDatabase

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/get_keywords')
def get_keywords():
    total_reviews = db.reviews.count_documents({})
    positive = list(db.positive_keywords.find({}, {'_id': 0, 'keyword': 1, 'count': 1}).sort('count', -1).limit(10))
    negative = list(db.negative_keywords.find({}, {'_id': 0, 'keyword': 1, 'count': 1}).sort('count', -1).limit(10))
    return jsonify({'total': total_reviews, 'positive': positive, 'negative': negative})


@app.route('/submit-review', methods=['POST'])
def submit_review():
    data = request.get_json()
    review_text = data['review']
    gemini = Gemini()
    positive_keywords, negative_keywords = gemini.analyze_review(review_text)

    # Update database with obtained keywords
    update_keywords('positive', positive_keywords)
    update_keywords('negative', negative_keywords)

    # Insert the review itself
    sentiment = 'positive' if len(positive_keywords) > len(negative_keywords) else 'negative'
    update_reviews(review_text, sentiment)

    return jsonify({"status": "success", "message": "Review processed"})

if __name__ == '__main__':
    app.run(debug=True)
