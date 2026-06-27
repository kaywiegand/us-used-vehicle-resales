"""
Zentraler Feature-Baukasten für das Car-Buy (BadBuy) Projekt.
Strukturiert nach Risiko-Hypothesen (Feature Groups).
FT_GROUP_ALL ist die vertikale Master-Liste für maximale Kontrolle.
"""


# Numerische Basis-Werte (Kontinuierlich)
FT_DOMAIN_NUMERIC = [
    'VehicleAge', 'VehOdo', 'VehBCost', 'WarrantyCost',
    'MMRAcquisitionAuctionAveragePrice', 'MMRCurrentAuctionAveragePrice'
]

# Deine berechneten Ratios (Informing the Model)
FT_DOMAIN_ENGINEERED_RATIOS = [
    'feat_miles_per_year', 'feat_price_ratio', 
    'feat_price_diff', 'feat_market_trend', 'feat_warranty_ratio'
]

# Deine neuen Risiko-Schubladen (Feature Binning)
FT_DOMAIN_ENGINEERED_BINS = [
    'feat_age_group', 'feat_odo_risk', 'feat_price_cat', 'feat_warranty_peak'
]

# Die starken Kategorien aus dem Ranking (High Impact)
FT_DOMAIN_CATEGORICAL_STRONG = [
    'Make', 'Model', 'Trim', 'SubModel', 'VNZIP1', 'Auction', 'WheelType'
]

# Die schwächeren Kategorien (Noise Check)
FT_DOMAIN_CATEGORICAL_WEAK = [
    'Color', 'Transmission', 'Nationality', 'Size', 'TopLineQuote', 'IsOnlineSale'
]

FT_GROUP_HISTORY = [
    'VehYear', 
    'VehicleAge', 
    'VehOdo', 
    'feat_miles_per_year'
]

FT_GROUP_BASELINE = [
    'VehicleAge', 'VehOdo', 'VehBCost',                     # Die Basics
    'MMRAcquisitionAuctionAveragePrice',                    # Ein solider Preisanker
    'feat_miles_per_year', 'feat_price_ratio',              # Deine besten neuen Features
    'Auction', 'Make'                                       # Die wichtigsten Kategorien
]

FT_GROUP_PRICE_DETAILED = [
    'MMRAcquisitionAuctionAveragePrice', 
    'MMRAcquisitionAuctionCleanPrice',
    'MMRAcquisitionRetailAveragePrice', 
    'MMRAcquisitonRetailCleanPrice',
    'MMRCurrentAuctionAveragePrice', 
    'MMRCurrentAuctionCleanPrice',
    'MMRCurrentRetailAveragePrice', 
    'MMRCurrentRetailCleanPrice',
    'VehBCost',
    'feat_price_ratio', 
    'feat_price_diff',
    'feat_market_trend'
]

FT_GROUP_RISK_PROXY = [
    'WarrantyCost', 
    'feat_warranty_ratio', 
    'IsOnlineSale'
]





