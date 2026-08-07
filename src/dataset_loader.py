import pandas as pd


# ----------------------------
# ISOT Dataset
# ----------------------------
def load_isot():

    fake = pd.read_csv("data/Fake.csv")
    real = pd.read_csv("data/True.csv")

    fake["label"] = 0
    real["label"] = 1

    fake["source"] = "ISOT"
    real["source"] = "ISOT"

    fake = fake[["title", "text", "label", "source"]]
    real = real[["title", "text", "label", "source"]]

    return pd.concat([fake, real], ignore_index=True)


# ----------------------------
# FakeNewsNet Dataset
# ----------------------------
def load_fakenewsnet():

    gc_fake = pd.read_csv("database/FakeNewsNet/gossipcop_fake.csv")
    gc_real = pd.read_csv("database/FakeNewsNet/gossipcop_real.csv")

    gc_fake["label"] = 0
    gc_real["label"] = 1

    gc_fake["source"] = "FakeNewsNet"
    gc_real["source"] = "FakeNewsNet"

    # FakeNewsNet only contains headlines
    gc_fake = gc_fake.rename(columns={"title": "text"})
    gc_real = gc_real.rename(columns={"title": "text"})

    gc_fake["title"] = ""
    gc_real["title"] = ""

    gc_fake = gc_fake[["title", "text", "label", "source"]]
    gc_real = gc_real[["title", "text", "label", "source"]]

    return pd.concat([gc_fake, gc_real], ignore_index=True)


# ----------------------------
# LIAR Dataset
# ----------------------------
def load_liar_dataset():

    train = pd.read_csv(
        "database/liar_dataset/train.tsv",
        sep="\t",
        header=None
    )

    valid = pd.read_csv(
        "database/liar_dataset/valid.tsv",
        sep="\t",
        header=None
    )

    test = pd.read_csv(
        "database/liar_dataset/test.tsv",
        sep="\t",
        header=None
    )

    liar = pd.concat(
        [train, valid, test],
        ignore_index=True
    )

    # Keep only label and statement
    liar = liar[[1, 2]]

    liar.columns = ["label", "text"]

    fake_labels = [
        "false",
        "barely-true",
        "pants-fire"
    ]

    liar["label"] = liar["label"].apply(
        lambda x: 0 if x in fake_labels else 1
    )

    liar["source"] = "LIAR"

    # LIAR doesn't have titles
    liar["title"] = ""

    liar = liar[["title", "text", "label", "source"]]

    return liar


# ----------------------------
# Merge All Datasets
# ----------------------------
def load_all_datasets():

    isot = load_isot()
    liar = load_liar_dataset()
    fakenewsnet = load_fakenewsnet()

    df = pd.concat(
        [isot, liar, fakenewsnet],
        ignore_index=True
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove missing text
    df = df.dropna(subset=["text"])

    # Remove empty text
    df = df[df["text"].str.strip() != ""]

    return df