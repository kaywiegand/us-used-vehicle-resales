import pandas as pd
import numpy as np
import wgnd as wg
import matplotlib.pyplot as plt
import seaborn as sns

from .printing import print_header, print_title, print_footer, print_seperator




def get_memory_usage(df):
    """Gibt den Speicherverbrauch in MB zurück."""
    return df.memory_usage(deep=True).sum() / 1024**2

def compare_memory(df_raw, df_new):
    """Druckt einen Vorher-Nachher-Vergleich des Speichers."""
    raw_mb = get_memory_usage(df_raw)
    new_mb = get_memory_usage(df_new)
    saving = raw_mb - new_mb

    print_title('Memory-Check')
    print(f"Raw: {raw_mb:.2f} MB")
    print(f"New {new_mb:.2f} MB")
    print(f"Saving: {saving:.2f} MB ({(saving/raw_mb)*100:.1f}%)")












# --- TEILFUNKTIONEN (MODULE) ---

def check_basic_meta(df, raw=None):
    """Prüft Dimensionen, Speicher und Duplikate."""
    num_duplicates = df.duplicated().sum()
    pct_duplicates = (num_duplicates / len(df) * 100).round(2)

    nans = df.isna().sum()

    print_title('Dimensions & Quality')

    print(f"Zeilen:      {df.shape[0]}")
    print(f"Spalten:     {df.shape[1]}")
    print(f"Duplikate:   {num_duplicates} ({pct_duplicates}%)")

    if nans.sum() > 0:
        print(f"Spalten NAs:\n{nans[nans > 0]}")
    else:
        print(f"Spalten NAs: keine ")
        
    todos = []
    if num_duplicates > 0:
        todos.append(("ACTION", f"{num_duplicates} Duplikate entfernen (df.drop_duplicates())"))
    return todos

def check_structure_na(df):
    """Analysiert Datentypen, Fehlwerte und Unique-Counts."""

    print_title('Structure & NaN-Values')

    info_df = pd.DataFrame({
        'Dtype': df.dtypes,
        'Nulls': df.isna().sum(),
        'Null %': (df.isna().sum() / len(df) * 100).round(2),
        'Unique': df.nunique()
    })
    print(info_df)
    
    todos = []
    high_na = info_df[info_df['Null %'] > 10].index.tolist()
    low_na = info_df[info_df['Nulls'] > 0].index.tolist()
    
    if low_na:
        todos.append(("CHECK", f"Fehlwerte in Spalten {low_na}. Imputation prüfen."))
         
    if high_na:
        todos.append(("CHECK", f"Hohe Fehlwerte (>10%) in Spalten {high_na}. Imputation prüfen."))
        
    return todos

def check_numeric_stats(df):
    """Berechnet Statistiken und identifiziert Ausreißer, Schiefe & Negativwerte."""
    num_cols = df.select_dtypes(include=[np.number]).columns
    todos = []
    
    if not num_cols.empty:
        print_title('Numerical Statistic')

        stats = df[num_cols].describe().round(2)
        display(stats)
        
        for col in num_cols:
            # 1. Check auf Negativwerte
            if df[col].min() < 0:
                todos.append(("CHECK", f"Negative Werte in '{col}' (Min: {df[col].min()}). Plausibilität prüfen!"))

            # 2. Ausreißer via IQR
            q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            iqr = q3 - q1
            outlier_count = ((df[col] < (q1 - 1.5 * iqr)) | (df[col] > (q3 + 1.5 * iqr))).sum()
            if outlier_count > 0:
                todos.append(("VISUALISIERUNG", f"Boxplot für '{col}' ({outlier_count} q1/q3 +/- 1.5)"))
            
            # 3. Schiefe (Skewness)
            if abs(df[col].mean() - df[col].median()) > df[col].std() * 0.5:
                todos.append(("VISUALISIERUNG", f"Histogramm für '{col}' (Starke Schiefe der Verteilung)"))
                
    return todos

def check_categorical_balance(df):
    """Prüft kategoriale Spalten auf Balance."""
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    todos = []
    
    for col in cat_cols:
        n_unique = df[col].nunique()
        if 1 < n_unique <= 15:
            todos.append(("VISUALISIERUNG", f"Countplot für '{col}' ({n_unique} Klassen prüfen)"))
    return todos

# --- HAUPTFUNKTION (ORCHESTRATOR) ---

