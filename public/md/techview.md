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

**Bad-Buy Prediction als Klassifikations-Case**
**Feature-Katalog · Model-Katalog · ModelTracker · Error Analysis**

* **52.496 / 13.124** — Train / Test (stratifiziert)
* **28 / 6** — Features Champion / Modellfamilien getestet
* **F1 0,3726** — bester Tracker-Lauf (Val-Split)
* **F1 0,42** — Champion, Held-out-Test, Threshold 0,65

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

### Datenstrategie

## Dataset & Cleaning
*65.620 Fahrzeuge, 33 Rohspalten — nichts gelöscht, alles aufgefüllt*

* **Datensatz**
  - 65.620 Trainings-Fahrzeuge, 33 Rohspalten, StackFuel-Capstone-Datensatz
  - Stratifizierter Split: 52.496 Train / 13.124 Test, 12,35 % Bad-Buy-Rate in beiden identisch erhalten
* **Bereinigt**
  - 106.348 kategoriale Lücken über mehrere Spalten (u. a. Trim, SubModel, Color, WheelType) gefunden und mit 'Unknown' aufgefüllt statt gelöscht
  - PRIMEUNIT und AUCGUART fehlen bei 95,3 % aller Fahrzeuge — bleiben trotzdem als eigene Kategorie drin
  - 621 unplausible Preis-/Alters-/Kilometerstand-Werte (z. B. Preis < 100 $) über gestufte Gruppen-Median-Imputation geheilt (Modell+Baujahr → Marke+Baujahr → Alter → Baujahr)
* **Ergebnis**
  - 0 Zeilen gelöscht — 100 % Retention Rate, jedes Auto bleibt im Datensatz

## Class Imbalance
*12,35 % Bad Buys — der Kern der Herausforderung*


## Bivariate Risk-Analyse
*Text-Spalten ohne offensichtlichen Zahlenwert sind die stärksten Risikotreiber*


## Preis-Korrelation → Feature Engineering
*8 redundante MMR-Preisspalten werden zu 3 Verhältnis-Features verdichtet*



---

### Systematisches Experimentieren

## Feature-Katalog & Model-Katalog
*19 Feature-Sets × 6 Modellfamilien statt Ad-hoc-Training*

* **Feature-Katalog — jede Gruppe testet eine Ja/Nein-Frage**
  - baseline_minimal (4 Feat.): Nullpunkt — was passiert mit fast nichts?
  - numeric (6 Feat.): nur rohe Zahlen, keine Kategorien — Referenzwert
  - modern_engineered_only: helfen die gebauten Ratio-/Bin-Features auch ohne komplexe Kategorien?
  - cats_strong / high_impact_categories (7 Feat.): nur die im Risk-Spread-Plot entdeckten starken Kategorien
  - cats_weak: die schwächeren Kategorien (Farbe, Getriebe) — Rauschen oder Signal?
  - champion_v1: beste Kategorien + beste Engineered-Features + Basis-Zahlen kombiniert
  - all_in_with_noise (28 Feat.): wirklich alles rein — verschlechtert sich der Score durch Rauschen?
* **Model-Katalog — 3 Lernprinzipien, je 2 Ausbaustufen**
  - Logistische Regression: Ridge (L2, alle Features geschrumpft) vs. Lasso (L1, Feature-Selektion — macht Koeffizienten als Wichtigkeits-Ranking lesbar)
  - Random Forest: flach (Tiefe 7) vs. tief (Tiefe 15) — mehr Baum-Komplexität sinnvoll oder Überanpassung?
  - HistGradientBoosting: Standard vs. aggressiv — der 'State of the Art'-Kandidat für Tabellendaten

## Der ModelTracker
*Selbstgebauter Experiment-Logger statt manuellem Vergleich*

> Pro Durchlauf werden F1, Recall, Precision und ROC-AUC in eine dauerhafte CSV geschrieben. Ein neuer Bestwert wird automatisch markiert. Das Modell selbst wird nur bei Bestwert oder F1 ≥ 0,30 exportiert ('Smart Export') — kein Datenmüll durch schwache Modelle.

