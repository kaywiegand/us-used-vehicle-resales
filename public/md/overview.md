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

**Bad-Buy Prediction | Fehlkäufe vor dem Kauf erkennen**
**Data-Science-Projekt mit 448-Runs-Experimentierframework | StackFuel Capstone**

* **65.620** — Auktions-Fahrzeuge
* **12,35 %** — Bad-Buy-Rate (unausgewogen)
* **F1 0,42** — Champion-Modell (Test)
* **448** — systematisch getestete Modell-Läufe

## Inhaltsübersicht
*Die wichtigsten Informationen mit Fokus auf Business-Impact*

1. Einstieg
2. Data & Exploration
3. Systematisches Experimentieren
4. Key Findings
5. Empfehlungen & Opportunities


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

## Class Imbalance
*12,35 % Bad Buys — Balance als Kern der Herausforderung*


## Bivariate Risk-Analyse
*Text-Spalten ohne offensichtlichen Zahlenwert sind die stärksten Risikotreiber*



---

### Systematisches Experimentieren

## Die Testreihe
*448 protokollierte Durchläufe in rund einer Stunde aktiver Rechenzeit*

* **448** — geloggte Durchläufe (19 Feature-Sets × 6 Modellfamilien)
* **3 Sek.** — Median-Abstand zwischen Durchläufen
* **~62 Min.** — aktive Rechenzeit für alle 448 Durchläufe zusammen
> Nach einer Stunde Wartezeit steht sofort eine auswertbare Tabelle mit allen 448 Kombinationen zur Verfügung.


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

### Ende

## US Used Vehicle Resales
*Bad-Buy Prediction bei Gebrauchtwagen-Auktionen<br>Data-Science-Projekt | StackFuel Capstone*

> Fast leer und doch stark
