# US Used Vehicle Resales — Bad-Buy Prediction

> Ein Klassifikationsmodell, das **vor dem Kauf** vorhersagt, ob ein bei einer Auktion gekauftes
> Gebrauchtfahrzeug sich als "Bad Buy" entpuppt — ein Montagsauto, das nicht weiterverkauft werden
> kann — damit ein US-Gebrauchtwagenhändler aufhört, für Fahrzeuge zu viel zu bezahlen, die
> Verluste statt Marge erzeugen.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Stack](https://img.shields.io/badge/Stack-scikit--learn%20·%20pandas-orange)
![Type](https://img.shields.io/badge/Type-Data%20Science%20·%20Classification-green)
![Status](https://img.shields.io/badge/Status-Portfolio%20WIP-yellow)

---

## TL;DR

- **Aufgabe:** binäre Klassifikation von `IsBadBuy` auf **65.620 versteigerten Fahrzeugen** mit **33 Features**.
- **Die Schwierigkeit:** Die Klassen sind stark **unbalanciert** — nur **12,35 %** der Autos sind Bad Buys. Ein Modell, das immer "guter Kauf" vorhersagt, käme schon auf 87,65 % Accuracy, ohne einen einzigen Bad Buy zu erwischen — deshalb optimiert das Projekt stattdessen den **F1-Score der Bad-Buy-Klasse**.
- **Systematisches Testen statt Handverlesen:** Ein selbstgebauter `ModelTracker` + ein Feature-/Model-Catalog fuhr **448 geloggte Experimente** über 19 Feature-Sets × 6 Modell-Familien in ~62 Minuten aktiver Rechenzeit — siehe [`05_experiment_framework.ipynb`](notebooks/05_experiment_framework.ipynb).
- **Breit angelegt gewinnt:** Ein rein numerisches Feature-Set (6 Features) deckelt bei **F1 0,29**; der volle Catalog (28 Features, plus Kategoriale) erreicht **F1 0,37** — konsistent über alle Modell-Familien hinweg.
- **Stärkstes Signal ist ein fast leeres Feld:** `WheelType` ist bei 95,6 % der Autos normal befüllt (dort unauffällig), aber die 4,4 %, bei denen es schlicht **fehlt**, haben eine **Bad-Buy-Rate von 70,3 %** — das 6-fache der Basisrate, und der stärkste Einzelprädiktor.
- **Bestes Modell:** Logistische Regression mit L1-Penalty (`class_weight='balanced'`) erreicht **Bad-Buy-F1 ≈ 0,37** auf dem Held-out-Testset. Das Tunen des Decision-Thresholds auf den Triage-Use-Case hebt es auf **F1 ≈ 0,42 bei Precision ≈ 0,45**.
- **Error Analysis:** Der blinde Fleck des Modells sind neuere, teurere Bad Buys ohne das `WheelType = Unknown`-Flag — siehe [`06_error_analysis.ipynb`](notebooks/06_error_analysis.ipynb).

![Class distribution of IsBadBuy](public/img/target_distribution.png)

*Klassenverteilung: ~57.500 gute Käufe vs. ~8.100 Bad Buys — die zentrale Modellierungs-Herausforderung.*

---

## Wo einsteigen

| Du bist… | Hier starten |
| :--- | :--- |
| Recruiter (30 Sek.) | Dieses README — TL;DR + Ergebnisse |
| Data Scientist (10 Min.) | [`00_introduction.ipynb`](notebooks/00_introduction.ipynb) → [`01_exploring.ipynb`](notebooks/01_exploring.ipynb) → [`01a_eda-detail.ipynb`](notebooks/01a_eda-detail.ipynb) |
| Modellierungs-Deep-Dive | [`03a_modelling-logreg.ipynb`](notebooks/03a_modelling-logreg.ipynb) · [`03b_modelling-rf.ipynb`](notebooks/03b_modelling-rf.ipynb) |

---

## Problemstellung

Ein US-Gebrauchtwagenhändler kauft Fahrzeuge günstig in Onlineauktionen ein, um sie
gewinnbringend weiterzuverkaufen. Das grösste Risiko ist ein **"Bad Buy"** (ein Montagsauto):
ein Auto mit schwerwiegenden Mängeln, das nicht weiterverkauft werden kann und stattdessen
Folgekosten erzeugt (Lagerung, Reparaturen, Wertberichtigungen).

**Leitfrage:** Können wir vor dem Kauf vorhersagen, ob ein Angebot ein Bad Buy ist —
**ohne dabei zu viele gute Autos abzulehnen**? Das ist ein Precision/Recall-Trade-off auf einer
seltenen Positivklasse, kein Accuracy-Problem.

**Ziel (Assessment-Hürde):** **Bad-Buy-F1 > 0,40** auf dem verdeckten Scoring-Set
`features_aim.csv` erreichen, dessen Labels nur der Prüfer kennt. Das Deliverable ist der Satz an
Predictions für diese Datei. (Original-Briefing → [`docs/ASSIGNMENT.md`](docs/ASSIGNMENT.md).)

---

## Datenbasis

| | |
| :--- | :--- |
| Trainingsdaten | `data/01_raw/data_train.csv` — **65.620 Zeilen**, **33 Spalten**, `;`-separiert, gelabelt |
| Scoring-Daten | `data/01_raw/features_aim.csv` — **7.292 Zeilen**, ungelabelt (Vorhersageziel) |
| Target | `IsBadBuy` — `0` guter Kauf (87,65 %), `1` Bad Buy (12,35 %) |
| Herkunft | StackFuel-Abschlussprojekt (Modul 3, Kapitel 4) |

Vollständige Spaltenreferenz → [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) · Original-Briefing → [`docs/ASSIGNMENT.md`](docs/ASSIGNMENT.md).

> Rohdaten und trainierte Modelle sind via `.gitignore` aus dem Repo ausgeschlossen.

---

## Ansatz

**1 · Exploration** ([`01_exploring.ipynb`](notebooks/01_exploring.ipynb) ·
[`01a_eda-detail.ipynb`](notebooks/01a_eda-detail.ipynb) ·
[`01b_eda-summary.ipynb`](notebooks/01b_eda-summary.ipynb)) — Verteilungen,
fehlende Werte, die starke Klassen-Imbalance, und eine bivariate Risikoanalyse, die zeigt, dass
textartige Spalten (Trim, SubModel, VNZIP1, WheelType) starke Risikotreiber sind, kein Rauschen;
Preisspalten (MMR-Familie) sind stark korreliert und werden zu 3 Ratio-Features verdichtet.

**2 · Preparation** ([`02_processing.ipynb`](notebooks/02_processing.ipynb)) — Cleaning,
Feature Engineering (Preis-Ratios, Meilen-pro-Jahr, Risiko-Buckets) und ein **stratifizierter**
Train/Test-Split, der die 12,35 %-Bad-Buy-Rate erhält.

**3 · Systematisches Experimentieren** ([`05_experiment_framework.ipynb`](notebooks/05_experiment_framework.ipynb))
— ein Feature-Catalog (19 Sets) × Model-Catalog (6 Familien), gesweept und geloggt von einem
selbstgebauten `ModelTracker` (448 Runs), statt vorab ein Feature-Set handverlesen auszuwählen.

**4 · Modeling** ([`03a`](notebooks/03a_modelling-logreg.ipynb) ·
[`03b`](notebooks/03b_modelling-rf.ipynb)) — Baseline Logistische Regression → L1 Logistische
Regression und Random Forest, alle mit `class_weight='balanced'`, um der Imbalance
entgegenzuwirken. Decision-Threshold auf der F1-Kurve getunt.

**5 · Evaluation** ([`04_evaluation.ipynb`](notebooks/04_evaluation.ipynb)) — alle drei
Finalisten auf demselben Held-out-Testset, Threshold-Tuning, Scoring.

**6 · Error Analysis** ([`06_error_analysis.ipynb`](notebooks/06_error_analysis.ipynb)) — Confusion
Matrix plus eine Segment-Aufschlüsselung der verpassten und fälschlich geflaggten Autos.

---

## Ergebnisse

Performance auf der **Bad-Buy-Klasse** (der Minoritätsklasse, auf die es ankommt), alle drei auf
demselben **Held-out-Testset** (n = 13.124), Threshold 0,5:

| Modell | Recall | Precision | F1 (Bad-Buy) | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| Baseline — Logistische Regression (8 Feat.) | 0,61 | 0,19 | 0,29 | 0,67 |
| Random Forest (deep, balanced) | 0,64 | 0,24 | 0,35 | 0,75 |
| **Logistische Regression Lasso (L1, balanced)** | 0,60 | 0,27 | **0,37** | 0,77 |

<sub>End-to-End reproduziert in [`04_evaluation.ipynb`](notebooks/04_evaluation.ipynb).</sub>

**Breit angelegt schlägt Handverlesen** — über die 448 getrackten Runs deckelt ein rein
numerisches Feature-Set (6 Features) bei F1 0,2918; der volle Catalog (28 Features, plus
Kategoriale) erreicht F1 0,3726, konsistent über alle Modell-Familien:

| Feature-Set | Features | Bester F1 (getrackte Runs) |
| :--- | :---: | :---: |
| `numeric` — nur Preis, Alter, Kilometerstand | 6 | 0,2918 |
| **`all_in_with_noise` — voller Catalog** | **28** | **0,3726** |

**Threshold-Tuning** — bei balancierten Klassengewichten überflaggt der Default-Threshold von
0,5. Beim F1-optimalen Threshold (0,65) erreicht das Gewinner-Modell **F1 0,42 · Precision 0,45 ·
Recall 0,40** — ausbalanciert für den Triage-Use-Case: Bad Buys erwischen, ohne zu viele gute
Autos abzulehnen.

**Prädiktivstes Feature: ein fast leeres Feld.** `WheelType` ist bei 95,6 % der Autos normal
befüllt — dort unauffällig — aber die 4,4 %, bei denen es schlicht fehlt, tragen eine
Bad-Buy-Rate von 70,3 %:

| WheelType-Wert | Anteil Autos | Bad-Buy-Rate |
| :--- | :---: | :---: |
| Alloy | 49,3 % | 11,1 % |
| Covers | 45,3 % | 8,1 % |
| Special | 1,0 % | 12,6 % |
| **Fehlend** | **4,4 %** | **70,3 %** |
| Durchschnitt (alle Autos) | — | 12,3 % |

**Empfehlungen:** Die **L1 Logistische Regression** beim getunten Threshold als **Triage-Filter**
deployen — sie flaggt ~10 % eines ungelabelten Batches zur menschlichen Review bei ~0,45
Precision, nicht als automatischen Reject. Ein fehlendes `WheelType` als erstrangigen
Risikoindikator beim Intake behandeln.

**Potenzial:** Ein zweites, unabhängiges Risiko-Feature für den blinden Fleck des Modells
ergänzen — neuere, teurere Bad Buys ohne das `WheelType`-Flag (siehe
[`06_error_analysis.ipynb`](notebooks/06_error_analysis.ipynb)); und das schlankere
7-Feature-Set `cats_strong` evaluieren (F1 0,3587 — 96 % der Performance des vollen Catalogs mit
einem Viertel der Features).

> **Vollständige Ausarbeitung:** [`07_results.ipynb`](notebooks/07_results.ipynb) — interne +
> echte Holdout-Zahlen, Robustheits-Checks und Lessons Learned.

---

## Notebooks

| # | Notebook | Inhalt |
| :--- | :--- | :--- |
| 00 | [`00_introduction.ipynb`](notebooks/00_introduction.ipynb) | Einstiegspunkt: Szenario, Aufgabe, Navigation |
| 01 | [`01_exploring.ipynb`](notebooks/01_exploring.ipynb) | Setup, Split, erste EDA-Insights |
| 01a | [`01a_eda-detail.ipynb`](notebooks/01a_eda-detail.ipynb) | Explorative Datenanalyse im Detail |
| 01b | [`01b_eda-summary.ipynb`](notebooks/01b_eda-summary.ipynb) | EDA Summary — wichtigste Findings auf einen Blick |
| 02 | [`02_processing.ipynb`](notebooks/02_processing.ipynb) | Cleaning, Feature Engineering, Split |
| 03 | [`03_modelling-prep.ipynb`](notebooks/03_modelling-prep.ipynb) | Modelling-Vorbereitung |
| 03a | [`03a_modelling-logreg.ipynb`](notebooks/03a_modelling-logreg.ipynb) | Logistische Regression |
| 03b | [`03b_modelling-rf.ipynb`](notebooks/03b_modelling-rf.ipynb) | Random Forest |
| 04 | [`04_evaluation.ipynb`](notebooks/04_evaluation.ipynb) | **Ergebnis-SSoT** — alle Modelle auf demselben Held-out-Test, Threshold-Tuning, Scoring |
| 04a | [`04a_evaluation-baseline.ipynb`](notebooks/04a_evaluation-baseline.ipynb) | Baseline-Evaluation (exploratorisch) |
| 04b | [`04b_evaluation-logreg.ipynb`](notebooks/04b_evaluation-logreg.ipynb) | LogReg-Deployment-Walkthrough (exploratorisch) |
| 05 | [`05_experiment_framework.ipynb`](notebooks/05_experiment_framework.ipynb) | **Engineering-Showcase** — Feature-Catalog, Model-Catalog & der selbstgebaute `ModelTracker` (448-Run-Sweep) |
| 06 | [`06_error_analysis.ipynb`](notebooks/06_error_analysis.ipynb) | **Error Analysis** — Confusion Matrix, False-Negative-/False-Positive-Segment-Aufschlüsselung |
| 07 | [`07_results.ipynb`](notebooks/07_results.ipynb) | **Vollständige Ergebnisse & Retrospektive** — interne + echte Holdout-Zahlen, Robustheits-Checks, Lessons Learned |

---

## Tech Stack

Python 3.12 · pandas · NumPy · scikit-learn (Logistic Regression, Random Forest,
pipelines, `ColumnTransformer`) · Matplotlib / Seaborn · Jupyter · uv.

Projekt-spezifischer Code (Cleaning, Feature Engineering, die Feature-/Model-Catalogs) liegt im
installierbaren Paket `us_used_vehicle_resales`. Der wiederverwendbare **`ModelTracker`** — ein
schlanker Experiment-Logger, der F1 / Recall / Precision / ROC-AUC pro Run in ein CSV schreibt,
den besten Run flaggt und die gefittete Pipeline exportiert (448 Runs über Feature-Sets und
Modell-Familien) — wurde **in diesem Projekt selbstgebaut und ist seitdem ins gemeinsam genutzte
[`wgnd-toolkit`](https://github.com/kaywiegand/wgnd-toolkit)** (v0.3.0) übernommen worden. Dieses
Projekt bezieht ihn jetzt von dort (`from wgnd import ModelTracker`), zusammen mit den
gemeinsamen EDA-/Output-Helfern.

> **Verwandte Arbeit:** teilt das Projekt-Scaffolding und den Tooling-Ansatz mit
> [**zh-tram-flow**](https://github.com/kaywiegand/zh-tram-flow) — dem Flaggschiff-Projekt des
> Portfolios (eine End-to-End-Data-Science-Pipeline für Zürcher Tram-Verspätungen), das das
> gemeinsame `wgnd-toolkit` bereits nutzt.

---

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e .            # add ".[dev]" for pytest/ruff/black
```

Danach die Notebooks in Lesereihenfolge öffnen (Start mit `00_introduction.ipynb`).

```python
from us_used_vehicle_resales.cleaning import clean_data
from us_used_vehicle_resales.features import engineer_features
import us_used_vehicle_resales as wg     # ModelTracker, print_*, save_*, inspect_*
```

---

## Reports & Artefakte

| Artefakt | Pfad | Inhalt |
| :--- | :--- | :--- |
| Ergebnisse & Retrospektive | [`notebooks/07_results.ipynb`](notebooks/07_results.ipynb) | Vollständige Ergebnisse, echter Holdout-Beweis, Robustheits-Checks, Lessons Learned |
| Error Analysis | [`notebooks/06_error_analysis.ipynb`](notebooks/06_error_analysis.ipynb) | Confusion Matrix, False-Negative-/False-Positive-Segment-Aufschlüsselung |
| Projekt-Hub | [`public/index.html`](public/index.html) | Eigenständige Übersicht: Pitch, Key Charts, Ergebnistabelle |
| Data Dictionary | [`public/data-dictionary.html`](public/data-dictionary.html) · [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) | Alle 33 Spalten + bekannte Probleme |
| Charts | [`public/img/`](public/img/) | Zielverteilung, Korrelationen, Feature Importance, Threshold-Kurve |

## Autor

**Kay Wiegand** · [GitHub](https://github.com/kaywiegand) · [LinkedIn](https://www.linkedin.com/in/kaywiegand/)