## Die Testreihe
*448 protokollierte Durchläufe in rund einer Stunde aktiver Rechenzeit*

* **448** — geloggte Durchläufe (19 Feature-Sets × 6 Modellfamilien)
* **3 Sek.** — Median-Abstand zwischen Durchläufen
* **~62 Min.** — aktive Rechenzeit für alle 448 Durchläufe zusammen
> Der Vorteil: nach knapp einer Stunde Wartezeit steht eine fertige, sofort auswertbare Tabelle mit allen 448 Kombinationen — statt einzeln nacheinander von Hand zu trainieren und zu vergleichen.

## Die Testreihe
*Top-10 von 448 Durchläufen nach F1*



---

### Key Findings

## Breiter Katalog schlägt Handpicking
*Kategoriale Signale sind kein Rauschen, sondern der Haupthebel*

> Der Unterschied hält über mehrere Modellfamilien hinweg — kein Zufallstreffer. Casting a wide net statt Vorab-Auswahl nach vermuteter Wichtigkeit war der entscheidende Schritt, nicht ein bestimmter Algorithmus.

## Der WheelType-Fund
*Das stärkste Signal ist ein fast leeres Datenfeld*


## Der WheelType-Fund
*95,6 % unauffällig gefüllt, aber die fehlenden 4,4 % sind der Alarm*

> Ein Feld, das in 95,6 % der Fälle einfach normal ausgefüllt und damit unauffällig ist, wird in den seltenen 4,4 % zum stärksten Alarmsignal im ganzen Datensatz — sechsmal höher als der Durchschnitt.

## Threshold-Tuning für Business-Balance
*Der Standard-Schwellenwert markiert zu viele Autos*


## Threshold-Tuning für Business-Balance
*F1 0,37 → 0,42 durch den richtigen Schwellenwert*

* **F1 0,37 → 0,42** — Threshold 0,5 → 0,65
* **Precision 0,45** — bei getuntem Threshold
* **Recall 0,40** — bei getuntem Threshold
> Abgestimmt auf den Triage-Zweck: Fehlkäufe fangen, ohne zu viele gute Autos abzulehnen — nicht auf einen generischen 0,5-Default.


---

### Results & Error Analysis

## Modellvergleich
*Alle drei Kandidaten auf demselben Held-out-Test (13.124 Fahrzeuge)*


## Confusion Matrix
*Beim getunten Threshold 0,65*


## Fehlerbild — FN/FP-Segmente
*Blinder Fleck bei verpassten Fehlkäufen, akzeptabler Trade-off bei Fehlalarmen*



---

### Empfehlungen & Opportunities

## Empfehlungen & Opportunities
*Einsatz heute, offene Schritte für morgen*



---

### Learnings & Ausblick

## Projekt-Rahmen
*Tech-Stack, Reproduzierbarkeit, Links*

* **Tech-Stack**
  - Python · pandas · scikit-learn · Matplotlib/Seaborn · Jupyter · uv
* **Reproduzierbarkeit**
  - 12 Notebooks, durchgehend nummeriert (00–07) und ausgeführt
  - Selbstgebauter ModelTracker wandert perspektivisch ins eigene wgnd-toolkit

## Learnings
*Vier Methodik-Lehren, kompakt*

* **Learnings**
  - Breiten Feature-Net vor dem Aussortieren casten (F1 0,29 → 0,37, siehe Findings)
  - Prüfen, ob 'fehlt' selbst ein Signal ist, bevor man auffüllt (WheelType-Fund)
  - Batch-Statistiken für Einzelfall-Scoring einfrieren (Median-Imputation, Quantil-Bins)
  - Alle Finalisten auf demselben Test-Set vergleichen — RF-0,39-Annahme widerlegt (tatsächlich 0,35)


---

### Ende

## US Used Vehicle Resales
*Kay Wiegand*

* **52.496 / 13.124** — Train / Test
* **28** — Features Champion
* **448** — geloggte Modell-Läufe
* **F1 0,42** — Champion, getunter Threshold
