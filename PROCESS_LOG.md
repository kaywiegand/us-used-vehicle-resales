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
- **Nächster Schritt:** Phase 3 — Notebook-Hygiene (Intro bereinigen, `03a/03b`,
  Tabellen, lose Artefakte verschieben).
