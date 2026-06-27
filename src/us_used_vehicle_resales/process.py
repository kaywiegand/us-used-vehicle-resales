from sklearn.model_selection import train_test_split
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from .inspect import inspect_classification_split_consistency, inspect_continuous_split_consistency
from .printing import print_header, print_title, print_footer, print_seperator

def continuous_split_train_test(df_train, TARGET): 
    print_header('Continuous Data Train Test Split (Regression)')
    
    # Target Inspection
    print_title(f'Target Curve: {TARGET}')
    sns.histplot(df_train[TARGET], bins=50, kde=True, color='royalblue')
    plt.title(f'Verteilung von {TARGET}')
    plt.show()
    
    # Split ohne Stratify
    features = df_train.drop(columns=[TARGET])
    target = df_train[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    
    print_title('Split Shapes')
    print(f"Train {X_train.shape} | Test {X_test.shape}")

    inspect_continuous_split_consistency(df_train[TARGET], y_train, y_test)


    return X_train, X_test, y_train, y_test


def classification_split_train_test(df_train, TARGET): 
    print_header('Classification Data Train Test Split (Stratified)')
    
    # Target Inspection: Countplot statt Histplot
    print_title(f'Class Distribution: {TARGET}')
    sns.countplot(x=df_train[TARGET], data=df_train, hue='IsBadBuy', palette='viridis', legend=False)

    plt.title(f'Häufigkeit der Klassen in {TARGET}')
    plt.show()
    
    # Split MIT Stratify
    features = df_train.drop(columns=[TARGET])
    target = df_train[TARGET]
    
    X_train, X_test, y_train, y_test = train_test_split(
        features, 
        target, 
        test_size=0.2, 
        random_state=42,
        stratify=target 
    )
    
    print_title('Split Shapes & Class Balance')
    print(f"Train {X_train.shape} | Test {X_test.shape}")
    print(f"BadBuy Rate Train: {y_train.mean():.2%}")
    print(f"BadBuy Rate Test:  {y_test.mean():.2%}")
    print_seperator()
    
    inspect_classification_split_consistency(df_train[TARGET], y_train, y_test)

    return X_train, X_test, y_train, y_test


def save_split_data(features_train, features_test, target_train, target_test, folder='../data/'):
    """
    Speichert die vier Split-Objekte als Parquet-Dateien ab.
    Konvertiert Targets (Series) automatisch in DataFrames für Parquet-Kompatibilität.
    """
    # Ordner erstellen, falls er nicht existiert
    output_dir = Path(folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    print_title('Export to parquet')


    # Mapping für die Dateien
    data_map = {
        'features_train.parquet': features_train,
        'features_test.parquet': features_test,
        'target_train.parquet': target_train.to_frame() if isinstance(target_train, pd.Series) else target_train,
        'target_test.parquet': target_test.to_frame() if isinstance(target_test, pd.Series) else target_test
    }
    
    for filename, data in data_map.items():
        file_path = output_dir / filename
        data.to_parquet(file_path, index=True) # Index mitspeichern (wichtig für 'id')
        print(f"File:'{file_path}'")

    print("---")
    print(f"Split-Daten erfolgreich in '{folder}' gespeichert.")
    print_seperator()



def load_split_data(folder='../data/'):
    """
    Lädt die vier Parquet-Dateien und gibt sie in der richtigen Reihenfolge zurück.
    Konvertiert die Targets zurück in Pandas Series.
    """
    input_dir = Path(folder)
    
    ft_train = pd.read_parquet(input_dir / 'features_train.parquet')
    ft_test  = pd.read_parquet(input_dir / 'features_test.parquet')
    tg_train = pd.read_parquet(input_dir / 'target_train.parquet').iloc[:,0]
    tg_test  = pd.read_parquet(input_dir / 'target_test.parquet').iloc[:,0]
    
    print(f"🚀 Daten aus '{folder}' geladen.\n\nShapes: \nTrain {ft_train.shape} \nTest {ft_test.shape}")
    return ft_train, ft_test, tg_train, tg_test



def save_processed_data(df_x, df_y=None, folder='../data/03_processed/', name='train'):
    """
    Sichert aufbereitete Daten im Parquet-Format. 
    df_y ist optional (wichtig für AIM/Test-Daten ohne Labels).
    """
    import os
    import pandas as pd

    # Verzeichnis erstellen falls nötig
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Ordner '{folder}' wurde erstellt.")

    # Pfad für X (immer vorhanden)
    x_path = os.path.join(folder, f'X_{name}_final.parquet')
    df_x.to_parquet(x_path)
    
    y_status = "Nicht vorhanden"
    
    # Speichern von y nur, wenn df_y übergeben wurde
    if df_y is not None:
        y_path = os.path.join(folder, f'y_{name}.parquet')
        if isinstance(df_y, pd.Series):
            df_y.to_frame().to_parquet(y_path)
        else:
            df_y.to_parquet(y_path)
        y_status = f"Gespeichert ({df_y.shape[0]} Zeilen)"

    # Abschluss-Report
    print(f"{'~'*40}")
    print(f"PROCESSED {name.upper()} DATA EXPORT")
    print(f"{'~'*40}")
    print(f"🚀 X-Features: {df_x.shape[0]} rows | {df_x.shape[1]} cols")
    print(f"🎯 y-Labels:   {y_status}")
    print(f"📂 Location:   {folder}")
    print(f"{'~'*40}")