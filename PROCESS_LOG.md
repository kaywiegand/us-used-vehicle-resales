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

## 2026-07-09 — Phase 5: Results-Reproduktion + Robustheits-Checks

- **Entscheidung Kay:** Notebooks sauber rerun → neues `04_evaluation.ipynb` als Single Source
  of Truth (deterministisch, per nbconvert ausgeführt, echte Outputs eingebettet).
- **Reproduzierte Test-Zahlen** (alle 3 Archetypen auf demselben Held-out-Test, n=13.124):
  Ergebnis-Tabelle in `04_evaluation.ipynb`. Winner = **LogReg Lasso**, nicht RF.
  Das behauptete „RF F1 0.39" war nicht reproduzierbar → retired. RF landet zweiter.
  Threshold-Tuning hebt den Winner auf ein brauchbares Operating Point (Notebook §4).
  → BACKLOG #13 + #14 erledigt.
- **AIM** neu mit Winner + getuntem Threshold: ein kanonisches File
  `data/05_results/predictions_aim_final.csv` (gitignored).
- **Robustheits-Checks** (Leakage/Overfitting) durchgeführt, ausgelöst durch Kays Hinweis, die
  Pipeline systematisch auf saubere Generalisierung zu prüfen:
  - Vektor-für-Vektor geprüft: Split vor FE, Transformer nur auf Train gefittet, keine
    target-abgeleiteten Features, 0 Duplikate → **kein Leakage**.
  - **Experiment** (Notebook-nahe, Script): hochkardinale Identifier (VNZIP1/Model/SubModel/Trim/
    BYRNO, 2.082 Levels) entfernen kostet **nur 0.003 F1** (0.373→0.370) → **kein Overfitting**.
  - **2026-07-09 (später): echte AIM-Labels** von Kay besorgt (`target_aim.csv`, zip/b64 → lokal
    dekodiert, verifiziert 7.292/863). Champion auf echten Out-of-Sample-Labels evaluiert:
    **Champion AIM-F1: 0.360 @0.5, 0.409 @tuned 0.65.** Intern→AIM-Gap nur 0.013 →
    Leakage/Overfitting empirisch ausgeschlossen, Modell generalisiert sauber.
    README + Hub auf diese belegten Zahlen gehoben. (`target_aim.csv` bleibt gitignored.)
  - **`docs/RESULTS.md` erstellt** (Kay-Wunsch, später zu `notebooks/07_results.ipynb`
    weiterentwickelt): vollständiger Results-Report + Retrospektive (Modeling-Journey, interne +
    AIM-Zahlen, Robustheits-Checks, Lessons Learned, Recommendations). Als Narrative-Spine für
    `/project-case`. Aus README verlinkt.
  - **`notebooks/05_experiment_framework.ipynb` erstellt** (Kay-Wunsch): Engineering-Showcase der
    Experimentier-Infrastruktur — Feature-Catalog, Model-Catalog, `ModelTracker` (Live-Demo +
    realer 448-Run-Benchmark, Top-10-Chart). Deterministisch per nbconvert ausgeführt (0 Fehler).
    Aus README-Notebooks + RESULTS.md verlinkt.
  - **Toolkit-Hygiene (Schritt 1 von 2):** Cross-Projekt-Scan zeigte — us-used ist einer von 3
    Nachzüglern (mit quito, zomato) mit lokalem Toolkit-Fork; Flaggschiff `zh-tram-flow` konsumiert
    `wgnd` bereits extern. `ModelTracker` existiert nur in den 3 Forks, nicht im Toolkit.
    Hygiene hier: toter Code entfernt (`utils_tracker`/`utils_export`/`sampling`), Phantom-`wgnd`-
    Dependency aus `pyproject` raus (war deklariert, nie importiert), README auf die Realität
    korrigiert (Helfer liegen lokal, nicht via wgnd). Paket-Import verifiziert.
  - **Schritt 2 (Workspace-Task):** Toolkit-Konsolidierung — `ModelTracker` + generische Helfer ins
    `wgnd-toolkit` promoten, alle 3 Nachzügler migrieren, Release. → Workspace-BACKLOG.
  - **`infos.md` → `docs/ASSIGNMENT.md`** verschoben (Provenance; Inhalt redundant zu README+DATA_DICTIONARY). Root aufgeräumt.
  - **2. `/project-review` (BEDINGT):** Hauptbefund = Notebook-Konventionsverstöße.
    **Notebook-Header-Cleanup (Schritt 1 — Header, erledigt):** programmatischer Transform über alle
    10 Notebooks — Emojis aus Überschriften entfernt (`01` allein hatte 39), jede Überschrift in
    eigene Markdown-Zelle gesplittet (CONVENTIONS-Kernregel), leere MD-Zellen entfernt, Cell-IDs
    ergänzt. Content-Erhalt verifiziert, nbformat-validiert, Code-Outputs unberührt. Betraf auch
    meine `04`/`05`. Zusätzlich: toter `mad`-Import (`statsmodels`, nicht installiert) aus `01` raus.
    **Offen (Schritt 2 — Tabellen):** `show_df()`-Tabellen zu Plots (BACKLOG #5), eins nach dem anderen.
  - **Docs angereichert:** `00_introduction` neu (Standard-Header + ToC, Ansatz/Modelle, Zielmetrik
    F1>0.40), README (Ziel + ASSIGNMENT-Link, 7.291→7.292). Header/Subtitle/ToC auf alle NBs,
    `03b`-Titel-Typo gefixt.
  - **Entscheidung Kay:** `01`-Split + Tabellen **geparkt** (gekoppelt an Run-Loop) → BACKLOG #19/#5.
    Exploration bleibt vorerst unverändert.
  - **Cleanup-Pass (kein Notebook-Run):** `nbstripout`-Dev-Dep entfernt (war inaktiv; Outputs bewusst
    committet behalten). `tests/test_import.py` angelegt (3 passed). BACKLOG #12/#16 geschlossen.
    ROADMAP Phase 5 + PROJECTS.md aktualisiert. Lokaler Cruft (`.ipynb_checkpoints`/`.DS_Store`/
    `__pycache__`) entfernt.
- **Nächster Schritt:** `/project-case check` — oder Run-Loop für Exploration-Split + Tabellen.
- **Portfolio-Aufwertungen** (Kay-Wunsch): `ModelTracker` als selbstgebautes Tool in README+Hub
  erwähnt; Querverweis auf Flaggschiff `zh-tram-flow` (geteiltes `wgnd`-Toolkit).
- README + `public/index.html` auf die belegten Zahlen umgeschrieben.
- **Offen:** BACKLOG #15 (nbstripout/rerun-Hygiene), #16 (AIM-Schärfung teilw. erledigt),
  #17 (qcut/Imputation in Pipeline fitten — aus den Robustheits-Checks als Empfehlung bestätigt).
- **Nächster Schritt:** `/project-case check`.

## 2026-07-09 — `/project-case check` + Error-Analysis-/Results-Notebooks

- **`/project-case check` durchgeführt:** alle Pflicht-Artefakte ✅, Story-Phase freigegeben.
  Top-3-Gaps: (1) Notebook-Header-Format weicht vom Standard ab (Title/Subtitle in getrennten
  statt einer Zelle, `01_exploring` hat vertauschte Zellen + falschen Titel „Preparation", `03a`
  hat deutschen Titel, `00`-Subtitle deutsch) — nicht in dieser Session gefixt, bleibt offen;
  (2) **Error Analysis fehlte** — `ConfusionMatrixDisplay` nur importiert, nie genutzt/besprochen;
  (3) `public/md/portfolio.md` fehlt erwartungsgemäß (Story-Phase stand noch aus).
- **`notebooks/06_error_analysis.ipynb`** neu angelegt (Kay-Wunsch): Confusion Matrix (echt
  geplottet, `public/img/confusion_matrix.png`), False-Negative-Segmentanalyse (verpasste Bad Buys
  sind newer + teurer, tragen fast nie `WheelType=Unknown` — Modell-Blind-Spot identifiziert),
  False-Positive-Segmentanalyse (fälschlich geflaggte Autos sind älter + günstiger — akzeptabler
  Trade-off für Triage-Filter), kurzer Verweis auf `ModelTracker`/Catalogs (`05`) für schnelles
  Testen/Protokollieren. Deterministisch per nbconvert ausgeführt, 0 Fehler.
- **`notebooks/07_results.ipynb`** neu angelegt — übernimmt den kompletten Inhalt von
  `docs/RESULTS.md` (Objective, Modeling Journey, Results intern + AIM-true-holdout,
  Robustheits-Checks, Lessons Learned, Recommendations). AIM-Zahlen (Baseline F1 0.2799,
  Champion F1 0.409 @0.65) werden live gegen `target_aim.csv` reproduziert, nicht kopiert —
  reproduziert exakt die zuvor dokumentierten Werte. Deterministisch per nbconvert ausgeführt,
  0 Fehler. **`docs/RESULTS.md` danach gelöscht** (Inhalt lebt jetzt im Notebook, MD-Anti-Pattern
  „Findings in MD-Files" damit aufgelöst).
- **README.md** aktualisiert: Notebook-Tabelle (+06, +07), alle `docs/RESULTS.md`-Links auf
  `notebooks/07_results.ipynb` umgebogen, Error-Analysis-Finding in TL;DR + Results-Section
  ergänzt, Approach-Section um Error-Analysis-Schritt erweitert.
- **Nächster Schritt:** `/project-case story` (`public/md/portfolio.md`) → `slides` (Dialog) →
  `report` (`make portfolio`).

## 2026-07-09 — BACKLOG #20: Notebook-Header-Format-Feinschliff

- Alle 12 Notebooks gegen das Pflicht-Format aus `wgnd-skills/project-case/project-case.md`
  geprüft (`# Titel` + `**SUBTITLE**` + `---` **in einer** Markdown-Zelle) — Script zeigte alle 12
  als ❌, weil Title und Subtitle projektweit in zwei getrennten Zellen standen (nicht nur in den
  3 im Backlog explizit genannten Notebooks).
- **Alle 12 Notebooks**: Title-Zelle + Subtitle-Zelle zu einer Zelle zusammengeführt, Text
  unverändert. Direkt per JSON-Patch (nicht NotebookEdit) — `03a_modelling-logreg.ipynb` u.a. sind
  zu gross fürs Read-Tool-Preflight von NotebookEdit; Formatierung (`indent=1`, `ensure_ascii=False`,
  Trailing-Newline) manuell an den Originalstil angeglichen, um den Diff auf die Header-Zellen zu
  begrenzen. Mit `nbformat.validate()` gegengeprüft — alle 12 valide, keine Outputs/Code-Zellen
  angefasst.
- **`00_introduction.ipynb`**: Subtitle DE→EN.
- **`03a_modelling-logreg.ipynb`**: Titel DE→EN (Subtitle war schon EN).
- **`01_exploring.ipynb`**: Cell 0 war ein verwaister `---`-Divider vor dem eigentlichen Titel
  (nichts davor zu trennen), Cell 1 „# Preparation" passte nicht zum Inhalt (Setup/Data
  Gathering/Split — „Preparation" ist inhaltlich der Job von `02_processing.ipynb`). Beide Zellen
  durch einen neuen Header ersetzt: „# Exploring" + Subtitle „SETUP · SPLIT · EXPLORATORY DATA
  ANALYSIS". Mid-Notebook-Kapiteltitel „Explorative Data Analysis" → „Exploratory Data Analysis"
  (EN); der `---`-Divider davor blieb unangetastet (regulärer Kapitel-Break, kein Bug).
- **Nächster Schritt:** BACKLOG #21 — Kay: manuelle Durchsicht der `public/`-Artefakte, letzter
  Schritt vor Phase-5-Abschluss.

## 2026-07-10 — Toolkit-Konsolidierung: ModelTracker → gemeinsames `wgnd` (Workspace-BACKLOG #24)

- **`ModelTracker` + `save_model` ins gemeinsame `wgnd-toolkit` (v0.3.0) promotet**, dieses Projekt
  konsumiert sie jetzt von dort statt aus dem lokalen Fork. Ebenso `EdaNotes`/`notes`.
- **`src/us_used_vehicle_resales/__init__.py`**: `ModelTracker`/`save_model`/`EdaNotes`/`notes` via
  `from wgnd import …` (Re-Export bleibt, `wg.ModelTracker` in den Notebooks unverändert nutzbar).
- **`models.py`** auf `inspect_run_full` reduziert — bleibt bewusst lokal (LogReg-/`Good/Bad`-/
  IsBadBuy-spezifisch, kein allgemeiner Toolkit-Kandidat). **`printing.py`** auf die `print_*`-Helfer
  reduziert (von `process.py` genutzt); `EdaNotes`/`notes` raus. Tote `utils.py` (Quito-Copy-Paste,
  nirgends importiert) entfernt.
- **`pyproject.toml`**: `wgnd @ git+…@main` als Dependency ergänzt (analog zh-tram-flow etc.), alte
  „helpers live locally / consolidation planned"-Notiz entfernt. **README** entsprechend geflippt.
- **Entscheidung:** `process`-Split-Funktionen NICHT promotet (projekt-spezifisch) → bleiben lokal.
- **Verifiziert:** Paket-Import ok, `wg.ModelTracker is wgnd.ModelTracker`, ModelTracker-Smoke-Run
  grün (gegen lokal editable-installiertes Toolkit 0.3.0; `uv run --no-sync`, da git@main bis zu
  Kays Push noch 0.2.0 ist). Notebooks bewusst NICHT per nbconvert ausgeführt (würde gespeicherte
  Outputs überschreiben + braucht 448-Run-Daten) — API identisch, Re-Run bleibt Kay überlassen.
- **Nächster Schritt:** Kay pusht `wgnd-toolkit` (Tag `v0.3.0`) → danach ziehen Consumer via
  normalem `uv sync` die neue Version; erst dann `wgnd`-Dep in us-used ohne `--no-sync` auflösbar.
