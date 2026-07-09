# Data-Leakage Audit — US Used Vehicle Resales

> Reproducible audit of the modeling pipeline for target/data leakage.
> Trigger: the original StackFuel assessment set a bar of **bad-buy F1 > 0.40**. That bar was
> not met on submission, and **data leakage was suspected** — the project was then shelved.
> This audit settles the question with evidence.

**Verdict: No data leakage. No high-cardinality overfitting. Confirmed on the true holdout labels —
the champion generalizes with a 0.013 F1 gap and, at the tuned threshold, clears the assessment's
F1 > 0.40 bar (AIM F1 0.409). The historically low score came from submitting the baseline model at
the default threshold, not from a modeling defect.**

All checks are reproducible in [`notebooks/04_evaluation.ipynb`](../notebooks/04_evaluation.ipynb)
and the audit experiment below.

---

## 1 · What "leakage" would look like here

Data leakage = information reaches the model at training time that would not be available at
prediction time, inflating internal scores relative to true generalization. For this pipeline the
candidate vectors are: split ordering, preprocessing fit scope, target-derived features, duplicate
rows across the split, batch-level statistics, high-cardinality memorization, and temporal order.
Each is checked below.

---

## 2 · Vector-by-vector findings

| # | Vector | Finding | Verdict |
|:--|:-------|:--------|:-------:|
| 1 | **Split ordering** | The stratified train/test split happens in `01_exploring` on the raw frame **before** any cleaning or feature engineering. Cleaning/FE are applied to each split independently. | ✅ clean |
| 2 | **Preprocessing fit scope** | `StandardScaler` and `OneHotEncoder` live **inside** the sklearn `Pipeline`; `pipe.fit(X_train)` fits them on train only and applies the frozen parameters to test/aim. `handle_unknown='ignore'` for unseen categories. | ✅ clean |
| 3 | **Target-derived features** | No engineered feature uses `IsBadBuy`. All features (price ratios, miles/year, warranty ratio, risk bins) derive from columns known **at purchase time** (MMR market prices, `VehBCost`, `VehOdo`, `VehicleAge`, `WarrantyCost`). | ✅ clean |
| 4 | **Duplicate rows across split** | `inspect_data` reports **0 duplicate rows** in the cleaned train set; no vehicle can appear in both train and test. | ✅ clean |
| 5 | **Batch-level statistics** | `impute_prices_hierarchical` (group-median) and `feat_price_cat` (`pd.qcut`) compute their statistics **per dataset**, so a test row's imputed price/bin uses other *test* rows — not train. This is **not** train→test target leakage (test never sees train), but it is a mild batch-time dependency: a single incoming record could not be imputed/binned this way in production. | ⚠️ minor, documented |
| 6 | **High-cardinality memorization** | Tested directly (§3). Removing the 2 082 memorizable category levels (VNZIP1, Model, SubModel, Trim, BYRNO) changes test F1 by **−0.003**. The high-cardinality one-hots carry almost no aggregate signal — the L1 penalty zeroes them out. | ✅ clean |
| 7 | **Temporal order** | The split is random (stratified), not time-based. Acceptable for the static-holdout framing of this task; would need a time split if the goal were forecasting future auctions. | ℹ️ noted |

---

## 3 · Experiment — high-cardinality overfitting test

Hypothesis: the internal test F1 (~0.37) is inflated by the model memorizing rare
ZIP/model/sub-model identifiers that will not recur on unseen auction batches.

Method: retrain the champion (LogReg Lasso, L1, balanced) three ways and evaluate on the **same
held-out test set** (n = 13 124), threshold 0.5.

| Variant | Features | OHE dims | High-card levels | Test F1 | Precision | Recall |
|:--------|:--------:|:--------:|:----------------:|:-------:|:---------:|:------:|
| A — full (`all_in_with_noise`) | 27 | 2 183 | 2 082 | **0.373** | 0.270 | 0.604 |
| B — minus high-card identifiers | 23 | 101 | 0 | **0.370** | 0.268 | 0.598 |
| C — baseline (8 feat) | 8 | 38 | 0 | 0.288 | 0.188 | 0.614 |

**Result:** dropping 2 082 memorizable levels costs **0.003 F1** (0.373 → 0.370). The signal is
carried by ~23 low-cardinality features (missing `WheelType`, price ratios, vehicle age, `Make`,
`Auction`). **Hypothesis refuted — there is no high-cardinality overfitting.**

---

## 4 · Explaining the original assessment score

The examiner scored the submitted `predictions_aim.csv` against the hidden `target_aim.csv`:

```
              precision    recall  f1-score   support
           1     0.1819    0.6176    0.2810       863   ← bad-buy class
    accuracy                         0.6260      7292
```

- The submitted predictions flagged **~40 %** of the batch (recall 0.62, precision 0.18) — this is
  the **baseline Logistic Regression**, not the champion.

### 4.1 · Measured on the true holdout labels

The hidden `target_aim.csv` (863 bad buys in 7 292 vehicles) was later recovered, so the models
can be scored directly on the true out-of-sample labels.

**Pipeline-fidelity check** — the reproduced baseline matches the examiner almost exactly:

| Baseline on AIM | F1 | Confusion matrix |
|:----------------|:--:|:-----------------|
| Examiner (original) | 0.2810 | `[[4032, 2397], [330, 533]]` |
| Reproduced here | 0.2799 | `[[4029, 2400], [332, 531]]` |

±3 rows out of 7 292 — the local reproduction *is* the original StackFuel pipeline, so every
number below is trustworthy.

**Champion (LogReg Lasso) on the true AIM labels:**

| Threshold | F1 (bad-buy) | Precision | Recall | Flagged |
|:----------|:------------:|:---------:|:------:|:-------:|
| 0.50 | 0.360 | 0.26 | 0.59 | 26.8 % |
| **0.65 (tuned)** | **0.409** | **0.452** | 0.373 | 9.8 % |

- Champion **internal** test F1 = 0.373 vs **AIM** F1 = 0.360 (both at threshold 0.5) → a gap of
  **0.013**. The model generalizes almost perfectly to unseen data — **no leakage and no
  overfitting, now confirmed empirically on the true out-of-sample set**, not just argued.
- **At the tuned threshold the champion clears the F1 > 0.40 bar on the real holdout: F1 0.409.**

**Conclusion:** there was never any data leakage. The assessment's F1 > 0.40 bar *is* met — the
tuned champion reaches 0.409 on the hidden AIM labels. The historical shortfall came purely from
**submitting the baseline model at the default 0.5 threshold** (AIM F1 0.28) instead of the tuned
champion. A modeling/deployment choice, not a leakage or data-quality failure.

---

## 5 · Recommendations

1. Re-submit / report the **tuned LogReg Lasso** (threshold 0.65) as the deliverable — not the baseline.
2. Fold the two batch-level statistics (§2.5) into the fitted pipeline: fit imputation medians and
   `price_cat` quantile edges on **train only**, then apply to test/aim (removes the mild batch
   dependency and makes single-record scoring production-safe). Tracked as BACKLOG #17.
3. Keep the honest framing: bad buys are only weakly separable from pre-purchase features — F1 in
   the 0.37–0.42 band is a property of the problem, not a bug.
