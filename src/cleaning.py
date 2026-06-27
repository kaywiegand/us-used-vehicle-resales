import pandas as pd
import numpy as np

# =============================================================================
# --- 1. INTEGRITY CHECKS (Diagnose-Masken) ---
# =============================================================================

def get_integrity_masks(df):
    """
    Erstellt Plausibilitäts-Masken basierend auf harten Logik-Fehlern.
    Korrektur: Wir prüfen auf < 100$, um Dummy-Werte (wie 1.0$) zu fangen.
    """
    masks = {}

    # 1. Kosten-Check: Alles unter 100$ ist ein Datensatz-Fehler oder Dummy
    masks['mask_invalid_low_cost'] = (df['VehBCost'] < 100) | df['VehBCost'].isna()

    # 2. MMR-Check: Auch Auktions-Marktpreise unter 100$ sind unplausibel
    if 'MMRCurrentAuctionAveragePrice' in df.columns:
        masks['mask_invalid_relation_cost'] = (df['MMRCurrentAuctionAveragePrice'] < 100) | df['MMRCurrentAuctionAveragePrice'].isna()
    else:
        masks['mask_invalid_relation_cost'] = pd.Series(False, index=df.index)

    # 3. Alters-Check: Negatives Alter ist unmöglich (0.0 ist aber okay für Neuwagen)
    masks['mask_invalid_age'] = df['VehicleAge'] < 0

    # 4. Kilometerstand: Unter 10 Meilen deutet auf Erfassungsfehler hin
    masks['mask_invalid_odo'] = df['VehOdo'] <= 10 

    # 5. Konsistenz: Ohne Marke/Modell fehlt die Basis für jedes Feature
    masks['mask_inconsistent_unit'] = df['Model'].isna() | df['Make'].isna()

    return masks


# =============================================================================
# --- 2. COMPLETENESS & IMPUTATION (Heilung) ---
# =============================================================================

def impute_prices_hierarchical(df):
    """
    HIERARCHISCHE MEDIAN-IMPUTATION (PREIS-RETTUNG)
    LOGIK: Fehlende/unplausible Preise (< 100$) werden durch Gruppen-Mediane ersetzt.
    Stufe 1: [Model, VehYear] -> Exakter Vergleich
    Stufe 2: [Make, VehYear]  -> Marken-Vergleich
    Stufe 3: [VehicleAge]     -> Alters-Vergleich (starker Preistreiber)
    Stufe 4: [VehYear]        -> Jahres-Vergleich (letzter Rettungsanker)
    """
    df_impute = df.copy()
    price_cols = [col for col in df_impute.columns if 'MMR' in col] + ['VehBCost']
    
    # WICHTIG: Alles unter 100$ als NaN markieren, damit die Stufen es überschreiben
    for col in price_cols:
        if col in df_impute.columns:
            df_impute[col] = df_impute[col].where(df_impute[col] >= 100, np.nan)

    levels = [['Model', 'VehYear'], ['Make', 'VehYear'], ['VehicleAge'], ['VehYear']]

    for group_cols in levels:
        for col in price_cols:
            if col in df_impute.columns:
                mask = df_impute[col].isna()
                if mask.any():
                    # Median innerhalb der aktuellen Hierarchie-Stufe berechnen
                    group_medians = df_impute.groupby(group_cols, observed=False)[col].transform('median')
                    df_impute.loc[mask, col] = group_medians[mask]
    return df_impute

def handle_eda_completeness(df):
    """Füllt alle kategorialen Lücken dynamisch mit 'Unknown'."""
    df_temp = df.copy()
    cat_cols = df_temp.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        if df_temp[col].isna().any():
            if df_temp[col].dtype.name == 'category':
                if 'Unknown' not in df_temp[col].cat.categories:
                    df_temp[col] = df_temp[col].cat.add_categories(['Unknown'])
            df_temp[col] = df_temp[col].fillna('Unknown')
    return df_temp


# =============================================================================
# --- 3. ORCHESTRATOR ---
# =============================================================================

def clean_data(df, cols_to_drop=None):
    df_clean = df.copy()
    
    # --- DIAGNOSE ---
    cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns
    initial_cat_nans = df_clean[cat_cols].isna().sum().sum()
    initial_masks = get_integrity_masks(df_clean)
    
    detected_logical_issues = (
        initial_masks['mask_invalid_low_cost'].sum() + 
        initial_masks['mask_invalid_relation_cost'].sum() + 
        initial_masks['mask_invalid_age'].sum() + 
        initial_masks['mask_invalid_odo'].sum()
    )

    # --- KAPITEL 1: COMPLETENESS ---
    df_clean = handle_eda_completeness(df_clean)
    
    # --- KAPITEL 2: INTEGRITY (Heilung) ---
    df_clean = impute_prices_hierarchical(df_clean)
    
    # --- KONTROLLE & REINIGUNG ---
    final_masks = get_integrity_masks(df_clean)
    unfixable_issues = (
        final_masks['mask_invalid_low_cost'] | final_masks['mask_invalid_relation_cost'] | 
        final_masks['mask_invalid_age'] | final_masks['mask_invalid_odo'] | 
        final_masks['mask_inconsistent_unit']
    ).sum()
    
    repaired_logical = detected_logical_issues - unfixable_issues
    df_clean = df_clean[~ (final_masks['mask_invalid_low_cost'] | final_masks['mask_invalid_relation_cost'] | 
                          final_masks['mask_invalid_age'] | final_masks['mask_invalid_odo'] | 
                          final_masks['mask_inconsistent_unit'])].copy()
    
    cnt_before_dups = df_clean.shape[0]
    df_clean = df_clean.drop_duplicates()
    cnt_dupes = cnt_before_dups - df_clean.shape[0]

    if cols_to_drop is not None:
        df_clean = df_clean.drop(columns=cols_to_drop, errors='ignore')

    # --- SUCCESS REPORT ---
    print(f"{'='*55}")
    print(f" DATA CLEANING & SUCCESS REPORT ")
    print(f"{'='*55}")
    print(f"KAPITEL 1: COMPLETENESS\n  - Erkannt: {initial_cat_nans:>6} kategoriale Lücken\n  - Aktion:  {initial_cat_nans:>6} gefüllt mit 'Unknown'")
    print(f"\nKAPITEL 2: INTEGRITY\n  - Erkannt: {detected_logical_issues:>6} Logik-Fehler (< 100$, Alter, Odo)")
    print(f"  - Aktion:  {repaired_logical:>6} geheilt via Imputation\n  - Aktion:  {unfixable_issues:>6} unrettbar gelöscht")
    
    cnt_raw, cnt_new = df.shape[0], df_clean.shape[0]
    retention, churn = (cnt_new/cnt_raw)*100, 100-(cnt_new/cnt_raw)*100
    print(f"-------------------------------------------------------\nENDERGEBNIS:\n  - Datensätze (Rows): {cnt_new:>6}\n  - Retention Rate:   {retention:>7.2f}%\n  - Churn Rate:       {churn:>7.2f}%\n{'='*55}\n")
    
    return df_clean