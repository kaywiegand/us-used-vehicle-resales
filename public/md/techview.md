# US Used Vehicle Resales

**Projekt:** US Used Vehicle Resales
**Beschreibung:** Technischer Deep Dive
**Autor:** Kay Wiegand
**Zielgruppe:** Data Scientists · Tech Leads · Interviewer
**Dauer:** 15 Minuten
**Zeitraum:** StackFuel Capstone
**GitHub:** [kaywiegand/us-used-vehicle-resales](https://github.com/kaywiegand/us-used-vehicle-resales)

---


---

### Einstieg

# US Used Vehicle Resales

**Bad-Buy Prediction | Fehlkäufe vor dem Kauf erkennen**
**Data-Science-Projekt mit 448-Runs-Experimentierframework | StackFuel Capstone**

* **52.496 / 13.124** — Train / Test (stratifiziert)
* **28 / 6** — Features Champion / Modellfamilien getestet
* **F1 0,3726** — bester Tracker-Lauf (Val-Split)
* **F1 0,42** — Champion, Held-out-Test, Threshold 0,65

## Inhaltsübersicht
*Die wichtigsten Technical Insights als Data-Science Deep-Dive*

1. Einstieg
2. Datenstrategie
3. Systematisches Experimentieren
4. Key Findings
5. Results & Error Analysis
6. Empfehlungen & Opportunities
7. Project Insights


---

### Ausgangssituation

## Die Herausforderung
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
> <span class="sw-normal">Triage statt Automatik.</span><br><span class="sw-thin">Das Modell markiert Auffälligkeiten zur menschlichen Prüfung – kein automatisches Ablehnen oder Durchwinken.</span>


---

### Datenstrategie

## Dataset & Cleaning
*65.620 Fahrzeuge, 33 Rohspalten — nichts gelöscht, alles aufgefüllt*


## Class Imbalance
*12,35 % Bad Buys — Balance als Kern der Herausforderung*


## Bivariate Risk-Analyse
*Text-Spalten ohne offensichtlichen Zahlenwert sind die stärksten Risikotreiber*


## Preis-Korrelation → Feature Engineering
*8 redundante MMR-Preisspalten werden zu 3 Verhältnis-Features verdichtet*



---

### Systematisches Experimentieren

## Feature-Katalog & Model-Katalog
*19 Feature-Sets × 6 Modellfamilien statt Ad-hoc-Training*


## Der ModelTracker
*Selbstgebauter Experiment-Logger statt manuellem Vergleich*

> Kombinationen aus Model- und Feature-Kataloge

## Die Testreihe
*448 protokollierte Durchläufe in rund einer Stunde aktiver Rechenzeit*

* **448** — geloggte Durchläufe (19 Feature-Sets × 6 Modellfamilien)
* **3 Sek.** — Median-Abstand zwischen Durchläufen
* **~62 Min.** — aktive Rechenzeit für alle 448 Durchläufe zusammen
> Nach einer Stunde Wartezeit steht sofort eine auswertbare Tabelle mit allen 448 Kombinationen zur Verfügung.

## Benchmark der Testreihe
*Top-10 von 448 Durchläufen nach F1*



---

### Key Findings

## Breiter Katalog schlägt Handpicking
*Kategoriale Signale sind kein Rauschen, sondern der Haupthebel*

> Noise mit wichtigem Informationsgehalt

## Der WheelType-Fund
*Das stärkste Signal ist ein fast leeres Datenfeld*


## Der WheelType-Fund
*95,6 % unauffällig gefüllt, aber die fehlenden 4,4 % sind der Alarm*

> Ein in 95,6 % der Fälle unauffälliges Feld wird in den restlichen 4,4 % zum stärksten Alarmsignal.

## Threshold-Tuning für Business-Balance
*Der Standard-Schwellenwert markiert zu viele Autos*


## Threshold-Tuning für Business-Balance
*F1 0,37 → 0,42 durch den richtigen Schwellenwert*

* **F1 0,37 → 0,42** — Threshold 0,5 → 0,65
* **Precision 0,45** — bei getuntem Threshold
* **Recall 0,40** — bei getuntem Threshold
> <span class="sw-normal">Ziel: Balance der Triage</span><br><span class="sw-thin">Fehlkäufe blockieren, gute Autos behalten – statt generischem 0,5-Standard.</span>


---

### Results & Error Analysis

## Modellvergleich
*Alle drei Kandidaten auf demselben Held-out-Test (13.124 Fahrzeuge)*


## Confusion Matrix
*Beim getunten Threshold 0,65*


## Robustheits-Checks
*Ist das Modell sauber, oder wurde geleakt?*

* **F1 0,409** — Champion auf echtem AIM-Holdout (7.292 Fahrzeuge)
* **~0,01** — Lücke intern → echter Holdout
* **0,003** — F1-Delta nach Entfernen von 2.082 memorisierbaren Kategorie-Levels
> <span class="sw-normal">Es gibt kein Leakage.</span><br><span class="sw-thin">Split vor Feature Engineering, keine target-abgeleiteten Features, 0 doppelte Zeilen über den Split hinweg — die Lücke zum echten Holdout ist der stärkste empirische Beleg, dass die internen Zahlen sauber sind.</span>

## Fehlerbild — FN/FP-Segmente
*Blinder Fleck bei verpassten Fehlkäufen, akzeptabler Trade-off bei Fehlalarmen*



---

### Empfehlungen & Opportunities

## Empfehlungen & Opportunities
*Einsatz heute, offene Schritte für morgen*



---

### Project Insights

## Project Insights
*Tech-Stack, Reproduzierbarkeit*

* **Tech-Stack**
  - Python · pandas · scikit-learn · Matplotlib/Seaborn · Jupyter · uv
* **Reproduzierbarkeit**
  - 12 Notebooks, durchgehend nummeriert (00–07) und ausgeführt
  - Selbstgebauter ModelTracker wandert perspektivisch ins eigene wgnd-toolkit

## Learnings
*Vier Methodik-Lehren, kompakt*

* **Breites Netz vor Vorauswahl**
  - Breites Feature-Net vor dem Aussortieren casten (F1 0,29 → 0,37, siehe Findings).
* **Fehlen als Signal**
  - Prüfen, ob 'fehlt' selbst ein Signal ist, bevor man auffüllt (WheelType-Fund).
* **Batch-Statistiken einfrieren**
  - Batch-Statistiken für Einzelfall-Scoring einfrieren (Median-Imputation, Quantil-Bins).
* **Gleicher Test-Set-Vergleich**
  - Alle Finalisten auf demselben Test-Set vergleichen — RF-0,39-Annahme widerlegt (tatsächlich 0,35).


---

### Ende

## US Used Vehicle Resales
*Bad-Buy Prediction | Fehlkäufe vor dem Kauf erkennen<br>Data-Science-Projekt mit 448-Runs-Experimentierframework | StackFuel Capstone*

> Fast leer und doch stark
