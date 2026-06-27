import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

class ModelTracker:
    def __init__(self):
        self.results = []
        self.models = {}
        self.features = {}

    def add_entry(self, model_name, model_obj, features_name, features_list, y_true, y_pred, description=""):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        # Speichere Metriken
        self.results.append({
            'Model': model_name,
            'Features Name': features_name,
            'Features Count': len(features_list),
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'Description': description
        })
        
        # Speichere Objekte für den Export
        self.models[model_name] = model_obj
        self.features[features_name] = features_list
        self.features[model_name] = features_list # Doppelt hält besser für den Export-Key

    def get_results(self):
        return pd.DataFrame(self.results)