# Results & Retrospective — US Used Vehicle Resales

> The full results of the bad-buy classification project, plus an honest retrospective:
> what worked, what the real failure was, and what it teaches. This document is the narrative
> spine for the portfolio case.

**Headline:** On the hidden out-of-sample set, the tuned champion reaches **bad-buy F1 0.409** —
clearing the original assessment's 0.40 bar. The project was historically marked as a failure not
because of the model, but because the **baseline was submitted at the default threshold**. A
rigorous audit shows **no data leakage and no overfitting**; the modeling was sound, the last-mile
submission was not.

---

## 1 · Objective

Predict, **before purchase**, whether a used car bought at auction will be a "Bad Buy" (a lemon that
can't be resold). The target `IsBadBuy` is strongly imbalanced — **12.35 %** positive — so accuracy
is meaningless and the project optimizes the **F1 score of the bad-buy class**. The assessment set a
bar of **F1 > 0.40** on a hidden scoring set (`features_aim`, 7 292 vehicles).

| | |
|:--|:--|
| Training data | 65 620 rows · 33 features · stratified train/test split (n_test = 13 124) |
| Scoring data | 7 292 vehicles, labels hidden at the time (`target_aim`, 863 bad buys) |
| Metric of record | F1 of the bad-buy (minority) class |
| Bar to clear | F1 > 0.40 |

---

## 2 · The modeling journey

1. **Baseline** — Logistic Regression on 8 hand-picked features (age, odometer, price anchors,
   two engineered ratios, auction, make). Establishes the floor.
2. **Systematic benchmark** — a self-built **`ModelTracker`** ran **448 experiments** across
   feature sets × model families (Logistic Regression ridge/lasso/elastic-net, Random Forest
   shallow/deep, HistGradientBoosting standard/aggressive), logging F1 / recall / precision /
   ROC-AUC per run, flagging the best and exporting the fitted pipeline.
3. **Champion** — **Logistic Regression with an L1 penalty** (`class_weight='balanced'`) on the
   full `all_in_with_noise` feature set. Two findings drove the choice:
   - **Categorical signal is essential:** dropping the categorical/engineered features collapses F1
     from ~0.38 to ~0.29. The market-price numerics alone are not enough.
   - **Consistent high recall (~0.60)** at modest precision — the right trade-off for a *triage*
     use case where missing a bad buy is costlier than a false alarm.
4. **Threshold tuning** — with balanced class weights the default 0.5 threshold over-flags. The
   F1-optimal operating point on the held-out test is **threshold ≈ 0.65**.

**A judgment call that aged well:** several Random Forest runs showed F1 > 0.40, but with recall
~0.3 and precision ~0.7 — useless for a triage filter that must *catch* bad buys. These were
correctly rejected in favour of the higher-recall Logistic Regression. Chasing the headline F1
there would have been the wrong call.

---

## 3 · Results

All models evaluated on the **same held-out test set** (n = 13 124), threshold 0.5 unless noted.
Reproduced end-to-end in [`notebooks/04_evaluation.ipynb`](../notebooks/04_evaluation.ipynb).

### 3.1 · Internal held-out test

| Model | Recall | Precision | F1 (bad-buy) | ROC-AUC |
|:------|:------:|:---------:|:------------:|:-------:|
| Baseline — Logistic Regression (8 feat) | 0.61 | 0.19 | 0.29 | 0.67 |
| Random Forest (deep, balanced) | 0.64 | 0.24 | 0.35 | 0.75 |
| **Logistic Regression Lasso (L1, balanced)** | 0.60 | 0.27 | **0.37** | 0.77 |
| Logistic Regression Lasso — **tuned threshold 0.65** | 0.40 | 0.45 | **0.42** | — |

### 3.2 · True holdout (AIM) — the decisive numbers

The hidden `target_aim.csv` was later recovered, so the models can be scored on the **true
out-of-sample labels** (7 292 vehicles, 863 bad buys).

**Pipeline-fidelity check** — the reproduced baseline matches the original examiner almost exactly,
which makes every number below trustworthy:

| Baseline on AIM | F1 | Confusion matrix |
|:----------------|:--:|:-----------------|
| Original examiner | 0.2810 | `[[4032, 2397], [330, 533]]` |
| Reproduced here | 0.2799 | `[[4029, 2400], [332, 531]]` |

**Champion on the true AIM labels** (threshold 0.65 chosen on the internal test, **not** on AIM):

| Threshold | F1 (bad-buy) | Precision | Recall | Flagged |
|:----------|:------------:|:---------:|:------:|:-------:|
| 0.50 | 0.360 | 0.26 | 0.59 | 26.8 % |
| **0.65 (tuned)** | **0.409** | **0.452** | 0.373 | 9.8 % |

The internal-test F1 (0.373) and the AIM F1 (0.360) at threshold 0.5 differ by only **0.013** — the
model generalizes almost perfectly. **At the tuned threshold the champion clears the 0.40 bar on the
real holdout (0.409).**

---

## 4 · Data-leakage investigation

Because the assessment bar wasn't met, data leakage was suspected and the project was shelved. A
reproducible audit ([`docs/DATA_LEAKAGE_AUDIT.md`](DATA_LEAKAGE_AUDIT.md)) checked every vector:

- **Split before feature engineering**, transformers fit on **train only**, **no target-derived
  features**, **zero duplicate rows** across the split → no classic leakage.
- **High-cardinality memorization tested directly:** removing 2 082 memorizable category levels
  (ZIP, model, sub-model) changes test F1 by only **0.003** → no overfitting.
- **Confirmed empirically:** the 0.013 internal→holdout gap on true out-of-sample data is the final
  proof that internal scores were never inflated.

**There was no leakage.**

---

## 5 · Root-cause — why the original score was 0.28

The historical failure was a **last-mile submission mistake**, not a modeling defect. Two
compounding errors:

| # | Mistake | Effect on F1 |
|:--|:--------|:-------------|
| 1 | **Baseline model submitted** instead of the LogReg Lasso champion | ~0.28 instead of ~0.36 |
| 2 | **Default threshold 0.5** instead of the tuned 0.65 | ~0.36 instead of ~0.41 |

Either fix alone would have moved the needle; both together are the difference between "failed" and
"0.409, passed". The modeling analysis had already identified the right champion — it simply didn't
make it into the exported predictions file, and the threshold was never applied to the submission.

The more expensive error was the **misdiagnosis afterwards**: concluding "leakage" and abandoning
the project, when the real cause was a cheap process slip.

---

## 6 · Lessons learned

1. **Threshold tuning is part of the deliverable, not an afterthought.** On an imbalanced target,
   the operating point is a first-class modeling decision — the single biggest lever here (0.36 → 0.41).
2. **Evaluate the *final chosen* model on one clean held-out test before shipping.** One number,
   one source of truth. The original confusion ("is RF 0.39 the best?") came from comparing
   validation scores across several tracking files instead of one final test.
3. **A high F1 with unusable recall is not a win.** Reading the full precision/recall picture, not
   the headline metric, was the right instinct — keep doing that.
4. **When a result disappoints, check the pipeline's last mile before blaming the data.** Verify
   *which* artifact was submitted before reaching for "leakage".
5. **The self-built `ModelTracker` was a genuinely good instinct** — systematic, logged, exportable.
   For production, know that MLflow / Weights & Biases do this off-the-shelf, so the trade-off can
   be named explicitly. The gap wasn't the tool; it was the missing single-source-of-truth test pass.

---

## 7 · Recommendations

- **Deploy the tuned LogReg Lasso (threshold 0.65)** as a **triage filter**: it flags ~10 % of an
  unlabeled batch at ~0.45 precision for human review — not an automatic reject.
- Treat a missing `WheelType` (`WheelType = Unknown`) as a **first-order risk flag at intake** — it
  is the single strongest predictor and doubles as a data-quality signal.
- Fold the two batch-level statistics (median imputation, `price_cat` quantile bins) into the fitted
  pipeline so single-record scoring is production-safe (see audit §2.5).

---

### Reproducibility

| Artifact | Location |
|:---------|:---------|
| Results SSoT (all numbers above) | [`notebooks/04_evaluation.ipynb`](../notebooks/04_evaluation.ipynb) |
| Leakage audit + experiments | [`docs/DATA_LEAKAGE_AUDIT.md`](DATA_LEAKAGE_AUDIT.md) |
| Model comparison / threshold / feature-importance charts | [`public/img/`](../public/img/) |

<sub>The hidden `target_aim.csv` is kept out of the repository (assessment ground truth); the true-holdout
numbers in §3.2 were computed locally against it.</sub>
