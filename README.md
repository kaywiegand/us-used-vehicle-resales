# US Used Vehicle Resales — Bad-Buy Prediction

> A classification model that predicts, **before purchase**, whether a used car bought at
> auction will turn out to be a "Bad Buy" — a lemon that cannot be resold — so a US used-car
> dealer can stop overpaying for vehicles that generate losses instead of margin.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Stack](https://img.shields.io/badge/Stack-scikit--learn%20·%20pandas-orange)
![Type](https://img.shields.io/badge/Type-Data%20Science%20·%20Classification-green)
![Status](https://img.shields.io/badge/Status-Portfolio%20WIP-yellow)

---

## TL;DR

- **Task:** binary classification of `IsBadBuy` on **65,620 auctioned vehicles** with **33 features**.
- **Hard part:** the classes are strongly **imbalanced** — only **12.35 %** of cars are bad buys, so accuracy is meaningless; the project optimizes the **F1 score of the bad-buy class**.
- **Best model:** Logistic Regression with L1 penalty (`class_weight='balanced'`) reaches **bad-buy F1 ≈ 0.37** on the held-out test set, up from a **0.29 baseline**. Tuning the decision threshold lifts it to **F1 ≈ 0.42 at precision ≈ 0.45**.
- **Strongest signal:** a **missing wheel-type** (`WheelType = Unknown`) is the single most predictive feature for a bad buy — a data-quality flag that doubles as a risk flag.
- **Deliverable:** scored predictions for **7,292 unlabeled vehicles** (`features_aim.csv`); at the deployment threshold ≈ **10 %** are flagged for review.
- **Rigor:** a reproducible [**data-leakage audit**](docs/DATA_LEAKAGE_AUDIT.md) clears the pipeline — no target leakage, no high-cardinality memorization. Verified on the **hidden holdout labels**: the champion generalizes with a 0.013 F1 gap and, at the tuned threshold, reaches **F1 0.409 on the true out-of-sample set** — clearing the original assessment's 0.40 bar that a mis-submitted baseline had missed. Experiments were logged with a self-built `ModelTracker` (448 runs).

![Class distribution of IsBadBuy](public/img/target_distribution.png)

*Class distribution: ~57,500 good buys vs ~8,100 bad buys — the core modeling challenge.*

---

## Where to start

| You are a… | Start here |
| :--- | :--- |
| Recruiter (30 s) | This README — TL;DR + Results |
| Data Scientist (10 min) | [`00_introduction.ipynb`](notebooks/00_introduction.ipynb) → [`01_exploring.ipynb`](notebooks/01_exploring.ipynb) |
| Modeling deep-dive | [`03a_modelling-logreg.ipynb`](notebooks/03a_modelling-logreg.ipynb) · [`03b_modelling-rf.ipynb`](notebooks/03b_modelling-rf.ipynb) |

---

## Problem Statement

A US used-car dealer buys vehicles cheaply at online auctions to resell them at a margin.
The biggest risk is a **"Bad Buy"** (a lemon): a car with severe defects that cannot be
resold and instead generates follow-up costs (storage, repairs, write-downs).

**Guiding question:** Can we predict before purchase whether an offer is a bad buy —
**without rejecting too many good cars**? This is a precision/recall trade-off on a rare
positive class, not an accuracy problem.

---

## Dataset

| | |
| :--- | :--- |
| Training data | `data/01_raw/data_train.csv` — **65,620 rows**, **33 columns**, `;`-separated, labeled |
| Scoring data | `data/01_raw/features_aim.csv` — **7,291 rows**, unlabeled (prediction target) |
| Target | `IsBadBuy` — `0` good buy (87.65 %), `1` bad buy (12.35 %) |
| Source | StackFuel capstone project (Module 3, Chapter 4) |

Full column reference → [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).

> Raw data and trained models are excluded from the repo via `.gitignore`.

---

## Approach

**1 · Exploration** ([`01_exploring.ipynb`](notebooks/01_exploring.ipynb)) — distributions,
missing values, and the strong class imbalance; price columns (MMR family) are highly
correlated.

![Feature correlations](public/img/feature_correlations.png)

**2 · Preparation** ([`02_processing.ipynb`](notebooks/02_processing.ipynb)) — cleaning,
feature engineering (price ratios, mileage-per-year, risk buckets), and a **stratified**
train/test split to preserve the 12.35 % bad-buy rate.

**3 · Modeling** ([`03a`](notebooks/03a_modelling-logreg.ipynb) ·
[`03b`](notebooks/03b_modelling-rf.ipynb)) — baseline Logistic Regression → L1 Logistic
Regression and Random Forest, all with `class_weight='balanced'` to counter the imbalance.
Decision threshold tuned on the F1 curve:

![Threshold tuning](public/img/threshold_f1_curve.png)

**4 · Evaluation** ([`04a`](notebooks/04a_evaluation-baseline.ipynb) ·
[`04b`](notebooks/04b_evaluation-logreg.ipynb)) — bad-buy precision/recall/F1 vs. the baseline.

---

## Results

Performance on the **bad-buy class** (the minority class that matters):

| Model | Recall | Precision | F1 (bad-buy) | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| Baseline — Logistic Regression (8 feat) | 0.61 | 0.19 | 0.29 | 0.67 |
| Random Forest (deep, balanced) | 0.64 | 0.24 | 0.35 | 0.75 |
| **Logistic Regression Lasso (L1, balanced)** | 0.60 | 0.27 | **0.37** | 0.77 |

<sub>All three on the **same held-out test set** (n = 13,124), threshold 0.5, selection metric =
F1 of the bad-buy class. Reproduced end-to-end in [`04_evaluation.ipynb`](notebooks/04_evaluation.ipynb).</sub>

![Model comparison on the held-out test set](public/img/model_comparison.png)

**Threshold tuning** — with balanced class weights the default 0.5 threshold over-flags. At the
F1-optimal threshold (0.65) the winning model reaches **F1 0.42 · Precision 0.45 · Recall 0.40**:

![Decision threshold vs. F1](public/img/threshold_f1_curve.png)

**Most predictive feature:** a **missing wheel type** (`WheelType = Unknown`) dominates the L1
coefficients, followed by specific ZIP regions, models and sub-models.

![Logistic Regression feature importance](public/img/logreg_feature_importance.png)

**Recommendation:** deploy the **L1 Logistic Regression** at the tuned threshold as a **triage
filter** — it flags ~10 % of an unlabeled batch for human review at ~0.45 precision, not as an
automatic reject. Treat missing `WheelType` as a first-order risk indicator at intake.

---

## Notebooks

| # | Notebook | Content |
| :--- | :--- | :--- |
| 00 | [`00_introduction.ipynb`](notebooks/00_introduction.ipynb) | Entry point: scenario, task, navigation |
| 01 | [`01_exploring.ipynb`](notebooks/01_exploring.ipynb) | Exploratory data analysis |
| 02 | [`02_processing.ipynb`](notebooks/02_processing.ipynb) | Cleaning, feature engineering, split |
| 03 | [`03_modelling-prep.ipynb`](notebooks/03_modelling-prep.ipynb) | Modeling setup |
| 03a | [`03a_modelling-logreg.ipynb`](notebooks/03a_modelling-logreg.ipynb) | Logistic Regression |
| 03b | [`03b_modelling-rf.ipynb`](notebooks/03b_modelling-rf.ipynb) | Random Forest |
| 04 | [`04_evaluation.ipynb`](notebooks/04_evaluation.ipynb) | **Results SSoT** — all models on the same held-out test, threshold tuning, scoring |
| 04a | [`04a_evaluation-baseline.ipynb`](notebooks/04a_evaluation-baseline.ipynb) | Baseline evaluation (exploratory) |
| 04b | [`04b_evaluation-logreg.ipynb`](notebooks/04b_evaluation-logreg.ipynb) | LogReg deployment walk-through (exploratory) |

---

## Tech Stack

Python 3.12 · pandas · NumPy · scikit-learn (Logistic Regression, Random Forest,
pipelines, `ColumnTransformer`) · Matplotlib / Seaborn · Jupyter · uv ·
[`wgnd`](https://github.com/kaywiegand/wgnd-toolkit) toolkit for EDA helpers.

Project code lives in the installable package `us_used_vehicle_resales`. Model experiments were
tracked with a **self-built `ModelTracker`** — a lightweight experiment logger that records
F1 / recall / precision / ROC-AUC per run to CSV, flags the best run, and exports the fitted
pipeline (448 runs across feature sets and model families).

> **Related work:** this project shares the `wgnd` toolkit and project scaffolding with
> [**zh-tram-flow**](https://github.com/kaywiegand/zh-tram-flow) — the portfolio's flagship
> end-to-end data-science project (a Zürich tram-delay prediction pipeline).

---

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e .            # add ".[dev]" for pytest/ruff/black
```

Then open the notebooks in reading order (start with `00_introduction.ipynb`).

```python
from us_used_vehicle_resales.cleaning import clean_data
from us_used_vehicle_resales.features import engineer_features
import us_used_vehicle_resales as wg     # ModelTracker, print_*, save_*, inspect_*
```

---

## Reports & Artifacts

| Artifact | Path | Content |
| :--- | :--- | :--- |
| Project hub | [`public/index.html`](public/index.html) | Self-contained overview: pitch, key charts, results table |
| Data dictionary | [`public/data-dictionary.html`](public/data-dictionary.html) · [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) | All 33 columns + known issues |
| Charts | [`public/img/`](public/img/) | Target distribution, correlations, feature importance, threshold curve |

## Author

**Kay Wiegand** · [GitHub](https://github.com/kaywiegand) · [LinkedIn](https://www.linkedin.com/in/kaywiegand/)