def inspect_data(df, name="DataFrame", raw=None):
    """
    Ruft modulare Check-Funktionen auf und gibt gruppierte To-Dos aus.
    """
    print_header(f'Data Report: {name}')
    raw_todos = []

    # Module aufrufen
    raw_todos.extend(check_basic_meta(df,raw))

    if raw is not None:        
        compare_memory(raw, df)

    raw_todos.extend(check_structure_na(df))
    raw_todos.extend(check_numeric_stats(df))
    raw_todos.extend(check_categorical_balance(df))
     

    # Abschluss: Gruppierte To-Do Liste
    print_title('EDA ToDos')

    categories = ["ACTION", "CHECK", "VISUALISIERUNG"]
    found_any = False

    for cat in categories:
        # Filtert die Liste nach der jeweiligen Kategorie
        items = [content for label, content in raw_todos if label == cat]
        if items:
            found_any = True
            print(f"[{cat}S]")
            for item in items:
                print(f"  - {item}")
            print() # Leerzeile nach jeder Kategorie

    if not found_any:
        print("Keine sofortigen Maßnahmen oder Auffälligkeiten gefunden.")

    print_footer()


















def inspect_correlations(df, target=None, pairplot=True, threshold=0.4):
    """Gibt Spaltenpaare mit hoher Korrelation zurück."""

    wg.print_header('Check Correlations')

    
    if target != None:
        print_title('Ranking of correlations with target')
        corr = df.corr(numeric_only=True)
        display(corr[target].abs().sort_values(ascending=False))
        print()

    corr = df.corr(numeric_only=True).abs()
    # Nur die obere Dreiecksmatrix betrachten (um Dopplungen zu vermeiden)
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    
    high_corr = sorted([
        (column, row, upper.loc[row, column]) 
        for column in upper.columns 
        for row in upper.index 
        if upper.loc[row, column] > threshold
    ], key=lambda x: x[2], reverse=True)

    print()
    print_title(f"Starke Korrelationen (> {threshold}):")
    for col1, col2, val in high_corr:
        print(f"  {col1} <-> {col2}: {val:.2f}")

    print_footer()
    
    fig, ax = plt.subplots(figsize=(18,6))
    sns.heatmap(corr, annot=True)
    plt.show()
    print()

    if pairplot == True:
        print_title('Pairplot')
        sns.pairplot(df, diag_kind='kde', plot_kws={'alpha': 0.05})
        plt.show()
        print()






















# CHECK SPLIT CONSISTENCY 
#///////////////////////////////////////////////////

def inspect_split_consistency(y_full, y_train, y_test):
    """
    Vergleicht die statistische Verteilung der Zielvariablen 
    zwischen dem Originaldatensatz, dem Training- und dem Test-Set.
    
    Benötigt Pandas als pd 


    Anwendung:
    check_split_consistency(df_train['target'], y_train, y_test)
    """
    
    stats = {
        'Original': [y_full.mean(), y_full.median(), y_full.std(), y_full.max(), y_full.min()],
        'Train-Set': [y_train.mean(), y_train.median(), y_train.std(), y_train.max(), y_train.min()],
        'Test-Set': [y_test.mean(), y_test.median(), y_test.std(), y_test.max(), y_test.min()]
    }
    
    df_stats = pd.DataFrame(stats, index=['Mittelwert', 'Median', 'Std-Abw', 'Max', 'Min'])

    # Abweichung berechnen: (Test - Train) / Train * 100
    df_stats['Abweichung Train/Test %'] = ((df_stats['Test-Set'] - df_stats['Train-Set']) / df_stats['Train-Set'] * 100)
    
    display(df_stats.round(2))
    #print(df_stats.round(2).to_string())
    
    print_seperator()

    print_title('Schiefe')

    #Visualisierung der Verteilung
    plt.figure(figsize=(12, 5))
    sns.kdeplot(y_train, label='Train-Set', fill=True, alpha=0.3, color='blue')
    sns.kdeplot(y_test, label='Test-Set', fill=True, alpha=0.3, color='orange')
    plt.title('Verteilungs-Check: Train vs. Test (Target)')
    plt.xlabel('wait_sec')
    plt.legend()
    plt.show()
    
    if y_train.mean() > y_train.median():
        print("\nNote: Die Verteilung im Training-Set ist rechtsschief (Mean > Median).")
    else:
        print("\nNote: Die Verteilung im Training-Set ist annähernd symmetrisch oder linksschief.")
    print_seperator()



    

    

    



#///////////////////////////////////////////////////
