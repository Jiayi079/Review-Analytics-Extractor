import json
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'model')))
from model.gemini import Gemini
from model.traditional import Traditional

import spacy

spacy.cli.download("en_core_web_md")

with open("product_review.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)

nlp = spacy.load('en_core_web_md')


def compare_similarity(word1, word2):
    similarity_score = nlp(word1).similarity(nlp(word2))
    return similarity_score > 0.7


def calculate_metrics(dataset, model):
    TP_positive = 0
    FP_positive = 0
    FN_positive = 0
    TP_negative = 0
    FP_negative = 0
    FN_negative = 0

    process = 0
    for review in dataset:
        process += 1
        print(process, "/", len(dataset))
        predicted_positive_tokens, predicted_negative_tokens = model.analyze_review(review["ReviewText"], False, False)
        actual_positive_tokens = set()
        actual_negative_tokens = set()
        for segment in review["Segments"]:
            if segment["Sentiment"] == "Positive":
                actual_positive_tokens.update(segment["Token"])
            elif segment["Sentiment"] == "Negative":
                actual_negative_tokens.update(segment["Token"])

        print("Predicted Positive Tokens:", predicted_positive_tokens)
        print("Actual Positive Tokens:", actual_positive_tokens)
        print("Predicted Negative Tokens:", predicted_negative_tokens)
        print("Actual Negative Tokens:", actual_negative_tokens)

        for token in predicted_positive_tokens:
            if any(compare_similarity(token, actual_token) for actual_token in actual_positive_tokens):
                TP_positive += 1
            else:
                FP_positive += 1

        for token in actual_positive_tokens:
            if not any(compare_similarity(token, predicted_token) for predicted_token in predicted_positive_tokens):
                FN_positive += 1

        for token in predicted_negative_tokens:
            if any(compare_similarity(token, actual_token) for actual_token in actual_negative_tokens):
                TP_negative += 1
            else:
                FP_negative += 1

        for token in actual_negative_tokens:
            if not any(compare_similarity(token, predicted_token) for predicted_token in predicted_negative_tokens):
                FN_negative += 1

    precision_positive = TP_positive / (TP_positive + FP_positive) if (TP_positive + FP_positive) > 0 else 0
    recall_positive = TP_positive / (TP_positive + FN_positive) if (TP_positive + FN_positive) > 0 else 0
    f1_score_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive) if (
                                                                                                                       precision_positive + recall_positive) > 0 else 0

    precision_negative = TP_negative / (TP_negative + FP_negative) if (TP_negative + FP_negative) > 0 else 0
    recall_negative = TP_negative / (TP_negative + FN_negative) if (TP_negative + FN_negative) > 0 else 0
    f1_score_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative) if (
                                                                                                                       precision_negative + recall_negative) > 0 else 0

    overall_precision = (precision_positive + precision_negative) / 2
    overall_recall = (recall_positive + recall_negative) / 2
    overall_f1_score = (f1_score_positive + f1_score_negative) / 2

    confusion_matrix = np.array([[TP_positive, FP_negative], [FN_positive, TP_negative]])

    return precision_positive, recall_positive, f1_score_positive, precision_negative, recall_negative, f1_score_negative, overall_precision, overall_recall, overall_f1_score, confusion_matrix


model = Gemini()
precision_positive, recall_positive, f1_score_positive, precision_negative, recall_negative, f1_score_negative, overall_precision, overall_recall, overall_f1_score, confusion_matrix = calculate_metrics(dataset, model)
print("Positive Tokens:")
print("Precision:", precision_positive)
print("Recall:", recall_positive)
print("F1-score:", f1_score_positive)
print("\nNegative Tokens:")
print("Precision:", precision_negative)
print("Recall:", recall_negative)
print("F1-score:", f1_score_negative)
print("\nOverall Metrics:")
print("Overall Precision:", overall_precision)
print("Overall Recall:", overall_recall)
print("Overall F1-score:", overall_f1_score)
print("\nConfusion Matrix:")
print(confusion_matrix)
