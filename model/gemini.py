import re
from transformers import BartTokenizer, BartForConditionalGeneration
import google.generativeai as genai
import json

key = "AIzaSyB0h3PUL6aUTe_wNFqd-0H0fJceJzY4U-c"


class Gemini:
    def __init__(self):
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-pro')

    def summarize_bart(self, text):
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        summary_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

        inputs = tokenizer([f"summarize: {text}"], return_tensors="pt")
        summary_ids = summary_model.generate(
            inputs["input_ids"],
            max_length=50,
            min_length=10,
            early_stopping=True,
            num_beams=4,
            no_repeat_ngram_size=3
        )
        summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in
                   summary_ids]
        return summary[0].replace("summarize:", "").strip()

    def summarize_gemini(self, text):
        prompt = f"""I want you to summarize a review of a product.
                Some Noun keywords of the attributes of the product must be included in the summary as noun words.
                Prevent using any contrast words in the summary. If seeing one from the review, split it into two sentences.
                If the review talks about anything about shipping, include it in the summary.
                You also need to make sure that the summary is concise and informative.
                Do not make up any new noun words that are not in the review.
                Make sure each sentence in the summary must end with period.
                Make sure each sentence in the summary only talks about positive or negative attributes of the product.

                I will use the summary you generated to extract keywords of attributes of the product. If a sentence in the summary is not about the product or shipping, I will not be able to extract any keywords.

                Please provide the response with the summary only.

                Here is the review you need to summarize: {text}"""

        response = self.model.generate_content(prompt)
        return response.text

    def split_sentences(self, paragraph):
        pattern = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s"
        sentences = re.split(pattern, paragraph)
        return sentences

    def get_keywords(self, text):
        prompt = f"""I want you to detect the sentiment and extract keywords from the sentence i provided. 
        The sentence will be a review of a product. 
        
        For example, here is the positive review: "The product is truly exceptional in terms of both aesthetics and functionality". 
        You can see that the review is positive and user likes the aesthetics and functionality of the product. 
        So the keywords I want are Noun words like aesthetics and functionality.
        
        A negative review can be: "The delay in shipping and the poor handling of my queries about the status of the delivery left much to be desired.
        In this case, the user is not happy with the shipping and handling of the product. 
        So the keywords are shipping and handling.
        
        Remember, the keywords should only be related to the product itself instead of others like personal feelings.
        Only use the Noun words from the review. Do not make up any new words like converting adjectives or adverb to nouns.
        Ideally, the keyword you extracted better be a word instead of a phrase. Unless the phrase means something special.
        Extract only one keyword for a review unless the review has some "a and b" cases just like in the example positive review.

        Please provide the response with the following json format only:
        {{"sentiment": either positive or negative, "keywords": a list of the keywords extracted from the sentence}}
        
        Here is the review you need to analyze: {text}"""

        response = self.model.generate_content(prompt)
        return response.text

    def sentiment_detect(self, text):
        prompt = f"""I want you to detect the sentiment of a review of a product.
        
        Please provide the response in a single word: either positive or negative.
        
        Here is the review you need to detect: {text}"""

        response = self.model.generate_content(prompt)
        return response.text


    def analyze_review(self, text, bart=False):
        if bart:
            summary = self.summarize_bart(text)
        else:
            summary = self.summarize_gemini(text)
        sentences = self.split_sentences(summary)
        positive = []
        negative = []
        for sentence in sentences:
            response = self.get_keywords(sentence)
            response = json.loads(response)
            if response["sentiment"] == "positive":
                positive.extend(response["keywords"])
            else:
                negative.extend(response["keywords"])
        return positive, negative


