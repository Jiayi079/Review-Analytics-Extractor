import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

with open('product_review.json', 'r') as file:
    reviews = json.load(file)

def clean_text(text):
    text = re.sub(r'\W', ' ', str(text))
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = re.sub(r'^b\s+', '', text)
    text = text.lower()
    return text

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

for review in reviews:
    review['ReviewText'] = clean_text(review['ReviewText'])
    review['Tokens'] = [lemmatizer.lemmatize(word) for word in word_tokenize(review['ReviewText']) if word not in stop_words]

    for segment in review['Segments']:
        segment['SegmentText'] = clean_text(segment['SegmentText'])
        segment['Tokens'] = [lemmatizer.lemmatize(word) for word in word_tokenize(segment['SegmentText']) if word not in stop_words]

with open('preprocessed_reviews.json', 'w') as f:
    json.dump(reviews, f, indent=4)
