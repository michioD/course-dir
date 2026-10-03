import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

# 1. Read the predictions file
with open("predictions.txt", "r") as f:
    # Read lines, strip whitespace/newlines, and ignore empty lines
    preds = [line.strip() for line in f.readlines() if line.strip()]

# 2. Read the ground truth file
with open("EvaluationGT.csv", "r") as f:
    # Read lines, strip whitespace/newlines, and ignore empty lines
    gts = [line.strip() for line in f.readlines() if line.strip()]

# 3. Verify that both files have the same number of labels
print(f"Number of predictions: {len(preds)}")
print(f"Number of ground truths: {len(gts)}")

if len(preds) != len(gts):
    print("Warning: Lengths do not match! Truncating to the shorter file.")
    min_len = min(len(preds), len(gts))
    preds = preds[:min_len]
    gts = gts[:min_len]

# 4. Calculate overall accuracy
accuracy = accuracy_score(gts, preds)
print(f"Accuracy: {accuracy * 100:.2f}%\n")

# 5. Generate a detailed classification report
print("Classification Report:")
print(classification_report(gts, preds))
