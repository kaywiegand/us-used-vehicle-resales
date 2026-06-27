import os
import json
import joblib

def run_export(tracker, export_path, run_name):
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    results_df = tracker.get_results().sort_values(by='MAE')
    results_df.to_csv(f"{export_path}/summary_{run_name}.csv", index=False)
    
    # Top 3 Modelle sichern
    top_3 = results_df.head(3)
    for rank, (idx, row) in enumerate(top_3.iterrows(), 1):
        m_full_name = row['Model']
        f_cat_name = row['Features Name']
        
        joblib.dump(tracker.models[m_full_name], f"{export_path}/Rank{rank}_{m_full_name}.pkl")
        
        # Features holen (entweder via Cat-Name oder Modell-Name)
        feat_list = tracker.features.get(f_cat_name, tracker.features.get(m_full_name, []))
        with open(f"{export_path}/Rank{rank}_{m_full_name}_features.json", 'w') as f:
            json.dump(feat_list, f)

    joblib.dump(tracker, f"{export_path}/full_tracker_state.pkl")
    print(f"✅ Export in '{export_path}' abgeschlossen.")