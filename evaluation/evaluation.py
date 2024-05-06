import json
with open("product_review.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)

def calculate_metrics(dataset, model):
    TP_positive = 0
    FP_positive = 0
    FN_positive = 0
    TP_negative = 0
    FP_negative = 0
    FN_negative = 0

    for review in dataset:
        predicted_positive_tokens, predicted_negative_tokens = model.predict(review["ReviewText"])
        actual_positive_tokens = set()
        actual_negative_tokens = set()
        for segment in review["Segments"]:
            if segment["Sentiment"] == "Positive":
                actual_positive_tokens.update(segment["Token"])
            elif segment["Sentiment"] == "Negative":
                actual_negative_tokens.update(segment["Token"])
        for token in predicted_positive_tokens:
            if token in actual_positive_tokens:
                TP_positive += 1
            else:
                FP_positive += 1

        for token in actual_positive_tokens:
            if token not in predicted_positive_tokens:
                FN_positive += 1
        for token in predicted_negative_tokens:
            if token in actual_negative_tokens:
                TP_negative += 1
            else:
                FP_negative += 1

        for token in actual_negative_tokens:
            if token not in predicted_negative_tokens:
                FN_negative += 1

    precision_positive = TP_positive / (TP_positive + FP_positive) if (TP_positive + FP_positive) > 0 else 0
    recall_positive = TP_positive / (TP_positive + FN_positive) if (TP_positive + FN_positive) > 0 else 0
    f1_score_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive) if (precision_positive + recall_positive) > 0 else 0

    precision_negative = TP_negative / (TP_negative + FP_negative) if (TP_negative + FP_negative) > 0 else 0
    recall_negative = TP_negative / (TP_negative + FN_negative) if (TP_negative + FN_negative) > 0 else 0
    f1_score_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative) if (precision_negative + recall_negative) > 0 else 0

    overall_precision = (precision_positive + precision_negative) / 2
    overall_recall = (recall_positive + recall_negative) / 2
    overall_f1_score = (f1_score_positive + f1_score_negative) / 2

    return precision_positive, recall_positive, f1_score_positive, precision_negative, recall_negative, f1_score_negative, overall_precision, overall_recall, overall_f1_score

class MyModel:
    def predict(self, text):
        return ["aesthetics"], ["shipping", "communcation"]
    
model = MyModel()
precision_positive, recall_positive, f1_score_positive, precision_negative, recall_negative, f1_score_negative, overall_precision, overall_recall, overall_f1_score = calculate_metrics(dataset, model)
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
