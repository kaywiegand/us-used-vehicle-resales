# Portfolio Summary — US Used Vehicle Resales
<!-- Interface-Datei: Wird von /project-case story befüllt.
     Einzige Zahlenquelle für /project-case report und /project-case slides.
     KEINE Inhalte aus Notebooks kopieren — nur kuratierte Kernaussagen.
-->

---

## Project

```
name:       US Used Vehicle Resales — Bad-Buy Prediction
slug:       us-used-vehicle-resales
type:       DS (classification)
stage:      Phase 5 — Re-Review & Case Study, /project-case check passed, story done
target:     IsBadBuy (binary — lemon that cannot be resold)
stack:      Python · pandas · scikit-learn · Matplotlib/Seaborn · Jupyter · uv
period:     StackFuel Capstone
rows:       65,620 training rows + 7,292 hidden scoring rows (features_aim)
notebooks:  12
findings:   4
dashboard:  — (static notebook + report project, no live dashboard)
```

---

## Storyline

```
thesis:     Casting a wide net beats hand-picking. A full feature catalog, tested systematically
            rather than guessed at, surfaces a counter-intuitive top predictor that a "sensible"
            hand-picked feature set would never have included — and the model still needs its
            operating point tuned to the business decision, not left at a generic default.
hook:       The single strongest predictor in the champion model is WheelType = Unknown — a
            missing-data flag, not a real vehicle attribute, carrying almost no information
            content on its own. It only surfaces because the full feature catalog was tested,
            not just the "obviously relevant" columns.
proof:      4-step chain: (1) a self-built ModelTracker + feature/model catalogs ran 448 logged
            experiments across 19 feature sets × 6 model families instead of one hand-picked
            attempt, (2) the numeric-only set (6 features) tops out at F1 0.29 while the full
            catalog (28 features, adding the categoricals `01_exploring` had flagged as
            high-risk niches) reaches F1 0.37 — consistently, across model families, (3) among
            those features, the unassuming missing-data flag `WheelType = Unknown` dominates the
            champion's coefficients, (4) tuning the decision threshold for the triage business
            context (catch bad buys, don't reject too many good cars) lifts F1 from 0.37 to 0.42.
so_what:    Don't pre-filter features by assumed importance — cast the net wide and let
            systematic, logged experimentation surface the signal. Then tune the operating point
            to the actual business decision, not to a textbook 0.5 default.
```

---

## Problem

```
kpi_name:   Bad-buy F1 (minority-class F1 on IsBadBuy, internal held-out test)
kpi_ist:    0.42 (full catalog + tuned threshold)
kpi_soll:   0.29 (hand-picked baseline feature set, default threshold)
kpi_gap:    +0.13 F1 from casting a wider feature net + tuning the threshold
problem_statement: |
  A US used-car dealer buys vehicles cheaply at auction to resell at a margin. The biggest risk
  is a "Bad Buy" — a lemon with severe defects that cannot be resold and instead generates
  storage, repair and write-down costs. With only 12.35 % of auctioned cars being bad buys,
  accuracy is meaningless; the task is a precision/recall trade-off on a rare positive class,
  and the model must catch it *before* purchase, not after.
```

---

## Key Findings
<!-- Max 6 Findings — jeweils mit konkreter Zahl und Quelle-Notebook -->

### F1 — Systematic, logged experimentation instead of guessing
```
finding:   A self-built ModelTracker paired with a feature catalog (19 named feature sets) and a
           model catalog (6 model families) ran 448 logged experiments — every run's F1, recall,
           precision and ROC-AUC captured, best run flagged, model exported automatically.
number:    448 logged runs · 19 feature sets × 6 model families
source:    05_experiment_framework.ipynb
```

