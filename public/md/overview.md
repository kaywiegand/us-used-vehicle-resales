# US Used Vehicle Resales

**Projekt:** US Used Vehicle Resales
**Beschreibung:** Ergebnisse & Handlungsempfehlungen
**Autor:** Kay Wiegand
**Zielgruppe:** HR · Business · Hiring Manager
**Dauer:** 8 Minuten
**Zeitraum:** StackFuel Capstone
**GitHub:** [kaywiegand/us-used-vehicle-resales](https://github.com/kaywiegand/us-used-vehicle-resales)

---


---

### Einstieg

# US Used Vehicle Resales

**Bad-Buy Prediction — Fehlkäufe vor dem Kauf erkennen**
**Data-Science-Projekt · 448-Runs-Experimentierframework**

* **65.620** — Auktions-Fahrzeuge
* **12,35 %** — Bad-Buy-Rate (unausgewogen)
* **F1 0,42** — Champion-Modell (Test)
* **448** — systematisch getestete Modell-Läufe

## Das Problem
*Ein Fehlkauf beim Gebrauchtwagen-Ankauf kostet mehr als den Kaufpreis*

> Ein US-Gebrauchtwagenhändler kauft Fahrzeuge günstig auf Auktionen ein, um sie mit Marge weiterzuverkaufen. Das größte Risiko: ein 'Bad Buy' — ein Fahrzeug mit schweren Mängeln, das sich nicht weiterverkaufen lässt und stattdessen Lager-, Reparatur- und Abschreibungskosten verursacht.
> Leitfrage: Lässt sich vor dem Kauf erkennen, ob ein Angebot ein Fehlkauf ist — ohne zu viele gute Autos abzulehnen? Das ist ein Precision/Recall-Abwägungsproblem auf einer seltenen Zielklasse, kein Accuracy-Problem.

## Zielmetrik und Trade-off
*Warum Accuracy hier die falsche Metrik ist*

* **12,35 %** — Bad-Buy-Rate
im Datensatz
  - Nur jedes achte Auto ist ein Fehlkauf — eine stark unausgewogene Zielklasse.
* **87,65 %** — Accuracy eines
Stumpfen Modells
  - Ein Modell, das stur immer 'guter Kauf' tippt, hätte schon 87,65 % Accuracy — und würde trotzdem keinen einzigen Fehlkauf erkennen.
* **F1** — Leitmetrik
(Bad-Buy-Klasse)
  - F1 der Bad-Buy-Klasse zwingt das Modell, die seltene Klasse tatsächlich zu treffen statt sie zu ignorieren.
> Rahmen: Triage, nicht Automatik. Das Modell soll auffällige Fahrzeuge markieren, damit ein Mensch sie prüft — nicht automatisch ablehnen oder automatisch durchwinken.


---

### Data & Exploration

## Class Imbalance
*12,35 % Bad Buys — der Kern der Herausforderung*


## Bivariate Risk-Analyse
*Text-Spalten ohne offensichtlichen Zahlenwert sind die stärksten Risikotreiber*



---

### Systematisches Experimentieren

## Die Testreihe
*448 protokollierte Durchläufe in rund einer Stunde aktiver Rechenzeit*

* **448** — geloggte Durchläufe (19 Feature-Sets × 6 Modellfamilien)
* **3 Sek.** — Median-Abstand zwischen Durchläufen
* **~62 Min.** — aktive Rechenzeit für alle 448 Durchläufe zusammen
> Der Vorteil: nach knapp einer Stunde Wartezeit steht eine fertige, sofort auswertbare Tabelle mit allen 448 Kombinationen — statt einzeln nacheinander von Hand zu trainieren und zu vergleichen.


---

### Key Findings

## Der WheelType-Fund
*Das stärkste Signal ist ein fast leeres Datenfeld*


## Threshold-Tuning für Business-Balance
*Der Standard-Schwellenwert markiert zu viele Autos*



---

### Empfehlungen & Opportunities

## Empfehlungen
*Direkt umsetzbar für dieses Projekt*


## Opportunities
*Konkrete, noch offene nächste Schritte*



---

### Learnings & Ausblick

## Projekt-Rahmen
*Tech-Stack, Reproduzierbarkeit, Links*

* **Tech-Stack**
  - Python · pandas · scikit-learn · Matplotlib/Seaborn · Jupyter · uv
* **Reproduzierbarkeit**
  - 12 Notebooks, durchgehend nummeriert (00–07) und ausgeführt
  - Selbstgebauter ModelTracker wandert perspektivisch ins eigene wgnd-toolkit


---

### Ende

## US Used Vehicle Resales
*Kay Wiegand*

* **65.620** — Auktions-Fahrzeuge
* **448** — geloggte Modell-Läufe
* **F1 0,42** — Champion, getunter Threshold