features_catalog = {
    "baseline": FT_GROUP_BASELINE,
    "risk": FT_GROUP_RISK_PROXY,
    "price": FT_GROUP_PRICE_DETAILED,
    "history": FT_GROUP_HISTORY,
    "numeric": FT_DOMAIN_NUMERIC,
    "ratios": FT_DOMAIN_ENGINEERED_RATIOS,
    "bins": FT_DOMAIN_ENGINEERED_BINS,
    "cats_strong": FT_DOMAIN_CATEGORICAL_STRONG,
    "cats_weak": FT_DOMAIN_CATEGORICAL_WEAK,

    # 1. DER NULLPUNKT (Minimalistischer Test)
    # Ziel: Was passiert, wenn wir fast gar nichts machen?
    "baseline_minimal": ['VehicleAge', 'VehOdo', 'VehBCost', 'Auction'],
    "baseline_min_woVO": ['VehicleAge', 'VehBCost', 'Auction'],
    "baseline_min_woVA": [ 'VehOdo', 'VehBCost', 'Auction'],

    # 2. DER KLASSIKER (Traditioneller Ansatz)
    # Ziel: Alle numerischen Original-Daten + die offensichtliche Marke.
    "baseline_classic": FT_DOMAIN_NUMERIC + ['Make'],

    # 3. DER "HYPOTHESEN-CHECK" (Engineering Power)
    # Ziel: Helfen unsere berechneten Ratios und Bins dem Modell wirklich?
    # Wir lassen die komplexen Kategorien (VNZIP1 etc.) hier bewusst weg.
    "modern_engineered_only": FT_DOMAIN_ENGINEERED_RATIOS + FT_DOMAIN_ENGINEERED_BINS + ['VehicleAge'],

    # 4. DIE "DISCOVERY"-GRUPPE (EDA Power)
    # Ziel: Teste nur die starken Kategorien, die wir im Risk-Spread-Plot entdeckt haben.
    "high_impact_categories": FT_DOMAIN_CATEGORICAL_STRONG,

    # 5. DER "CHAMPION V1" (Best-of-Both-Worlds)
    # Ziel: Die stärksten Signale aus Engineering UND Discovery kombiniert.
    # Das ist aktuell unser heißester Kandidat für den Sieg.
    "champion_v1": [
        'VNZIP1', 'Trim', 'SubModel', 'Make',             # Top Kategorien (Signal)
        'feat_age_group', 'feat_price_ratio', 'feat_warranty_peak', # Engineered (Logik)
        'VehicleAge', 'VehOdo', 'VehBCost'                 # Basics (Stabilität)
    ],

    # 6. DER "NOISE-TEST" (Alles-oder-Nichts)
    # Ziel: Findet das Modell auch in schwachen Features (Farbe, Getriebe) noch Muster
    # oder verschlechtert sich der Score durch "Rauschen" (Overfitting)?
    "all_in_with_noise": (FT_DOMAIN_NUMERIC + FT_DOMAIN_ENGINEERED_RATIOS + 
                          FT_DOMAIN_ENGINEERED_BINS + FT_DOMAIN_CATEGORICAL_STRONG + 
                          FT_DOMAIN_CATEGORICAL_WEAK),
    
    "all_in": ['PurchDate', 'Auction', 'VehYear', 'VehicleAge', 'Make', 'Model',
       'Trim', 'SubModel', 'Color', 'Transmission', 'WheelTypeID', 'WheelType',
       'VehOdo', 'Nationality', 'Size', 'TopThreeAmericanName',
       'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice',
       'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitonRetailCleanPrice',
       'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice',
       'MMRCurrentRetailAveragePrice', 'MMRCurrentRetailCleanPrice',
       'PRIMEUNIT', 'AUCGUART', 'BYRNO', 'VNZIP1', 'VNST', 'VehBCost',
       'IsOnlineSale', 'WarrantyCost', 'feat_price_ratio', 'feat_price_diff',
       'feat_market_trend', 'feat_miles_per_year', 'feat_warranty_ratio',
       'feat_age_group', 'feat_odo_risk', 'feat_price_cat',
       'feat_warranty_peak'],

    "log_reg_set_01": [
        # --- Klassische numerische Spalten (für Log-Trafo/Scaling) ---
        'VehOdo', 
        'VehBCost', 
        'WarrantyCost',
        'VehicleAge',
        # --- Deine berechneten "Power-Features" (Ratios & Trends) ---
        'feat_price_ratio', 
        'feat_price_diff', 
        'feat_market_trend', 
        'feat_miles_per_year', 
        'feat_warranty_ratio',
        'feat_odo_risk',
        
        # --- Strategische Kategorien (für OHE) ---
        'Auction', 
        'Make', 
        'Color', 
        'Transmission', 
        'Size', 
        'VNST',             
        'IsOnlineSale', 
        'Nationality',
        'TopThreeAmericanName'
    ]
}




# --- 4. HILFSFUNKTION ---

def get_features(experiment_name):
    """Holt die Liste für ein Experiment aus dem Katalog."""
    return features_catalog.get(experiment_name, features_catalog["baseline_classic"])
