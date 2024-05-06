from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__, template_folder='../frontend/views', static_folder='../frontend/public')
client = MongoClient('mongodb://localhost:27017/')
db = client.reviewDatabase

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/get_keywords')
def get_keywords():
    positive = list(db.positive_keywords.find({}, {'_id': 0, 'keyword': 1, 'count': 1}))
    negative = list(db.negative_keywords.find({}, {'_id': 0, 'keyword': 1, 'count': 1}))
    return jsonify({'positive': positive, 'negative': negative})

@app.route('/submit-review', methods=['POST'])
def submit_review():
    data = request.get_json()
    review_text = data['review']
    print("Received review:", review_text)
    return jsonify({"status": "success", "message": "Review received"})

if __name__ == '__main__':
    app.run(debug=True)
