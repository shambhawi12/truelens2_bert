<div align="center">

### AI-powered misinformation detection with evidence-backed verification

[![Model](https://img.shields.io/badge/%F0%9F%A4%97_Model-truthlens--distilbert-yellow?style=for-the-badge)](https://huggingface.co/shambhawi12/truthlens-distilbert)
[![Live App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://truelens2bert-kav4vm9cxepb3dqksuyhx2.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Accuracy](https://img.shields.io/badge/Model_Accuracy-94%25-brightgreen?style=for-the-badge)](https://huggingface.co/shambhawi12/truthlens-distilbert)

**🚀 Live Project:** [TrueLens](https://truelens2bert-kav4vm9cxepb3dqksuyhx2.streamlit.app/)

<br/>

> **"A prediction tells you what the model thinks. Evidence helps you understand why you should investigate further."**

</div>

---

## 🧭 What is TrueLens?

News moves quickly. Verification usually doesn't.

A headline can sound convincing. An article can look professional. A claim can be repeated across multiple platforms — without actually being well-supported.

**TrueLens was built around that gap.**

Most fake-news detectors stop at a single binary label:

```
❌  FAKE  /  ✅ REAL
```

TrueLens goes further — it asks:

```
❓ Has this claim been fact-checked before?
📰 Is related reporting available?
🛡️ Are trusted news sources covering something similar?
```

It combines a **multilingual DistilBERT classifier** with **Google Fact Check results** and **related-news evidence** — giving you context, not just a verdict.

---

## ✨ Key Features

| Feature Description        |                                                          |
| -------------------------- | -------------------------------------------------------- |
| 🤖 **ML Classification**   | Multilingual DistilBERT trained on 169,000+ articles     |
| 🔍 **Google Fact Check**   | Surfaces existing fact-check reviews for the claim       |
| 📰 **Related News Search** | Checks for related coverage across trusted sources       |
| 🔗 **URL Analysis**        | Paste a URL — TrueLens extracts and analyzes the article |
| 🌐 **Multilingual**        | Supports analysis of English and Hindi news content  |
| 📊 **Confidence Scores**   | Shows fake/real probabilities, not just a label          |

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         USER  INPUT                                 │
│                    📝 Text  ─ or ─  🔗 URL                         │
│                              │                                      │
│                              ▼                                      │
│                 ┌────────────────────────┐                          │
│                 │   Article Extraction   │  ← URL path only        │
│                 │   (Trafilatura)        │                          │
│                 └───────────┬────────────┘                          │
│                             │                                       │
│                             ▼                                       │
│                 ┌────────────────────────┐                          │
│                 │  Multilingual          │                          │
│                 │  DistilBERT Classifier │                          │
│                 │  English + Hindi       │                          │
│                 └────────┬───────────────┘                          │
│                          │                                          │
│              ┌───────────┴────────────┐                             │
│              ▼                        ▼                             │
│          FAKE / REAL            Confidence %                        │
│              │                                                      │
│              ▼                                                      │
│   ┌──────────────────────┐                                          │
│   │  Google Fact Check   │  → Rating · Publisher · Review URL      │
│   │  Tools API           │                                          │
│   └──────────┬───────────┘                                          │
│              │                                                      │
│              ▼                                                      │
│   ┌──────────────────────┐                                          │
│   │  Related News Search │  → Trusted source signal                │
│   │  (NewsAPI)           │                                          │
│   └──────────┬───────────┘                                          │
│              │                                                      │
│              ▼                                                      │
│   ┌────────────────────────────────────────────────────┐            │
│   │                     RESULT                         │            │
│   │                                                    │            │
│   │   Prediction   Confidence   Fact-check   Coverage  │            │
│   └────────────────────────────────────────────────────┘            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 The Model

TrueLens uses **`distilbert-base-multilingual-cased`** fine-tuned on a combined dataset of English and Hindi misinformation articles.

> 🤗 Model hosted on Hugging Face: [`shambhawi12/truthlens-distilbert`](https://huggingface.co/shambhawi12/truthlens-distilbert)

### Training Configuration

| Parameter Value     |                               |
| ------------------- | ----------------------------- |
| Base Model          | DistilBERT Multilingual Cased |
| Training Languages  | English + Hindi               |
| Max Sequence Length | 128 tokens                    |
| Batch Size          | 16                            |
| Learning Rate       | 2e-5                          |
| Optimizer           | AdamW                         |
| Epochs              | 3                             |
| Data Split          | 80 / 10 / 10                  |
| Hardware            | Kaggle T4 × 2                 |
| Gradient Clipping   | 1.0                           |
| Warmup              | 10%                           |

---

## 📚 Training Data

The model was trained on a combined corpus of ~169,000 articles across English and Hindi.

```
┌─────────────────────────────────────────────────────┐
│  Dataset                      │  Articles            │
│─────────────────────────────────────────────────────│
│  Fake.csv + True.csv          │  77,617              │
│  FakeNewsNet                  │  ~23,000             │
│  LIAR                         │  12,836              │
│  HinFakeNews V1               │  68,754              │
│─────────────────────────────────────────────────────│
│  Total                        │  ~169,576            │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Model Performance

Evaluated on an unseen test set of **14,120 articles**.

### Overall Metrics

```
  Accuracy   ████████████████████  94%
  Precision  ████████████████████  94%
  Recall     ████████████████████  94%
  F1 Score   ████████████████████  94%
  ROC-AUC                          0.989
```

### Class-Level Results

| Class Precision Recall F1  |     |     |     |
| -------------------------- | --- | --- | --- |
| 🔴 Fake                    | 95% | 92% | 93% |
| 🟢 Real                    | 93% | 95% | 94% |

> ⚠️ These metrics reflect performance on the project's evaluation data and should not be interpreted as a guarantee of accuracy on arbitrary real-world news.

---

## 🔍 Verification Signals

TrueLens treats the classifier as **one input** in a broader workflow — not the final word.

### 1 · Google Fact Check

Queries the Google Fact Check Tools API and surfaces existing claim reviews.

Extracted per result:

- Claim text
- Fact-check rating (`false`, `misleading`, `true`, `accurate`, etc.)
- Publishing organization
- Original review URL

### 2 · Related News Coverage

Searches for related articles and checks them against a configured list of trusted sources:

```
Reuters       BBC           Associated Press    NDTV
The Hindu     Times of India    India Today
Bloomberg     Al Jazeera        AFP
```

Matching trusted-source coverage is surfaced as a verification signal — not absolute proof.

> 🔑 **Important:** Absence of evidence is not evidence of absence. A claim with no matching fact-check may still be accurate.

---

## 🖥️ Application

Built as an interactive **Streamlit** app with a custom UI.

> **Example interface layout — values shown below are illustrative.**

```
┌──────────────────────────────────────────────────────┐
│  🔎 TrueLens                                         │
│──────────────────────────────────────────────────────│
│                                                      │
│  [ Paste article text or URL here...           ]     │
│                                                      │
│                         [ Analyze ]                  │
│                                                      │
│──────────────────────────────────────────────────────│
│  Prediction      Confidence     Fact-check  Sources  │
│  🔴 FAKE         87.3%          ✅ Found    3 / 10   │
│──────────────────────────────────────────────────────│
│  📋 Fact-check: "False" — Reuters Fact Check        │
│  🔗 https://...                                      │
│                                                      │
│  📰 Related articles found in trusted sources        │
└──────────────────────────────────────────────────────┘
```

The interface supports:

- Text-based and URL-based analysis
- Prediction with confidence/probability breakdown
- Fact-check results with source attribution
- Related news evidence panel
- Verification notes

---

## 🏗️ Project Structure

```
TrueLens/
│
├── 📄 app.py                    ← Main Streamlit application
├── 📄 server.py                 ← Supporting server functionality
├── 🎨 truthlens_styles.py       ← Custom interface styling
│
├── src/
│   ├── dataset_loader.py        ← Dataset loading utilities
│   ├── preprocessing.py         ← Data preprocessing
│   ├── train.py                 ← Model training pipeline
│   ├── predict.py               ← Model inference + fact-check integration
│   ├── scraper.py               ← Article extraction from URLs
│   ├── keyword_extractor.py     ← Keyword extraction (YAKE)
│   ├── news_search.py           ← Related-news retrieval
│   └── source_checker.py        ← Trusted source verification
│
├── experiments/
│   ├── compare_models.py
│   ├── plot_accuracy.py
│   ├── plot_confusion_matrix.py
│   ├── train_random_forest.py
│   └── train_svm.py
│
├── results/
│   ├── accuracy_comparison.png
│   ├── confusion_matrix_rf.png
│   └── model_comparison.csv
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

<table> <tr> <td><b>ML & NLP</b></td> <td>Python · PyTorch · Hugging Face Transformers · DistilBERT Multilingual · Scikit-learn · NumPy</td> </tr> <tr> <td><b>Data & Text</b></td> <td>Pandas · NLTK · YAKE (keyword extraction) · Trafilatura (article scraping) · Requests</td> </tr> <tr> <td><b>Verification & APIs</b></td> <td>Google Fact Check Tools API · NewsAPI</td> </tr> <tr> <td><b>Application</b></td> <td>Streamlit · Custom CSS</td> </tr> <tr> <td><b>Deployment</b></td> <td>Hugging Face Hub (model) · Streamlit Cloud (app) · GitHub</td> </tr> </table>

---

## 🚀 Getting Started

### 1 · Clone the repository

```bash
git clone https://github.com/shambhawi12/truelens2_bert.git
cd truelens2_bert
```

### 2 · Create a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Configure API keys

Create a `.env` file in the project root:

```env
GOOGLE_FACT_CHECK_API_KEY=your_google_fact_check_api_key
```

> ⚠️ Never commit `.env` files or API keys to GitHub. The repository's `.gitignore` excludes them by default.

### 5 · Run the application

```bash
streamlit run app.py
```

The app will be available at the local URL shown in your terminal.

---

## ☁️ Model Loading

The trained model is hosted on Hugging Face and loaded at startup:

```
Hugging Face Hub
      ↓
  Tokenizer + Weights
      ↓
  Application Memory  (cached — loaded once per session)
      ↓
  Inference
```

Model loading is cached so it doesn't re-download on every prediction.

---

## 🧪 Experiments

Before landing on the transformer approach, the project benchmarked classical ML baselines:

| Experiment File        |                                        |
| ---------------------- | -------------------------------------- |
| Random Forest          | `experiments/train_random_forest.py`   |
| Support Vector Machine | `experiments/train_svm.py`             |
| Model Comparison       | `experiments/compare_models.py`        |
| Accuracy Visualization | `experiments/plot_accuracy.py`         |
| Confusion Matrix       | `experiments/plot_confusion_matrix.py` |

Results are preserved under `results/` as a record of the project's evolution.

---

## ⚠️ Known Limitations

TrueLens is a **research and educational prototype**, not an authoritative fact-checking system.

| Limitation Details        |                                                                                  |
| ------------------------- | -------------------------------------------------------------------------------- |
| 🤖 **Model Boundaries**   | Satire, manipulated context, and out-of-distribution claims may be misclassified |
| 🌐 **Article Extraction** | JavaScript-heavy or paywalled pages may not extract reliably                     |
| 🔍 **Evidence Gaps**      | A true claim may have no matching fact-check — absence of evidence ≠ falsehood   |
| 🗣️ **Multilingual Gap**  | English performance outpaces Hindi; other languages are less tested              |
| 🔌 **API Dependency**     | Fact-check and news features depend on external API availability and quotas      |

---

## 🛣️ Future Directions

- [ ] **Claim-level NLI** using DeBERTa-v3 for finer-grained entailment checking
- [ ] **Richer article extraction** via headless browser automation
- [ ] **Unverified state** — a third label distinct from FAKE / REAL for low-confidence cases
- [ ] **Improved Hindi support** with MuRIL and additional multilingual data
- [ ] **Browser extension** for in-page verification while reading news
- [ ] **Broader language coverage** beyond English and Hindi
- [ ] **News portal / social platform integration**

---

## 🎯 Who Is This For?

TrueLens is designed to support:

- 🎓 **Students & Researchers** exploring NLP and misinformation detection
- 📰 **Journalists & Editors** doing preliminary claim checks
- 🧑‍💻 **Developers** building on top of multilingual transformers
- 👤 **General readers** who want more context before sharing something

It is intended to **encourage verification and critical reading** — not replace them.

---

## 👥 Contributors

<table>
<tr>
<td align="center">

<b>Shambhawi & Samiksha Verma</b><br/>

Project development · ML/NLP · Application development · Verification pipeline · Experimentation · Documentation

</td>
</tr>
</table>

TrueLens was developed collaboratively as a practical project focused on real-world misinformation detection and verification.

---

## 📄 Disclaimer

TrueLens is a research and educational project. Its predictions and verification results are **preliminary assessments** and may be incorrect or incomplete. External APIs may return incomplete, outdated, or unavailable information.

> Do not use TrueLens as the sole basis for publishing, sharing, or making consequential decisions about the authenticity of a news claim. Always verify important information using multiple reliable and independent sources.

---

<div align="center"> 

```
🔎 TrueLens
READ. ANALYZE. VERIFY.
```

*An exploratory step toward more informed digital reading.*

</div>