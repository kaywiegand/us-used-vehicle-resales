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
- [ ] **Phase 1 — Fundament (Schicht 1)** — MD-Files: CLAUDE · README (Gerüst) · ROADMAP · PROCESS_LOG · BACKLOG · `.python-version`; Eintrag in `docs/PROJECTS.md`.
- [x] **Phase 2 — src-Konsolidierung + wgnd-Toolkit** — ein Paket `us_used_vehicle_resales/`, Namenskollision `wgnd` aufgelöst, echtes Toolkit als Git-Dependency, `pyproject.toml` neu, Notebook-Imports repointed. Verifiziert (Install + Importe).
- [x] **Phase 3 — Notebook-Hygiene** — Intro neu (`00_introduction`), Modell-Notebooks linearisiert (`03_modelling-prep`, `03a/03b`, `04a/04b`), lose Artefakte verschoben. _Offen (→ BACKLOG #5): `show_df()`-Tabellen-Retrofit als optionaler Feinschliff._
- [ ] **Phase 4 — README + Reports (Schicht 2)** — voller README, `DATA_DICTIONARY.md`, `reports/index.html` + ≥3 Charts in `reports/img/`.
- [ ] **Phase 5 — Re-Review & Case Study** — `/project-review` erneut, dann `/project-case check → story → full`.

---

## Ziel

Ein portfolio-ready DSC-Projekt: reproduzierbares Setup (`uv` + `pip install -e ".[dsc]"`),
saubere lineare Notebook-Strecke, externes Leseartefakt (`reports/index.html`),
aussagekräftige README mit Findings + Modellvergleich (inkl. Baseline) — bereit für
`/project-case`.
