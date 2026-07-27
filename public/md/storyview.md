# US Used Vehicle Resales

**Projekt:** US Used Vehicle Resales
**Beschreibung:** Der komplette Projektverlauf
**Autor:** Kay Wiegand
**Zielgruppe:** Portfolio · Konferenz · Vollbild
**Dauer:** 25 Minuten
**Zeitraum:** StackFuel Capstone
**GitHub:** [kaywiegand/us-used-vehicle-resales](https://github.com/kaywiegand/us-used-vehicle-resales)

---


---

### Einstieg

# US Used Vehicle Resales

**Bad-Buy Prediction | Fehlkäufe vor dem Kauf erkennen**
**Data-Science-Projekt mit 448-Runs-Experimentierframework | StackFuel Capstone**

* **65.620** — Auktions-Fahrzeuge
* **12,35 %** — Bad-Buy-Rate
* **448** — geloggte Modell-Läufe
* **F1 0,37 → 0,42** — Champion, Threshold getunt

## Inhaltsübersicht
*Der komplette Projektverlauf — von der Exploration bis zur Empfehlung*

1. Einstieg
2. Data & Exploration
3. Systematisches Experimentieren
4. Key Findings
5. Results & Error Analysis
6. Empfehlungen & Opportunities
7. Project Insights


---

### Einstieg

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

### Data & Exploration

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


## Blinder Fleck — verpasste Fehlkäufe
*Warum ein Drittel der Bad Buys unentdeckt bleibt*

> Das Modell verlässt sich stark auf ein einziges Signal und hat kein zweites für neuere, teurere Autos, die trotzdem ein Fehlkauf sind.

## Fälschlich markierte gute Autos
*Der akzeptable Preis eines Triage-Filters*

> <span class="sw-normal">Die zu Unrecht markierten guten Autos (FP) sind im Schnitt $1.740 günstiger und 2,3 Jahre älter als die korrekt durchgewunkenen (TN).</span><br><br><span class="sw-thin">Ein akzeptabler Kompromiss, weil diese Fahrzeuge günstig einzeln nachzuprüfen sind.</span>


---

### Empfehlungen & Opportunities

## Empfehlungen
*Direkt umsetzbar für dieses Projekt*


## Opportunities
*Konkrete, noch offene nächste Schritte*



---

### Project Insights

## Learnings
*Methodik-Lehren fürs nächste Projekt — nicht spezifisch für diesen Datensatz*

* **Breites Netz vor Vorauswahl**
  - Vor dem Aussortieren ein breites Feature-Net casten — nicht vorher raten, was wichtig sein könnte.
* **Fehlen als Signal**
  - Prüfen, ob 'der Wert fehlt' selbst schon ein Signal ist, bevor man ihn stillschweigend auffüllt.
* **Batch-Statistiken einfrieren**
  - Median und Quantil-Grenzen einmal einfrieren, damit auch ein einzelnes neues Auto bewertet werden kann.
* **Gleicher Test-Set-Vergleich**
  - Alle Modell-Finalisten immer auf demselben Test-Set vergleichen — eine frühere Annahme 'Random Forest ist bestes Modell (F1 ~0,39)' hielt dem nicht stand (tatsächlich F1 0,35, Platz 2).


---

### Ende

## US Used Vehicle Resales
*Bad-Buy Prediction bei Gebrauchtwagen-Auktionen<br>Data-Science-Projekt | StackFuel Capstone*

> Fast leer und doch stark
