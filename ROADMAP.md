# ROADMAP — US Used Vehicle Resales

> Ausgangslage → Phasen → Ziel

---

## Ausgangslage

StackFuel-Abschlussprojekt (DSC, Bad-Buy-Klassifikation) mit substanzieller,
ausgeführter Analyse- und Modellierungsarbeit (EDA, mehrere Modelle, Predictions
auf `features_aim`), aber **ohne Portfolio-Infrastruktur** und ursprünglich **nicht
versioniert**. Ziel der Aufbereitung: ein nach aussen verständliches Portfolio-Projekt,
das `/project-review` und `/project-case` sauber durchläuft.

Referenz-Standard: `zh-tram-flow` · Struktur-Referenz: `wgnd-scaffolding`.

---

## Phasen

- [x] **Phase 0 — Git Safety Net** — Repo initialisiert, `.gitignore`, Snapshot-Commit, Push zu origin.
- [x] **Phase 1 — Fundament (Schicht 1)** — MD-Files: CLAUDE · README (Gerüst) · ROADMAP · PROCESS_LOG · BACKLOG · `.python-version`; Eintrag in `docs/PROJECTS.md`.
- [x] **Phase 2 — src-Konsolidierung + wgnd-Toolkit** — ein Paket `us_used_vehicle_resales/`, Namenskollision `wgnd` aufgelöst, echtes Toolkit als Git-Dependency, `pyproject.toml` neu, Notebook-Imports repointed. Verifiziert (Install + Importe).
- [x] **Phase 3 — Notebook-Hygiene** — Intro neu (`00_introduction`), Modell-Notebooks linearisiert (`03_modelling-prep`, `03a/03b`, `04a/04b`), lose Artefakte verschoben. _Offen (→ BACKLOG #5): `show_df()`-Tabellen-Retrofit als optionaler Feinschliff._
- [x] **Phase 4 — README + Reports (Schicht 2)** — voller englischer README mit echten Zahlen + Key Visual, `DATA_DICTIONARY.md`, self-contained `public/index.html`, 5 Charts in `public/img/`.
- [x] **Phase 5 — Re-Review & Case Study** — `/project-review` (BEDINGT), `/project-case check → story → slides → report` komplett durchlaufen. Erledigt: Struktur-Cleanup · **Results-SSoT** `04_evaluation.ipynb` (Winner LogReg Lasso F1 0.37/0.42) · **Robustheits-Checks** auf echten AIM-Labels (kein Leakage; Champion F1 0.409) · `05_experiment_framework.ipynb` (ModelTracker-Showcase) · **`06_error_analysis.ipynb`** (Confusion Matrix, FN/FP-Segmentanalyse, Blind-Spot identifiziert) · **`07_results.ipynb`** (voller Report+Retrospektive, ersetzt `docs/RESULTS.md`) · Toolkit-Hygiene (toter Code + Phantom-`wgnd` raus) · Notebook-Format (Emoji-Header raus, eine Überschrift/Zelle, Title/Subtitle/ToC) · Intro/README angereichert · `tests/` Smoke-Test · **Portfolio-Case** (`public/md/portfolio.md` + `slides.yaml`, 32 Slides über Overview/StoryView/TechView, live im Browser verifiziert, Content-Overflow auf 5 Slides gefixt). **Erledigt (BACKLOG #19):** `01_exploring` in drei Notebooks gesplittet (`01` Setup/Split/erste Insights ·
`01a_eda-detail` Detail-EDA · `01b_eda-summary` Key Findings als Tabelle). **Geparkt:** `show_df`-Tabellen
(→ BACKLOG #5, Run-Loop). **Erledigt (BACKLOG #20):** Notebook-Header-Format-Feinschliff — Title/Subtitle in einer Zelle, `01_exploring`-Titel korrigiert, `00`/`03a` DE→EN. **Erledigt (2026-07-16):** Sprach-/Portfolio-Hygiene über alle Notebooks (`04`–`07` übersetzt, Data-Leakage-Audit-Narrativ entfernt, Chat-/Coach-Sprache + nummerierte Headlines + Lorem-Ipsum + leere Zellen bereinigt) und Modelling-Boilerplate (`03`/`03a`/`03b`, → BACKLOG #22) auf eine gemeinsame `build_pipeline()`-Funktion konsolidiert. **Offen (Kay, manuell):** finale Durchsicht der public-Artefakte (`public/index.html`, `overview.html`, `storyview.html`, `techview.html`) — letzter Schritt vor Projekt-Abschluss.

---

## Ziel

Ein portfolio-ready DSC-Projekt: reproduzierbares Setup (`uv` + `pip install -e ".[dsc]"`),
saubere lineare Notebook-Strecke, externes Leseartefakt (`public/index.html`),
aussagekräftige README mit Findings + Modellvergleich (inkl. Baseline) — bereit für
`/project-case`.
