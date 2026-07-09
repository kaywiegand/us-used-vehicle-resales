# BACKLOG — US Used Vehicle Resales

Projektspezifische offene Tasks und Todos.
Nie mitten in einer Session den Kontext wechseln — hier notieren, gesammelt abarbeiten.

Prio: `1` = hoch · `2` = mittel · `3` = niedrig

---

| # | Beschreibung | Prio | Entdeckt in |
| :--- | :--- | :--- | :--- |
| ~~1~~ | ✅ Phase 2: `src/` konsolidiert, `wgnd`-Kollision aufgelöst, Toolkit als Dependency, `pyproject.toml` neu (538704c) | 1 | project-review 2026-06-27 |
| ~~2~~ | ✅ Phase 2: Notebook-Imports repointed (8 Notebooks) (538704c) | 1 | project-review 2026-06-27 |
| ~~3~~ | ✅ Phase 3: `00_introduction.ipynb` neu, LLM-Boilerplate entfernt (41cf47b) | 1 | project-review 2026-06-27 |
| ~~4~~ | ✅ Phase 3: Modell-Notebooks linearisiert `03a/03b`, `04a/04b` (41cf47b) | 2 | project-review 2026-06-27 |
| 5 | Phase 3 (offen): fehlende `show_df()`-Tabellen zu Plots ergänzen (CONVENTIONS) — optionaler Feinschliff | 2 | project-review 2026-06-27 |
| ~~6~~ | ✅ Phase 3: lose Artefakte verschoben (PNG → reports/img/, Dictionary → reports/, Dumps → docs/) (41cf47b) | 2 | project-review 2026-06-27 |
| ~~7~~ | ✅ Phase 4: voller englischer README mit echten Zahlen + Key Visual (1741535) | 1 | project-review 2026-06-27 |
| ~~8~~ | ✅ Phase 4: `DATA_DICTIONARY.md` (33 Spalten + Known Issues) (1741535) | 2 | project-review 2026-06-27 |
| ~~9~~ | ✅ Phase 4: `reports/index.html` + 5 Charts in `reports/img/` (1741535) | 1 | project-review 2026-06-27 |
| ~~10~~ | ✅ Paketname `us_used_vehicle_resales` beibehalten (Slug-konform) | 3 | Planung 2026-06-27 |
| 12 | `tests/`-Ordner mit Smoke-Test (Paket-Import) anlegen | 3 | Phase 2 2026-06-27 |
| 11 | Phase 5: `/project-review` erneut ✅ (BEDINGT, 2026-07-09), dann `/project-case` | 1 | project-review 2026-06-27 |
| ~~13~~ | ✅ **Results-Story korrigiert**: `04_evaluation.ipynb` als SSoT; Winner = LogReg Lasso (F1 0.37 / 0.42 tuned), RF-0.39-Claim retired; README+Hub umgeschrieben (2026-07-09) | 1 | content-audit 2026-07-09 |
| ~~14~~ | ✅ **Test-Metriken reproduzierbar**: alle 3 Modelle auf demselben Held-out-Test in `04_evaluation.ipynb`, deterministisch per nbconvert ausgeführt (2026-07-09) | 1 | content-audit 2026-07-09 |
| ~~18~~ | ✅ **Data-Leakage-Audit** (`docs/DATA_LEAKAGE_AUDIT.md`): kein Leakage, kein High-Card-Overfitting (−0.003 F1); niedriger Prüfer-Score = Baseline statt Champion eingereicht (2026-07-09) | 1 | Kay 2026-07-09 |
| 15 | **Notebooks reproduzierbar durchlaufen**: Outputs stale (autoreload, 5 vs 9 Features 04a/04b; alter Pfad `DSC_Gebrauchtwagen`). Top-to-bottom rerun im aktuellen venv; `nbstripout` aktivieren (pre-commit) oder bewusst Outputs committen. | 2 | content-audit 2026-07-09 |
| 16 | **AIM-Deliverable schärfen**: Predictions über-flaggen (40,6 %/27 % vs 12,35 %). Getunten Threshold (0.72, Precision ~0.50) nutzen, EIN eindeutiges Result-File definieren, Business-Framing (Triage-Filter) klarziehen. | 2 | content-audit 2026-07-09 |
| 17 | **`feat_price_cat` qcut-Bug**: `pd.qcut` bildet Bin-Grenzen pro Datensatz → train/test/aim inkonsistent. Auf feste Grenzen (aus Train-Quantilen) umstellen, in Pipeline fitten. | 2 | content-audit 2026-07-09 |
