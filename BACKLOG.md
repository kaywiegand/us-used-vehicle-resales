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
| 5 | **⏸ GEPARKT** — `show_df()`-Tabellen zu Plots (CONVENTIONS). Gebündelt mit dem Notebook-Run-Loop, wenn Exploration angefasst wird (Kay 2026-07-09). | 2 | project-review 2026-06-27 |
| 19 | **⏸ GEPARKT** — `01_exploring` in 4 thematische NBs splitten (`_0-setup-split`/`_1-quality`/`_2-distributions`/`_3-relationships`). Gekoppelt an Run-Loop (jedes Stück Setup/Load + lauffähig machen). Aktuell bleibt `01` unverändert. | 2 | 2026-07-09 |
| ~~6~~ | ✅ Phase 3: lose Artefakte verschoben (PNG → reports/img/, Dictionary → reports/, Dumps → docs/) (41cf47b) | 2 | project-review 2026-06-27 |
| ~~7~~ | ✅ Phase 4: voller englischer README mit echten Zahlen + Key Visual (1741535) | 1 | project-review 2026-06-27 |
| ~~8~~ | ✅ Phase 4: `DATA_DICTIONARY.md` (33 Spalten + Known Issues) (1741535) | 2 | project-review 2026-06-27 |
| ~~9~~ | ✅ Phase 4: `reports/index.html` + 5 Charts in `reports/img/` (1741535) | 1 | project-review 2026-06-27 |
| ~~10~~ | ✅ Paketname `us_used_vehicle_resales` beibehalten (Slug-konform) | 3 | Planung 2026-06-27 |
| ~~12~~ | ✅ `tests/test_import.py` — Smoke-Tests (Paket + Module + Katalog-Keys), 3 passed (2026-07-09) | 3 | Phase 2 2026-06-27 |
| 11 | Phase 5: `/project-review` erneut ✅ (BEDINGT, 2026-07-09), dann `/project-case` | 1 | project-review 2026-06-27 |
| ~~13~~ | ✅ **Results-Story korrigiert**: `04_evaluation.ipynb` als SSoT; Winner = LogReg Lasso (F1 0.37 / 0.42 tuned), RF-0.39-Claim retired; README+Hub umgeschrieben (2026-07-09) | 1 | content-audit 2026-07-09 |
| ~~14~~ | ✅ **Test-Metriken reproduzierbar**: alle 3 Modelle auf demselben Held-out-Test in `04_evaluation.ipynb`, deterministisch per nbconvert ausgeführt (2026-07-09) | 1 | content-audit 2026-07-09 |
| ~~18~~ | ✅ **Data-Leakage-Audit** (`docs/DATA_LEAKAGE_AUDIT.md`): kein Leakage, kein High-Card-Overfitting (−0.003 F1); niedriger Prüfer-Score = Baseline statt Champion eingereicht (2026-07-09) | 1 | Kay 2026-07-09 |
| 15 | **Notebooks reproduzierbar durchlaufen** (`01`–`03b` Outputs stale, aus Lernphase): top-to-bottom rerun im Run-Loop. Entscheidung 2026-07-09: **Outputs bewusst committet behalten**, `nbstripout`-Dep entfernt (war inaktiv). Rerun offen, gebündelt mit #19. | 2 | content-audit 2026-07-09 |
| ~~16~~ | ✅ **AIM-Deliverable geschärft**: `04_evaluation.ipynb` erzeugt EIN kanonisches `predictions_aim_final.csv` mit getuntem Threshold (0.65) + Triage-Framing; auf echten AIM-Labels validiert (F1 0.409). (2026-07-09) | 2 | content-audit 2026-07-09 |
| 17 | **`feat_price_cat` qcut-Bug**: `pd.qcut` bildet Bin-Grenzen pro Datensatz → train/test/aim inkonsistent. Auf feste Grenzen (aus Train-Quantilen) umstellen, in Pipeline fitten. | 2 | content-audit 2026-07-09 |
| ~~20a~~ | ✅ **Error Analysis fehlte** — `06_error_analysis.ipynb` neu: Confusion Matrix + FN/FP-Segmentanalyse (Blind-Spot: neuere/teurere Bad Buys ohne `WheelType=Unknown`). (2026-07-09) | 1 | project-case check 2026-07-09 |
| ~~20b~~ | ✅ **`docs/RESULTS.md` → Notebook migriert** — `07_results.ipynb` übernimmt vollständigen Inhalt (Numbers gehören in Notebooks, nicht MD), AIM-Zahlen live gegen `target_aim.csv` reproduziert. `docs/RESULTS.md` gelöscht. (2026-07-09) | 1 | Kay 2026-07-09 |
| 20 | **Notebook-Header-Format-Feinschliff**: Title/Subtitle in eine Zelle zusammenführen (Standard), `01_exploring` Zellreihenfolge + Titel „Preparation" korrigieren (passt nicht zum Inhalt), `03a`/`00`-Subtitle von Deutsch auf Englisch. | 2 | project-case check 2026-07-09 |
| 21 | **Kay: manuelle Durchsicht der public-Artefakte** (`public/index.html`, `overview.html`, `storyview.html`, `techview.html`) — letzter Schritt vor Projekt-Abschluss, bevor Phase 5 wirklich als fertig gilt. | 1 | Kay 2026-07-09 |
