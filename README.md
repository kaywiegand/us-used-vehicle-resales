# US Used Vehicle Resales — Bad-Buy Prediction

> Klassifikationsmodell, das für einen US-Gebrauchtwagenhändler vorhersagt, ob ein in
> der Auktion ersteigertes Fahrzeug ein Fehlkauf ("Bad Buy" / "Montagsauto") wird —
> bevor es gekauft wird.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Type](https://img.shields.io/badge/Type-Data%20Science%20·%20Classification-green)
![Status](https://img.shields.io/badge/Status-In%20Portfolio%20Aufbereitung-orange)

> ⚠️ **Work in Progress** — dieses README befindet sich im Aufbau (Portfolio-Phase 4).
> TL;DR mit Zahlen, Modell-Ergebnisse und Visualisierungen folgen.

---

## Problem Statement

Ein US-Gebrauchtwagenhändler kauft Fahrzeuge günstig in Onlineauktionen ein, um sie
gewinnbringend weiterzuverkaufen. Das grösste Risiko: ein ersteigertes Auto entpuppt
sich als **"Bad Buy"** ("Montagsauto") — ein Fahrzeug mit schwerwiegenden Mängeln, das
nicht weiterverkauft werden kann und neben den Anschaffungs- auch Folgekosten
(Lagerung, Reparatur, Wertverlust) verursacht.

**Leitfrage:** Lässt sich vor dem Kauf vorhersagen, ob ein Angebot ein Bad Buy ist —
ohne dabei zu viele gute Käufe fälschlich auszuschliessen?

**Charakteristik:** Binäre Klassifikation auf der Zielvariable `IsBadBuy` mit stark
**unbalancierten Klassen** (Bad Buys sind die Minderheit).

---

## Dataset

- **Quelle:** StackFuel-Abschlussprojekt (Modul 3, Kapitel 4) — Gebrauchtwagenauktionen US.
- **Trainingsdaten:** `data/01_raw/data_train.csv` (33 Spalten, eine Zeile je Fahrzeug).
- **Zieldatensatz ohne Labels:** `data/01_raw/features_aim.csv` (Predictions als Deliverable).
- **Spaltenbeschreibung:** → [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) _(in Aufbereitung; vollständig aktuell in [`infos.md`](infos.md))_.

> Rohdaten und trainierte Modelle sind via `.gitignore` aus dem Repo ausgeschlossen.

---

## Approach

Data-Science-Workflow ("StackFuel-Way"):

1. **Exploration** — EDA, Missing-Werte, Verteilungen, Klassenungleichgewicht.
2. **Preparation** — Cleaning, Feature Engineering, Train/Test-Split.
3. **Modelling** — Baseline (Logistic Regression) → Random Forest, Umgang mit Imbalance.
4. **Evaluation** — Recall/Precision/F1, PR-AUC; Modellvergleich gegen Baseline.

---

## Notebooks

| # | Notebook | Inhalt |
| :--- | :--- | :--- |
| 00 | `notebooks/00_introduction.ipynb` | Einstieg, Szenario, Navigation |
| 01 | `notebooks/01_exploring.ipynb` | Explorative Datenanalyse |
| 02 | `notebooks/02_processing.ipynb` | Cleaning, Feature Engineering, Split |
| 03 | `notebooks/03_modelling*.ipynb` | Modellierung (LogReg, Random Forest) |
| 04 | `notebooks/04_evaluation*.ipynb` | Evaluation & Modellvergleich |

> Hinweis: Notebook-Benennung wird in der Aufbereitung linearisiert (`03a/03b`, `04`).

---

## Tech Stack

Python 3.12 · pandas · NumPy · scikit-learn · LightGBM/XGBoost · Matplotlib/Seaborn ·
Jupyter · uv · [`wgnd`-Toolkit](https://github.com/kaywiegand/wgnd-toolkit)

---

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dsc]"
```

_(Vollständiges Setup folgt in Phase 4.)_

---

## Author

**Kay Wiegand** · [GitHub](https://github.com/kaywiegand)
