# PROCESS_LOG — US Used Vehicle Resales

Verlauf + Entscheidungen. Pointer auf Files — kein Inhalt kopieren.
Metriken, Findings, Outputs gehören in Notebooks/Code — nicht hier.

---

## 2026-06-27 — Portfolio-Rework gestartet

- `/project-review` durchgeführt: Ergebnis **NICHT bereit** für `/project-case` —
  keine Portfolio-Infrastruktur, Projekt nicht versioniert.
- Plan für Umbau zum Portfolio-Projekt erstellt und freigegeben (5 Phasen).
- **Entscheidungen:**
  - Daten/Modelle bleiben via `.gitignore` aus Git; Quelle wird dokumentiert.
  - `src/wgnd/` ist **kein** Toolkit-Fork, sondern Projekt-Code mit kollidierendem
    Namen → wird nach `us_used_vehicle_resales/` umgezogen; echtes `wgnd`-Toolkit
    kommt als Git-Dependency (Phase 2).
  - Modell-Notebooks werden als `03a/03b` gekennzeichnet (nicht zu einem gemerged).
- **Phase 0 erledigt:** Repo initialisiert, `.gitignore`, Snapshot-Commit `6275fee`,
  Push zu `git@github.com:kaywiegand/us-used-vehicle-resales.git`.
- **Phase 1 erledigt:** Fundament-MD-Files angelegt (CLAUDE · README-Gerüst · ROADMAP ·
  PROCESS_LOG · BACKLOG · `.python-version`), Eintrag in `docs/PROJECTS.md`.
- **Phase 2 erledigt:** Commit `538704c`.
  - Alle Module nach `src/us_used_vehicle_resales/` konsolidiert (`git mv`, Historie erhalten).
  - `wgnd`-Namenskollision aufgelöst; echtes Toolkit (`wgnd==0.2.0`) als Git-Dependency.
  - `inspect.py` repariert (war kaputt: fehlte als `.py`, zwei split-consistency-Aliase
    ergänzt, `display`-Import, tote `wg`-Referenz entfernt).
  - `shap`/`lightgbm`/`xgboost` aus Deps entfernt — ungenutzt (Projekt ist reines
    scikit-learn); `shap` brach zudem auf Python 3.12 (altes `llvmlite`).
  - 8 Notebooks auf `us_used_vehicle_resales` repointed.
  - Verifiziert: `uv pip install -e ".[dev]"`, Paket-Import, alle `wg.*`-Symbole,
    echtes Toolkit, alle Notebook-Import-Statements im venv.
- **Phase 3 erledigt:** Commit `41cf47b`.
  - `00_introducing.ipynb` (LLM-Boilerplate-Navigation auf erfundene Dateinamen) komplett
    ersetzt durch `00_introduction.ipynb` — echter Einstieg (Szenario, Aufgabe, Datenbasis,
    Navigation, Setup).
  - Modell-Notebooks linearisiert: `03_modelling-prep`, `03a_modelling-logreg`,
    `03b_modelling-rf`, `04a_evaluation-baseline`, `04b_evaluation-logreg` (Entscheidung
    Kay: Varianten behalten, klar nummerieren).
  - Lose Artefakte verschoben: `feature_importance.png` → `reports/img/`,
    `Data-Dictionary.html` → `reports/`, Text-Dumps → `docs/`.
  - `01_exploring`/`02_processing` bewusst nicht umbenannt (Namen klar, kein Scope-Creep).
  - Offen (BACKLOG #5): `show_df()`-Tabellen-Retrofit als optionaler Feinschliff.
- **Phase 4 erledigt:** Commit `1741535`.
  - Echte Zahlen aus Rohdaten + Notebook-Outputs extrahiert (65.620 Zeilen, 33 Spalten,
    Bad-Buy-Rate 12,35 %; Modell-Metriken aus 04a/04b + Model-Tracking 03b).
  - README.md neu (Englisch, portfolio-facing) mit Results-Tabelle Baseline → LogReg-Lasso
    → Random Forest (Bad-Buy F1 0.29 → 0.39) und Key Visual.
  - `DATA_DICTIONARY.md` (33 Spalten + Known Issues).
  - `reports/index.html` self-contained (3 Charts inline base64), per Preview verifiziert
    (Charts geladen, Tabelle korrekt).
  - 5 echte Charts nach `reports/img/` (target_distribution, feature_correlations,
    logreg_feature_importance, threshold_f1_curve, feature_importance).
  - Kernbefund: fehlende `WheelType`-Info ist stärkster Bad-Buy-Prädiktor.
- **Nächster Schritt:** Phase 5 — `/project-review` erneut, dann `/project-case`.
