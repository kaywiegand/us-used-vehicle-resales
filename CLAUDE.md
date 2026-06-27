# CLAUDE.md — US Used Vehicle Resales

> Projektspezifische Anweisungen für Claude Code.
> Ergänzt die globale CLAUDE.md aus dem Workspace-Root.

---

## Projekt

| Feld | Inhalt |
| :--- | :--- |
| Slug | `us-used-vehicle-resales` |
| Paket | `us_used_vehicle_resales` (Import mit Underscores) |
| Typ | DSC — Data Science / Klassifikation |
| Aufgabe | "Bad Buy"-Vorhersage: Wird ein ersteigerter Gebrauchtwagen ein Fehlkauf ("Montagsauto")? |
| Stack | Pandas · NumPy · scikit-learn · LightGBM/XGBoost · Matplotlib/Seaborn · Jupyter · uv |
| Herkunft | StackFuel-Abschlussprojekt (Modul 3, Kapitel 4) |
| Status | 🔄 in Portfolio-Aufbereitung |

---

## Session-Einstieg

```
1. PROCESS_LOG.md lesen — aktueller Stand und letzte Session
2. ROADMAP.md lesen — offene Phasen
3. Globale CLAUDE.md aus /Users/kaywiegand/Workspace/ gilt weiterhin
```

---

## Datenbasis

```
data/01_raw/        ← Rohdaten (data_train.csv, features_aim.csv) — nie verändern, nicht in Git
data/02_interim/    ← nach Cleaning + Split
data/03_processed/  ← ML-ready Features
data/04_models/     ← trainierte Modelle + Tracking-CSVs
data/05_results/    ← Predictions auf features_aim
```

Daten und Modelle sind via `.gitignore` ausgeschlossen.
Datenquelle + Spaltenbeschreibung → `DATA_DICTIONARY.md` (bzw. vorerst `infos.md`).

Python-Paket (Zielzustand nach Phase 2):
```python
from us_used_vehicle_resales.cleaning import clean_data
from us_used_vehicle_resales.features import engineer_features
from wgnd import setup, inspect, show_df   # echtes wgnd-Toolkit (Git-Dependency)
```

---

## Projektspezifische Konventionen

- **Code ist Englisch** (Variablen, Funktionen, Spalten, Kommentare) — Workspace-Regel.
- Zielvariable `IsBadBuy` ist **unbalanciert** — Klassengewichte / Sampling beachten,
  Accuracy ist keine sinnvolle Primärmetrik (→ Recall/Precision/F1, PR-AUC).
- `wgnd` referenziert ausschliesslich das **offizielle Toolkit** (Git-Dependency).
  Projekt-eigene Helfer liegen in `us_used_vehicle_resales.*` — nicht mehr unter `wgnd`.
- Outputs (Charts) → `reports/img/`, nie im Notebook-Root ablegen.

---

## Qualitätssicherung — Pflicht nach jeder Code-Änderung

Nach jeder nicht-trivialen Änderung an Python-Files **vor** der Fertigmeldung:

```bash
source .venv/bin/activate && python -c "from us_used_vehicle_resales.<modul> import <symbol>; print('OK')"
```

Mindestens das geänderte Modul importieren. Notebook-Edits erst nach Bestätigung,
dass Kay das Notebook geschlossen/gespeichert hat.

---

## Offener Umbau (siehe ROADMAP)

- Phase 2: `src/` zu einem Paket `us_used_vehicle_resales/` konsolidieren,
  lokale `src/wgnd/`-Namenskollision auflösen, echtes Toolkit als Dependency.
- Phase 3: Notebook-Hygiene (Intro bereinigen, Modell-Notebooks `03a/03b`, Tabellen).
- Phase 4: README + reports/index.html + DATA_DICTIONARY.md.
