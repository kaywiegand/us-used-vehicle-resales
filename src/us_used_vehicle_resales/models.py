import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
from sklearn.metrics import f1_score, recall_score, precision_score, roc_auc_score
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, f1_score, recall_score, precision_score
import matplotlib.pyplot as plt

# --- GLOBALE HELFER-FUNKTIONEN ---

def save_model(model, name, folder='../data/04_models/'):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.joblib")
    joblib.dump(model, path)
    print(f"💾 Modell-Datei erstellt: {path}")

# --- MODEL TRACKER KLASSE (SMART VERSION) ---


def inspect_run_full(run_id, X_val, y_val, tracker):
    """
    Lädt Modell ID, zeigt Hyperparameter, Features und Performance.
    """
    # 1. Daten aus Tracker laden
    df = tracker.get_results()
    run_info = df[df['Run_ID'].astype(str) == str(run_id)]
    
    if run_info.empty:
        print(f"❌ Run_ID {run_id} nicht gefunden!")
        return

    run_info = run_info.iloc[0]
    full_path = os.path.join(tracker.base_dir, run_info['Model_File'])
    
    if not os.path.exists(full_path):
        print(f"❌ Datei nicht gefunden: {full_path}")
        return

    # 2. Modell laden
    model = joblib.load(full_path)
    
    print("\n" + "═"*60)
    print(f"🔍 ANALYSE RUN_ID: {run_id} | Name: {run_info['Model']}")
    print("═"*60)

    # 3. SETTINGS AUS DER PIPELINE EXTRAHIEREN
    # Wir suchen den Classifier-Schritt (meist 'model')
    if hasattr(model, 'named_steps') and 'model' in model.named_steps:
        clf = model.named_steps['model']
        params = clf.get_params()
        
        print(f"⚙️  MODELL-EINSTELLUNGEN:")
        print(f"   • Typ:          {type(clf).__name__}")
        print(f"   • Penalty:      {params.get('penalty', 'N/A')}")
        print(f"   • Solver:       {params.get('solver', 'N/A')}")
        print(f"   • C (Regul.):   {params.get('C', 'N/A')}")
        print(f"   • Class Weight: {params.get('class_weight', 'N/A')}")
        print(f"   • Max Iter:     {params.get('max_iter', 'N/A')}")
    
    # 4. FEATURE-CHECK
    # Wir lesen aus dem Preprocessor, was er beim Training gesehen hat
    try:
        required_features = model.named_steps['pre'].feature_names_in_
        print(f"   • Features:     {len(required_features)} Spalten")
    except:
        print("   • Features:     (Konnte Namen nicht auslesen)")
        required_features = X_val.columns

    print("-" * 60)

    # 5. PERFORMANCE & MATRIX
    # Nur die Spalten nehmen, die das Modell kennt
    try:
        X_val_scoped = X_val[required_features].copy()
        y_pred = model.predict(X_val_scoped)
        
        print("📊 PERFORMANCE REPORT:")
        print(classification_report(y_val, y_pred, target_names=['Good (0)', 'Bad (1)']))

        cm = confusion_matrix(y_val, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Good', 'Bad'])
        disp.plot(cmap='Blues', values_format='d')
        plt.title(f"Confusion Matrix - Run {run_id}")
        plt.grid(False)
        plt.show()
        
    except KeyError as e:
        print(f"❌ Fehler: Im aktuellen X_val fehlen Spalten, die das Modell braucht: {e}")
    except Exception as e:
        print(f"❌ Ein Fehler ist aufgetreten: {e}")





class ModelTracker:
    def __init__(self, csv_path='../data/04_models/model_results_tracking.csv'):
        self.csv_path = csv_path
        self.base_dir = os.path.dirname(self.csv_path)
        self.export_dir = os.path.join(self.base_dir, 'export/')
        self.results = []
        
        for folder in [self.base_dir, self.export_dir]:
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

        if os.path.exists(self.csv_path):
            try:
                self.results = pd.read_csv(self.csv_path).to_dict('records')
            except:
                self.results = []

    def add_entry(self, model_name, model_obj, features_name, features_list, y_true, y_pred, y_proba=None, description=""):
        # 1. Metriken
        f1 = f1_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        auc = roc_auc_score(y_true, y_proba) if y_proba is not None else 0.0
        
        current_idx = len(self.results)
        
        # 2. Prüfen: Ist das ein neuer Bestwert?
        current_best_f1 = 0.0
        if self.results:
            current_best_f1 = max([r.get('F1-Score', 0) for r in self.results])
        
        is_best = f1 > current_best_f1
        is_worthy = f1 >= 0.30  # Deine magische Grenze
        
        # 3. Eintrag erstellen
        filename_short = f"{str(current_idx).zfill(3)}_{model_name}"
        # Wir merken uns in der CSV, ob ein File existiert
        file_saved = "No" 
        
        # 4. Nur speichern, wenn es sich lohnt (Smart Export)
        if is_best or is_worthy:
            filename_for_save = os.path.join("export", filename_short)
            save_model(model_obj, filename_for_save, folder=self.base_dir)
            file_saved = f"export/{filename_short}.joblib"
        
        entry = {
            'Run_ID': current_idx,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Model': model_name,
            'F1-Score': round(f1, 4),
            'Recall': round(rec, 4),
            'Precision': round(prec, 4),
            'ROC-AUC': round(auc, 4),
            'Model_File': file_saved,
            'Is_Best': is_best,
            'Description': description
        }
        
        self.results.append(entry)
        pd.DataFrame(self.results).to_csv(self.csv_path, index=False)
        
        # Feedback im Terminal
        status = "🏆 NEUER BESTWERT & GESPEICHERT" if is_best else ("✅ ÜBER 0.30 & GESPEICHERT" if is_worthy else "🔈 Nur CSV (F1 zu niedrig)")
        print(f"ID {current_idx}: F1={f1:.4f} -> {status}")
        
        return current_idx

    def get_results(self):
        return pd.DataFrame(self.results)