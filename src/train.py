import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from src.preprocessing import clean_text
from src.dataset_loader import load_all_datasets


# ----------------------------------
# Load all datasets
# ----------------------------------

df = load_all_datasets()

print("\nDatasets Loaded Successfully!")
print(df["source"].value_counts())


# ----------------------------------
# Keep only required columns
# ----------------------------------

df = df[["text", "label"]]


# ----------------------------------
# Remove missing values & duplicates
# ----------------------------------

df = df.dropna(subset=["text"])
df = df.drop_duplicates()


# ----------------------------------
# Clean text
# ----------------------------------

print("\nCleaning text...")

df["text"] = df["text"].apply(clean_text)


# Save cleaned dataset (optional)

df.to_csv(
    "data/fake_news_cleaned.csv",
    index=False
)


# ----------------------------------
# Features & Labels
# ----------------------------------

X_text = df["text"]
y = df["label"]


# ----------------------------------
# TF-IDF Vectorization
# ----------------------------------

vectorizer = TfidfVectorizer(
    max_features=5000
)

X = vectorizer.fit_transform(X_text)


# ----------------------------------
# Train-Test Split
# ----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ----------------------------------
# Train Logistic Regression
# ----------------------------------

print("\nTraining Logistic Regression...")

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train,
    y_train
)


# ----------------------------------
# Evaluation
# ----------------------------------

y_pred = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))


# ----------------------------------
# Save Model
# ----------------------------------

joblib.dump(
    model,
    "models/fake_news_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/vectorizer.pkl"
)

print("\n✅ Logistic Regression model saved successfully!")