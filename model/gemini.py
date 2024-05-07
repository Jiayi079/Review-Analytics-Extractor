import re
import time

from transformers import BartTokenizer, BartForConditionalGeneration
import google.generativeai as genai
import json

key = ""


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
                If you find the word "shipping" in the review, include all the discussion about shipping in the summary. If you don't find it, ignore this rule.
                You also need to make sure that the summary is concise and informative.
                Any Noun words that are not in the review should not be included in the summary.
                Make sure each sentence in the summary must end with period.
                Make sure each sentence in the summary only talks about positive or negative attributes of the product.
                Ignore a sentence of the review if it doesn't include any informative Noun words about the product itself. (Don't count verbs, adjective, and adverbs)

                I will use the summary you generated to extract keywords of attributes of the product. If a sentence in the summary is not about the product or shipping, I will not be able to extract any keywords.

                Please provide the response with the summary only.

                Here is the review you need to summarize: {text}"""

        response = self.model.generate_content(prompt)
        return response.text


    def get_keywords(self, text):
        prompt = f"""I want you to extract keywords from the paragraph i provided. 
        The paragraph will be a review of a product. 
        
        For example, here is the positive review: "The product is truly exceptional in terms of both aesthetics and functionality". 
        You can see that the review is positive and user likes the aesthetics and functionality of the product. 
        So the keywords I want are Noun words like aesthetics and functionality.
        
        A negative review can be: "The delay in shipping and the poor handling of my queries about the status of the delivery left much to be desired.
        In this case, the user is not happy with the shipping and handling of the product. 
        So the keywords are shipping and handling.
        
        Remember, the keywords should only be related to the product.
        For example, if the review is "The washer can clean shirts very well", "shirts" is not a keyword because it is not a product attribute. This review doesn't have any keywords.
        If the review is "It's required to have some skills in order to use this product", "skills" is not a keyword because it is not a product attribute and "product" either since it's not informative. This review doesn't have any keywords.
        If the review is "It doesn't take a lot of space", "space" is a keyword because it is related to the product size.
        You can clearly find the what product it is from the review.
        
        The product name itself is not a keyword.
        Keywords must be a noun word. Ignore any other words like verbs, adjectives, adverbs, even if they are related to the product.
        Only use the Noun words from the review. Do not make up any new words like converting adjectives or adverb to nouns. (For example, don't convert perform well to performance)
        Ideally, the keyword you extracted better be a word instead of a phrase. Unless the phrase means something special.
        Extract less than or equal to keyword for one sentence unless it has some "a and b" cases just like in the example positive review.
        The keywords should not be a letter.
        If you can't find any keywords, just provide an empty list.
        

        Please provide the response with the following json format only:
        {{"positive": a list of the positive keywords you extracted, "negative": a list of the negative keywords you extracted}}
        
        Here is the review you need to analyze: {text}"""

        response = self.model.generate_content(prompt)
        return response.text.lower()

    def sentiment_detect(self, text):
        prompt = f"""I want you to detect the sentiment of a review of a product.
        
        Please provide the response in a single word: either positive or negative.
        
        Here is the review you need to detect: {text}"""

        response = self.model.generate_content(prompt)
        return response.text.lower()


    def analyze_review(self, text, summarize=True, bart=False):
        if summarize:
            if bart:
                review = self.summarize_bart(text)
            else:
                time.sleep(1)
                review = self.summarize_gemini(text)
        else:
            review = text

        positive = []
        negative = []
        response = self.get_keywords(review)
        try:
            response = json.loads(response)
        except:
            return positive, negative
        positive.extend(response["positive"])
        negative.extend(response["negative"])
        return positive, negative


