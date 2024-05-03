import re
from transformers import BartTokenizer, BartForConditionalGeneration
import spacy
from sentiment_analysis import analysis


#spacy.cli.download("en_core_web_sm")

def split_sentences(paragraph):
    pattern = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!|;)\s"
    sentences = re.split(pattern, paragraph)
    return sentences


def summarize_bart(text):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    inputs = tokenizer([f"summarize: {text}"], return_tensors="pt")
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=50,
        min_length=10,
        do_sample=False,
        early_stopping=True,
        num_beams=4,
        length_penalty=2.0,
        no_repeat_ngram_size=3,
    )
    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    return summary[0].replace("summarize:", "").strip()


def keyword(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ("NOUN")]
    return keywords


def analyze_review(text):
    summary = summarize_bart(text)
    sentences = split_sentences(summary)
    positive = []
    negative = []

    for sentence in sentences:
        sentiment = analysis(sentence)
        if sentiment == 'positive':
            positive.extend(keyword(sentence))
        else:
            negative.extend(keyword(sentence))
    return [positive, negative]


test = "The product is truly exceptional in terms of both aesthetics and functionality, showcasing a level of craftsmanship that is rare in today's market. It exceeded my expectations in every way, making it a delight to use daily. However, the shipping process was incredibly slow and lacked proper communication from the carrier, which was quite frustrating given the anticipation of receiving such a high-quality item."
print(analyze_review(test))
