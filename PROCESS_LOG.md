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
- **Nächster Schritt:** Phase 2 — `src/` konsolidieren + wgnd-Toolkit integrieren
  (Notebooks vorher schliessen/speichern).
