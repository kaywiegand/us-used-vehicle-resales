import pandas as pd
import numpy as np

import pandas as pd
import numpy as np

# --- 1. FEATURE MODULES ---

def add_price_features(df):
    """Preis-Logik: Berechnet Relationen zwischen Einkauf und Marktwert."""
    df = df.copy()
    # Verhältnis Einkauf zu Markt: Zeigt, ob wir zu teuer eingekauft haben
    df['feat_price_ratio'] = df['VehBCost'] / (df['MMRCurrentAuctionAveragePrice'] + 1)
    # Absolute Differenz: Wie weit weicht unser Preis vom Schnitt ab?
    df['feat_price_diff'] = df['VehBCost'] - df['MMRCurrentAuctionAveragePrice']
    # Markttrend: Sind die Preise seit der Auktion gestiegen oder gefallen?
    df['feat_market_trend'] = df['MMRCurrentAuctionAveragePrice'] - df['MMRAcquisitionAuctionAveragePrice']
    return df

def add_usage_features(df):
    """Nutzungs-Logik: Kilometer-Intensität."""
    df = df.copy()
    # (Age + 1) verhindert Division durch Null bei Neuwagen
    # Zeigt die Belastung: Viel gefahren in kurzer Zeit?
    df['feat_miles_per_year'] = df['VehOdo'] / (df['VehicleAge'] + 1)
    return df

def add_risk_features(df):
    """Risiko-Logik: Garantie-Metriken."""
    df = df.copy()
    # Garantiekosten im Verhältnis zum Preis: Hoher Anteil = hohes Defektrisiko?
    df['feat_warranty_ratio'] = df['WarrantyCost'] / (df['VehBCost'] + 1)
    return df

def add_eda_risk_bins(df):
    """EDA-Insights: Transformiert numerische Auffälligkeiten in Risiko-Kategorien."""
    df = df.copy()
    
    # 1. Lebensphasen: Ältere Autos haben ein exponentiell höheres Ausfallrisiko
    df['feat_age_group'] = pd.cut(df['VehicleAge'], 
                                   bins=[-1, 2, 5, 10, 100], 
                                   labels=['New', 'Standard', 'Old', 'Antique'])

    # 2. Kilometer-Extreme: U-Kurve (Ganz wenig = evtl. Tacho-Trick / Ganz viel = Verschleiß)
    df['feat_odo_risk'] = 'normal'
    df.loc[df['VehOdo'] < 30000, 'feat_odo_risk'] = 'low_odo_suspicious'
    df.loc[df['VehOdo'] > 90000, 'feat_odo_risk'] = 'high_odo_risk'

    # 3. Preis-Klassen: Billig-Autos ('Budget') sind statistisch häufiger Schrott
    df['feat_price_cat'] = pd.qcut(df['MMRAcquisitionAuctionAveragePrice'], 
                                   q=5, labels=['Budget', 'Economy', 'Mid', 'High', 'Premium'])

    # 4. Garantie-Cluster: Isoliert die zwei Risiko-Berge aus der EDA (3.5k und >5.5k)
    df['feat_warranty_peak'] = 'standard'
    df.loc[(df['WarrantyCost'] > 3000) & (df['WarrantyCost'] < 4000), 'feat_warranty_peak'] = 'peak_3500'
    df.loc[df['WarrantyCost'] > 5500, 'feat_warranty_peak'] = 'peak_high_risk'
    
    return df


# --- 2. ORCHESTRATOR ---

def engineer_features(df, print_status=True):
    """
    Hauptfunktion: Reichert den Datensatz an. 
    Gibt am Ende eine Liste der neu erstellten Features aus.
    """
    if print_status:
        print(f"{'='*55}")
        print(f" FEATURE ENGINEERING REPORT ")
        print(f"{'='*55}")
    
    # Vorher-Spalten merken
    old_cols = set(df.columns)
    
    df_feat = df.copy()
    
    # Kaskade der Anreicherung
    df_feat = add_price_features(df_feat)
    df_feat = add_usage_features(df_feat)
    df_feat = add_risk_features(df_feat)
    df_feat = add_eda_risk_bins(df_feat) # <-- NEU: Deine EDA-Erkenntnisse
    
    # Neue Spalten identifizieren
    new_features = [c for c in df_feat.columns if c not in old_cols]
    
    if print_status:
        print(f"Status: Enrichment Complete")
        print(f"Added Features ({len(new_features)}):")
        for feat in new_features:
            print(f"   [+] {feat}")
        print(f"Total Columns now: {df_feat.shape[1]}")
        print(f"{'='*55}\n")
    
    return df_feat


# --- 3. CLEANUP (Konsistent zu cleaning.py) ---

def prepare_for_model(df, cols_to_drop=None, print_status=True):
    """
    Finaler Filter für das Modell-Training. 
    Entfernt gezielt Spalten und prüft auf verbleibende Text-Daten.
    """
    df_model = df.copy()
    
    if print_status:
        print(f"{'='*55}")
        print(f" PREPARE FOR MODEL REPORT ")
        print(f"{'='*55}")

    if cols_to_drop is not None:
        # Tatsächlich vorhandene Spalten zum Droppen finden
        to_remove = [c for c in cols_to_drop if c in df_model.columns]
        df_model = df_model.drop(columns=to_remove, errors='ignore')
        if print_status:
            print(f"Action: Dropped {len(to_remove)} specific columns.")
            # Optional: Liste der gedroppten Spalten (gekürzt falls zu viele)
            if len(to_remove) > 0:
                print(f"Example Drops: {to_remove[:5]}...")
    else:
        if print_status:
            print("Action: No columns dropped (Safe Mode).")

    if print_status:
        # Check auf verbleibende 'nicht-Modell-taugliche' Spalten
        non_num = df_model.select_dtypes(include=['object', 'category']).columns.tolist()
        if non_num:
            print(f"\n⚠️ WARNING: {len(non_num)} non-numeric columns remaining!")
            print(f"   These might crash the model: {non_num[:10]}")
        else:
            print(f"\n✅ Success: All remaining columns are numeric.")
        
        print(f"Final Feature Count: {df_model.shape[1]}")
        print(f"{'='*55}\n")
        
    return df_model