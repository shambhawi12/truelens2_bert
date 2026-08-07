import pandas as pd
import matplotlib.pyplot as plt

# Model names
models = [
    "Logistic Regression",
    "SVM",
    "Random Forest"
]

# Accuracy values
accuracy = [
    0.8556308799114555,
    0.8575677919203099,
    0.8620641947980078
]

df = pd.DataFrame({
    "Model": models,
    "Accuracy": accuracy
})

plt.figure(figsize=(8,5))

plt.bar(df["Model"], df["Accuracy"])

plt.title("Model Accuracy Comparison")

plt.xlabel("Models")

plt.ylabel("Accuracy")

for i, value in enumerate(df["Accuracy"]):
    plt.text(i, value + 0.002, f"{value:.3f}", ha="center")

plt.ylim(0.80,0.90)

plt.tight_layout()

plt.savefig("results/accuracy_comparison.png")

plt.show()

print("✅ Accuracy graph saved successfully!")