import numpy as np

def apply_sampling(X, y, threshold=3.0):
    """
    Entfernt extreme Ausreißer aus dem Trainingsset basierend auf dem Target (wait_sec).
    Nutzt MAD für robuste Erkennung.
    """
    # 1. Sicherstellen, dass y nur die Zeilen hat, die auch in X sind
    y_sync = y.loc[X.index]
    
    # 2. MAD Berechnung auf synchronisiertem y
    median_y = np.median(y_sync)
    mad_y = np.median(np.abs(y_sync - median_y))
    
    # Falls mad_y 0 ist (passiert bei sehr vielen identischen Werten), 
    # setzen wir einen minimalen Wert, um Division durch Null zu vermeiden
    if mad_y == 0: mad_y = 1e-6
    
    modified_z_scores = 0.6745 * (y_sync - median_y) / mad_y
    mask = np.abs(modified_z_scores) <= threshold
    
    # 3. Rückgabe der gefilterten Daten
    X_filtered = X[mask]
    y_filtered = y_sync[mask]
    
    print(f"🌲 Sampling: {len(y_sync) - len(y_filtered)} Ausreißer entfernt.")
    return X_filtered, y_filtered