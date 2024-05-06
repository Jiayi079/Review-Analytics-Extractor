import re
from transformers import BartTokenizer, BartForConditionalGeneration
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


class Traditional:
    def __init__(self):
        spacy.cli.download("en_core_web_sm")
        nltk.download('vader_lexicon')
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    def split_sentences(self, paragraph):
        pattern = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s"
        sentences = re.split(pattern, paragraph)
        return sentences

    def summarize_bart(self, text):
        inputs = self.tokenizer([f"summarize: {text}"], return_tensors="pt")
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=50,
            min_length=10,
            early_stopping=True,
            num_beams=4,
            length_penalty=-5.0,
            no_repeat_ngram_size=3
        )
        summary = [self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in
                   summary_ids]
        return summary[0].replace("summarize:", "").strip()

    def keyword(self, text):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        keywords = [token.text for token in doc if token.pos_ in ("NOUN")]
        return keywords

    def sentiment_detect(self, text):
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)
        score = sentiment_scores['compound']
        return 'positive' if score > 0 else 'negative'

    def analyze_review(self, text):
        summary = self.summarize_bart(text)
        sentences = self.split_sentences(summary)
        positive = []
        negative = []

        for sentence in sentences:
            sentiment = self.sentiment_detect(sentence)
            if sentiment == 'positive':
                positive.extend(self.keyword(sentence))
            else:
                negative.extend(self.keyword(sentence))
        return positive, negative

