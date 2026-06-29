# Data Dictionary — US Used Vehicle Resales

Jede Zeile des Datensatzes entspricht einem Fahrzeug, das in einer Auktion ersteigert
und anschliessend weiterverkauft wurde.

- **Trainingsdaten:** `data/01_raw/data_train.csv` — 65.620 Zeilen, 33 Spalten, **`;`-getrennt**, inkl. Label `IsBadBuy`.
- **Zieldatensatz:** `data/01_raw/features_aim.csv` — 7.291 Zeilen, ohne Label (Predictions = Deliverable).
- **Zielvariable:** `IsBadBuy` — Klassenbalance: `0` = 87,65 % · `1` = 12,35 % (stark unbalanciert).

> Rohdaten sind via `.gitignore` aus dem Repo ausgeschlossen. Quelle: StackFuel-Abschlussprojekt (Modul 3, Kapitel 4).

---

| # | Spalte | Datenniveau | Beschreibung |
|:--|:-------|:------------|:-------------|
| 1 | `IsBadBuy` | kategorisch (nominal) | **Zielvariable.** Fehlkauf ("Montagsauto")? `0` = guter Kauf, `1` = Montagsauto |
| 2 | `PurchDate` | datetime | Kaufdatum bei der Auktion |
| 3 | `Auction` | kategorisch | Auktionsanbieter |
| 4 | `VehYear` | int | Baujahr des Fahrzeugs |
| 5 | `VehicleAge` | int | Alter des Autos zum Auktionszeitpunkt |
| 6 | `Make` | kategorisch | Fahrzeughersteller |
| 7 | `Model` | kategorisch | Fahrzeugmodell |
| 8 | `Trim` | kategorisch | Ausstattungslinie |
| 9 | `SubModel` | kategorisch | Submodell |
| 10 | `Color` | kategorisch | Fahrzeugfarbe |
| 11 | `Transmission` | kategorisch | Getriebeart (Automatik, Manuell) |
| 12 | `WheelTypeID` | kategorisch | Typ-ID der Felgen |
| 13 | `WheelType` | kategorisch | Art der Felgen |
| 14 | `VehOdo` | int | Meilenstand (Odometer) |
| 15 | `Nationality` | kategorisch | Herkunftsland des Herstellers |
| 16 | `Size` | kategorisch | Grössenklasse (Kompakt, SUV, …) |
| 17 | `TopThreeAmericanName` | kategorisch | Einer der drei führenden US-Hersteller? |
| 18 | `MMRAcquisitionAuctionAveragePrice` | int | Anschaffungspreis (USD), Auktion, Durchschnittszustand, zum Kaufzeitpunkt |
| 19 | `MMRAcquisitionAuctionCleanPrice` | int | Anschaffungspreis (USD), Auktion, überdurchschnittlicher Zustand, zum Kaufzeitpunkt |
| 20 | `MMRAcquisitionRetailAveragePrice` | int | Anschaffungspreis (USD), Einzelhandel, Durchschnittszustand, zum Kaufzeitpunkt |
| 21 | `MMRAcquisitonRetailCleanPrice` | int | Anschaffungspreis (USD), Einzelhandel, überdurchschnittlicher Zustand, zum Kaufzeitpunkt _(Original-Tippfehler im Spaltennamen: "Acquisiton")_ |
| 22 | `MMRCurrentAuctionAveragePrice` | int | Preis (USD), Auktion, Durchschnittszustand, aktueller Tag |
| 23 | `MMRCurrentAuctionCleanPrice` | int | Preis (USD), Auktion, überdurchschnittlicher Zustand, aktueller Tag |
| 24 | `MMRCurrentRetailAveragePrice` | int | Preis (USD), Einzelhandel, Durchschnittszustand, aktueller Tag |
| 25 | `MMRCurrentRetailCleanPrice` | int | Preis (USD), Einzelhandel, überdurchschnittlicher Zustand, aktueller Tag |
| 26 | `PRIMEUNIT` | kategorisch | Höhere Nachfrage als ein Standardkauf? |
| 27 | `AUCGUART` | kategorisch | Garantielevel der Plattform (`GREEN` = Garantie, `YELLOW` = unklar, `RED` = keine) |
| 28 | `BYRNO` | kategorisch | Eindeutige Käufernummer |
| 29 | `VNZIP1` | kategorisch | Postleitzahl des Kaufs |
| 30 | `VNST` | kategorisch | US-Bundesstaat des Kaufs |
| 31 | `VehBCost` | int | Tatsächlich gezahlte Anschaffungskosten (USD) |
| 32 | `IsOnlineSale` | kategorisch | Ursprünglich online gekauft? |
| 33 | `WarrantyCost` | int | Garantiekosten für 36 Monate Laufzeit |

---

## Known Issues

- **Spaltenname-Tippfehler** im Original: `MMRAcquisitonRetailCleanPrice` (statt "Acquisition") — bewusst beibehalten, da Teil des Rohdatensatzes.
- **Fehlende Werte** v. a. in `PRIMEUNIT` und `AUCGUART` (oft leer). In der Modellierung wird fehlende `WheelType`-Information zu `Unknown` — und ist laut Random-Forest-Feature-Importance der **stärkste Einzelprädiktor** für einen Bad Buy.
- **Mehrere MMR-Preisspalten** sind stark korreliert (Acquisition/Current × Auction/Retail × Average/Clean) — relevant für Multikollinearität bei linearen Modellen.