### F2 — A broad feature catalog beats a "numbers-only" one
```
finding:   Across the 448 tracked runs, the numeric-only feature set (6 features: price, age,
           odometer) tops out at F1 0.2918. The full catalog (28 features, adding categoricals
           like Trim/SubModel/VNZIP1/WheelType) reaches F1 0.3726 — and this gap holds across
           model families, not just one lucky run. `01_exploring.ipynb`'s own bivariate risk
           analysis had flagged these categorical columns as "high-risk niches" worth including;
           the systematic sweep is the proof that hypothesis paid off.
number:    F1 0.2918 (6 numeric features) → 0.3726 (28-feature full catalog), best run per set
source:    data/04_models/model_results_tracking.csv (448 runs) · 01_exploring.ipynb · 05_experiment_framework.ipynb
```

### F3 — The single strongest signal is a near-empty data field
```
finding:   WheelType is filled in normally for 95.6 % of vehicles (Alloy 49.3 % / Covers 45.3 % /
           Special 1.0 %, bad-buy rates 8–13 %, close to the 12.3 % base rate — unremarkable on
           its own). But in the 4.4 % of cases where it's simply missing, 70.3 % are bad buys —
           ~6x the base rate. That rare "field is empty" case is the single most predictive
           signal among the champion's 27 features, well ahead of price or age. It goes one step
           further than `01_exploring.ipynb`'s own hypothesis, which flagged WheelType as
           informative because wheel *material* (Alloy vs. Steel) proxies the car's original
           price class — the actual top signal isn't the material, it's the absence of an entry.
number:    4.4 % missing (2,877 / 65,620 cars) → 70.3 % bad-buy rate vs. 12.3 % base rate
source:    data/01_raw/data_train.csv · 04_evaluation.ipynb · 01_exploring.ipynb
```

### F4 — Threshold tuning, balanced for the business context
```
finding:   With balanced class weights the default 0.5 threshold over-flags. Tuning the decision
           threshold to the triage use case (catch bad buys without rejecting too many good
           cars) lifts the champion from F1 0.37 to F1 0.42 — precision 0.45 / recall 0.40 at the
           chosen operating point.
number:    F1 0.37 → 0.42 (threshold 0.5 → 0.65)
source:    04_evaluation.ipynb
```

---

## Model Results

```
algorithm:      Logistic Regression, L1/Lasso penalty (class_weight='balanced')
target:         IsBadBuy
metric:         F1 of the bad-buy (minority) class
split_strategy: stratified train/test split (12.35 % bad-buy rate preserved)
train_rows:     52,496
val_rows:       — (systematic benchmark used its own internal validation split; see below)
test_rows:      13,124
```

### Baseline Benchmark

| Model | Logic | Metric |
|---|---|---|
| Naive majority class | Always predict "good buy" | F1 undefined (0 recall on bad-buy class) |
| Numeric-only feature set (6 feat, best of family) | Price/age/odometer only, no categoricals | F1 0.29 (best tracked run, `model_results_tracking.csv`) |
| **Baseline — Logistic Regression (8 feat)** | **Hand-picked features (age, odometer, price anchors, 2 ratios, auction, make), default threshold** | **F1 0.29 (test) ← floor** |

### Model Progression

| Model | Features | Test Metric | vs. Baseline | Data Requirement |
|---|---|---|---|---|
| Baseline LogReg | 8 | F1 0.29 | — | Age, odometer, price anchors, ratios, auction, make |
| Random Forest (deep, balanced) | 27 | F1 0.35 | +0.06 | + full categorical/engineered feature set |
| LogReg Lasso (L1, balanced) | 27 | F1 0.37 | +0.08 | Same feature set, L1 regularization |
| **LogReg Lasso @ tuned threshold 0.65** | 27 | **F1 0.42** | **+0.13** | + threshold tuning on the F1 curve |

```
best_model:     Logistic Regression, L1/Lasso, class_weight='balanced', threshold 0.65
best_metric:    F1 0.42 (internal held-out test, tuned threshold)
key_insight:    The strongest single predictor (WheelType = Unknown) is a missing-data flag, not
                a substantive feature — it only surfaced by testing the full catalog, not a
                hand-picked subset
mbe:            n/a — classification task (F1/precision/recall, no bias-error metric)
```

---

## Figures
<!-- Alle relevanten Exports in public/img/ — für Report und Slides -->

