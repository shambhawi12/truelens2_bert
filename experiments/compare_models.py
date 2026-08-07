import pandas as pd

results = {
    "Model": [
        "Logistic Regression",
        "SVM",
        "Random Forest"
    ],
    "Accuracy": [
        0.8556308799114555,
        0.8575677919203099,
        0.8620641947980078
    ]
}

df = pd.DataFrame(results)

print("\n===== MODEL COMPARISON =====\n")
print(df)

best = df.loc[df["Accuracy"].idxmax()]

print("\n🏆 Best Model")
print(best)

df.to_csv("results/model_comparison.csv", index=False)

print("\n✅ Comparison saved to results/model_comparison.csv")