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

## 2026-07-09 — Phase 5: Re-Review + Struktur-Cleanup + Content-Audit

- `/project-review` erneut: Ergebnis **BEDINGT** — Fundament/README/Hub portfolio-tauglich,
  aber Konventions-Drift + MD-Drift + Leichen-Notebooks.
- **Struktur-Cleanup (dieser Commit):**
  - `reports/` → `public/` (neuer Workspace-Standard, `git mv` — Historie erhalten).
    Pfade in README/CLAUDE/ROADMAP repointed. Hub-Links (relativ, eine Ebene höher) bleiben gültig.
  - 2 unnummerierte Leichen-Notebooks entfernt (`Workflow.ipynb`, `Data-Dictionary.ipynb` —
    redundant zu `DATA_DICTIONARY.md`).
  - MD-Drift: ROADMAP Phase 1 `[x]`; CLAUDE.md-Stack auf reines scikit-learn korrigiert
    (LightGBM/XGBoost waren nie im Code); README um „Reports & Artifacts" + LinkedIn ergänzt.
- **Content-Audit (inhaltliche Prüfung der Notebooks, da Lernphasen-Projekt):**
  - Split sauber (stratified, vor Cleaning/FE) — **kein** Leakage.
  - **Kernproblem = Ergebnis-Kommunikation, nicht die Pipeline:**
    - README/Hub krönen **RF (F1 0.39)** als Best — Tracking-CSVs zeigen RF max ~0.37,
      LogReg-Lasso 0.38–0.40; **deploytes Modell in `04b` ist LogReg-Lasso, nicht RF**;
      RF nie auf Held-out-Test evaluiert.
    - Test-`classification_report` in `04a/04b` nicht als Output gespeichert →
      README-Testzahlen nicht reproduzierbar belegt.
    - Notebook-Outputs stale (autoreload: `engineer_features` 5 vs 9 Features zwischen
      04a/04b; `os.getcwd()` = alter Pfad `DSC_Gebrauchtwagen`). `nbstripout` inaktiv.
    - AIM-Predictions über-flaggen (Baseline 40,6 % / Lasso 27 % vs. 12,35 % Basisrate),
      2 widersprüchliche Result-Files, getunter Threshold nicht genutzt.
    - `feat_price_cat` via `pd.qcut` → Bin-Grenzen pro Datensatz inkonsistent (train/test/aim).
  - → Findings in BACKLOG (#13–#17). **Entscheidung offen (Kay):** Results-Story korrigieren
    vor `/project-case` — nicht eigenmächtig umgeschrieben.
- **Nächster Schritt:** Content-Findings mit Kay klären → dann `/project-case check`.

## 2026-07-09 — Phase 5: Results-Reproduktion + Data-Leakage-Audit

- **Entscheidung Kay:** Notebooks sauber rerun → neues `04_evaluation.ipynb` als Single Source
  of Truth (deterministisch, per nbconvert ausgeführt, echte Outputs eingebettet).
- **Reproduzierte Test-Zahlen** (alle 3 Archetypen auf demselben Held-out-Test, n=13.124):
  Ergebnis-Tabelle in `04_evaluation.ipynb`. Winner = **LogReg Lasso**, nicht RF.
  Das behauptete „RF F1 0.39" war nicht reproduzierbar → retired. RF landet zweiter.
  Threshold-Tuning hebt den Winner auf ein brauchbares Operating Point (Notebook §4).
  → BACKLOG #13 + #14 erledigt.
- **AIM** neu mit Winner + getuntem Threshold: ein kanonisches File
  `data/05_results/predictions_aim_final.csv` (gitignored).
- **Data-Leakage-Audit** (`docs/DATA_LEAKAGE_AUDIT.md`) — ausgelöst durch Kays Hinweis: die
  StackFuel-Prüfung verlangte F1 > 0.40, wurde nicht erreicht, Leakage vermutet, Projekt gestoppt.
  - Prüfer-Zahlen (echte AIM-Labels) belegt: eingereicht wurde die **Baseline** (AIM-F1 0.281 ≈
    interne Baseline 0.287) → Baseline generalisiert sauber, kein Leakage.
  - Vektor-für-Vektor geprüft: Split vor FE, Transformer nur auf Train gefittet, keine
    target-abgeleiteten Features, 0 Duplikate → **kein Leakage**.
  - **Experiment** (Notebook-nahe, Script): hochkardinale Identifier (VNZIP1/Model/SubModel/Trim/
    BYRNO, 2.082 Levels) entfernen kostet **nur 0.003 F1** (0.373→0.370) → **kein Overfitting**.
  - Fazit: kein Leakage, kein Overfitting. Der niedrige Prüfer-Score war ein **Submission-Fehler
    (Baseline statt Champion)**. Die 0.40-Hürde ist mit dem getunten Champion erreichbar.
  - **2026-07-09 (später): echte AIM-Labels** von Kay besorgt (`target_aim.csv`, zip/b64 → lokal
    dekodiert, verifiziert 7.292/863). Champion auf echten Out-of-Sample-Labels evaluiert:
    Baseline reproduziert die Prüfer-Zahl exakt (F1 0.280 vs 0.281, ±3 Zeilen) → Pipeline-Fidelity
    bewiesen. **Champion AIM-F1: 0.360 @0.5, 0.409 @tuned 0.65 → knackt die 0.40-Hürde auf echten
    Daten.** Intern→AIM-Gap nur 0.013 → Leakage/Overfitting empirisch ausgeschlossen.
    Audit + README + Hub auf diese belegten Zahlen gehoben. (`target_aim.csv` bleibt gitignored.)
  - **`docs/RESULTS.md` erstellt** (Kay-Wunsch): vollständiger Results-Report + Retrospektive
    (Modeling-Journey, interne + AIM-Zahlen, Leakage-Zusammenfassung, Root-Cause der 0.28,
    Lessons Learned, Recommendations). Als Narrative-Spine für `/project-case`. Aus README verlinkt.
  - **`notebooks/05_experiment_framework.ipynb` erstellt** (Kay-Wunsch): Engineering-Showcase der
    Experimentier-Infrastruktur — Feature-Catalog, Model-Catalog, `ModelTracker` (Live-Demo +
    realer 448-Run-Benchmark, Top-10-Chart). Deterministisch per nbconvert ausgeführt (0 Fehler).
    Aus README-Notebooks + RESULTS.md verlinkt.
- **Portfolio-Aufwertungen** (Kay-Wunsch): `ModelTracker` als selbstgebautes Tool in README+Hub
  erwähnt; Querverweis auf Flaggschiff `zh-tram-flow` (geteiltes `wgnd`-Toolkit).
- README + `public/index.html` auf die belegten Zahlen + Audit umgeschrieben.
- **Offen:** BACKLOG #15 (nbstripout/rerun-Hygiene), #16 (AIM-Schärfung teilw. erledigt),
  #17 (qcut/Imputation in Pipeline fitten — vom Audit als Empfehlung bestätigt).
- **Nächster Schritt:** `/project-case check`.