```yaml
data:
  - img/target_distribution.png       # class imbalance: ~57.5k good vs. ~8.1k bad buys
  - img/feature_correlations.png      # MMR price-family features are highly correlated

model:
  - img/model_comparison.png          # baseline vs. RF vs. LogReg Lasso on held-out test
  - img/threshold_f1_curve.png        # F1 vs. decision threshold, tuned optimum at 0.65
  - img/logreg_feature_importance.png # top-15 |coefficients|, WheelType=Unknown dominates
  - img/feature_importance.png        # feature importance (exploratory / alternate model)
  - img/confusion_matrix.png          # confusion matrix at tuned threshold — error analysis
```

---

## Recommendations
<!-- Direct, actionable for this project as it stands today. -->

```
r1:
  title:  Deploy as a triage filter, not an auto-reject
  detail: Run the tuned LogReg Lasso (threshold 0.65) to flag ~10 % of an unlabeled batch for
          human review at ~45 % precision — the model is not accurate enough to auto-reject.

r2:
  title:  Flag a missing WheelType entry at intake, before any model runs
  detail: WheelType is missing for only 4.4 % of cars, but 70.3 % of those are bad buys — about
          6x the 12.3 % base rate. That single fact is the strongest risk signal in the whole
          dataset and costs nothing extra to check, since the field is already collected.
```

---

## Opportunities
<!-- Concrete, still-open next steps that could tangibly improve this model. -->

```
o1:
  title:  Give the model a second signal for its blind spot
  detail: Error analysis (06_error_analysis.ipynb) shows the model leans hard on WheelType and
          therefore misses bad buys that don't carry that flag — those missed cars are on average
          $672 pricier and 0.9 years newer than the ones it catches. Next iteration: add a second,
          independent risk feature (e.g. price deviation from the market-price anchors) aimed at
          exactly that segment.

o2:
  title:  Try the leaner 7-feature model for production
  detail: The `cats_strong` feature set (7 features: the strongest categoricals) reaches F1
          0.3587 in the tracked sweep — 96 % of the full 28-feature catalog's F1 0.3726, with a
          quarter of the features. Worth a real head-to-head: a much simpler, more maintainable
          model might be an acceptable trade for a small F1 cost.
```

---

## Learnings
<!-- Methodology takeaways for the next project — not specific to this dataset. -->

```
l1:
  title:  Cast a wide feature net before pruning
  detail: The full catalog beat the "obviously relevant" numeric-only subset by 0.08 F1 (0.29 →
          0.37, see F2). For the next project: build the broad catalog first, let systematic
          testing (ModelTracker + feature/model catalogs) find the signal, and only prune
          afterwards — not before.

l2:
  title:  Check whether "missing" itself is a signal before imputing it away
  detail: WheelType looked unremarkable when filled in (bad-buy rates 8–13 % across its normal
          values) — the signal only showed up in the 4.4 % where it was empty (70.3 % bad-buy
          rate). General practice for future projects: before silently filling in missing values,
          check whether the fact that a value is missing already predicts the target.

l3:
  title:  Freeze batch-level statistics for single-record scoring
  detail: Missing-price imputation (group median) and the price-category buckets (quantile cuts)
          are both recomputed from whichever batch of cars is currently loaded — they need a
          group to compute a median or a quantile from. A single incoming car has no such group.
          For a real production version: learn these values once from training data, freeze
          them, and reuse the same fixed numbers for every future car, one at a time or in bulk.

l4:
  title:  Compare all finalists on one shared held-out set before naming a winner
  detail: An earlier belief that Random Forest was the best model (~F1 0.39) didn't hold up once
          all three finalists were scored together on the exact same fixed test set — Random
          Forest actually placed second (F1 0.35) behind LogReg Lasso (F1 0.37). Different
          notebooks/tracking files with different splits had produced numbers that looked
          comparable but weren't. Lesson: always do one final, shared evaluation pass across
          finalists before declaring a winner.
```

---

## Status

```
generated_by:   /project-case story
generated_at:   2026-07-09
summary_version: 1
portfolio_check: ✅ passed
report_html:    ❌ pending
slides_html:    ❌ pending
dashboard:      ❌ not deployed — static notebook + report project, no dashboard planned
```
