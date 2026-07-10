"""
Projekt-spezifische Modell-Utilities für us-used-vehicle-resales.

``ModelTracker`` und ``save_model`` sind ins gemeinsame Toolkit gewandert
(2026-07, siehe ``from wgnd import ModelTracker, save_model`` im Paket-__init__).
Hier bleibt nur ``inspect_run_full`` — es ist bewusst projekt-spezifisch
(Logistic-Regression-Settings, Labels ``Good/Bad``, IsBadBuy-Kontext) und
gehört daher nicht ins allgemeine Toolkit.
"""

import os

import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    confusion_matrix,
)


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
    except Exception:
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
