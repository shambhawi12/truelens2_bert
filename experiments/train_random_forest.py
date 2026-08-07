import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from src.preprocessing import clean_text
from src.dataset_loader import load_all_datasets


# ----------------------------------
# Load datasets
# ----------------------------------

df = load_all_datasets()

print("\nDatasets Loaded Successfully!")
print(df["source"].value_counts())


# ----------------------------------
# Keep only required columns
# ----------------------------------

df = df[["text", "label"]]

df = df.dropna(subset=["text"])
df = df.drop_duplicates()

print("\nCleaning text...")

df["text"] = df["text"].apply(clean_text)


# ----------------------------------
# Features & Labels
# ----------------------------------

X_text = df["text"]
y = df["label"]


# ----------------------------------
# TF-IDF
# ----------------------------------

vectorizer = TfidfVectorizer(max_features=5000)

X = vectorizer.fit_transform(X_text)


# ----------------------------------
# Train Test Split
# ----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ----------------------------------
# Train Random Forest
# ----------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


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
    "models/random_forest_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/vectorizer.pkl"
)

print("\n✅ Random Forest model saved successfully!")