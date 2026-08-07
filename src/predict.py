import joblib
from src.preprocessing import clean_text

# Load model only once
model = joblib.load("models/fake_news_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def predict_news(text: str):
    """
    Predict whether a news article is Fake or Real.
    """

    cleaned_text = clean_text(text)

    transformed_text = vectorizer.transform([cleaned_text])

    prediction = model.predict(transformed_text)[0]

    probability = model.predict_proba(transformed_text)[0]

    fake_probability = round(probability[0] * 100, 2)
    real_probability = round(probability[1] * 100, 2)

    confidence = round(max(probability) * 100, 2)

    label = "FAKE" if prediction == 0 else "REAL"

    return {
        "label": label,
        "confidence": confidence,
        "fake_probability": fake_probability,
        "real_probability": real_probability,
    }