import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from src.preprocessing import clean_text
from src.dataset_loader import load_all_datasets

# ------------------------
# Load dataset
# ------------------------

df = load_all_datasets()

df = df.dropna()
df = df.drop_duplicates()

df["text"] = df["text"].apply(clean_text)

X_text = df["text"]
y = df["label"]

vectorizer = TfidfVectorizer(max_features=5000)

X = vectorizer.fit_transform(X_text)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ------------------------
# Load Random Forest model
# ------------------------

model = joblib.load("models/random_forest_model.pkl")

# ------------------------
# Plot confusion matrix
# ------------------------

ConfusionMatrixDisplay.from_estimator(
    model,
    X_test,
    y_test,
    cmap="Blues"
)

plt.title("Random Forest Confusion Matrix")

plt.savefig("results/confusion_matrix_rf.png")

plt.show()

print("✅ Confusion Matrix Saved!")