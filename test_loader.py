from src.dataset_loader import load_all_datasets

df = load_all_datasets()

print(df.head())

print("\nColumns:")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nDataset Sources:")
print(df["source"].value_counts())