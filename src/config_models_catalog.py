from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier

# Name ohne 's' am Ende für den Import im Notebook
models_catalog = {
    
    # --- LOGISTISCHE REGRESSION (Ridge / L2) ---
    "log_reg_balanced": LogisticRegression(
        max_iter=5000, 
        class_weight='balanced', 
        penalty='elasticnet', 
        solver='saga', 
        l1_ratio=0,           # 0 steht für reines L2
        random_state=42
    ),
    
    # --- LOGISTISCHE REGRESSION (Lasso / L1) ---
    "log_reg_lasso": LogisticRegression(
        max_iter=5000, 
        class_weight='balanced', 
        penalty='elasticnet', 
        solver='saga', 
        l1_ratio=1,           # 1 steht für reines L1
        C=0.1, 
        random_state=42
    ),

    # --- RANDOM FOREST VARIANTEN ---
    "rf_shallow": RandomForestClassifier(
        n_estimators=100, 
        max_depth=7, 
        class_weight='balanced', 
        random_state=42
    ),
    
    "rf_deep": RandomForestClassifier(
        n_estimators=200, 
        max_depth=15, 
        min_samples_leaf=5, 
        class_weight='balanced', 
        random_state=42
    ),

    # --- GRADIENT BOOSTING VARIANTEN ---
    "hist_boost_std": HistGradientBoostingClassifier(
        max_iter=100, 
        learning_rate=0.1, 
        max_depth=5,
        class_weight='balanced',
        random_state=42
    ),
    
    "hist_boost_aggressive": HistGradientBoostingClassifier(
        max_iter=300, 
        learning_rate=0.05, 
        max_depth=10,
        l2_regularization=1.0, 
        class_weight='balanced',
        random_state=42
    )
}




log_reg_models_catalog_01 = {
    # 1. RIDGE (L2) - Der Allrounder
    "log_reg_ridge": LogisticRegression(
        max_iter=5000, class_weight='balanced', solver='saga', 
        penalty='elasticnet', l1_ratio=0, C=0.1, random_state=42
    ),
    
    # 2. LASSO (L1) - Der Feature-Killer (Dein aktueller Champion)
    "log_reg_lasso_strong": LogisticRegression(
        max_iter=5000, class_weight='balanced', solver='saga', 
        penalty='elasticnet', l1_ratio=1, C=0.1, random_state=42
    ),

    # 3. LASSO (L1) - Etwas lockerer (Lässt mehr Features zu)
    "log_reg_lasso_mild": LogisticRegression(
        max_iter=5000, class_weight='balanced', solver='saga', 
        penalty='elasticnet', l1_ratio=1, C=1.0, random_state=42
    ),
    
    # 4. ELASTIC NET - Der Kompromiss
    "log_reg_elastic": LogisticRegression(
        max_iter=5000, class_weight='balanced', solver='saga', 
        penalty='elasticnet', l1_ratio=0.5, C=0.1, random_state=42
    ),

    # 5. PRECISION-BOOSTER (Manuelles Gewicht statt 'balanced')
    # Ziel: Weniger Fehlalarme, dafür etwas weniger Recall
    "log_reg_precision_focus": LogisticRegression(
        max_iter=5000, class_weight={0: 1, 1: 4}, solver='saga', 
        penalty='elasticnet', l1_ratio=1, C=0.1, random_state=42
    )
}

log_reg_models_catalog = {
    
    "log_reg_rige": LogisticRegression(
        max_iter=5000, 
        class_weight='balanced', 
        solver='saga', 
        l1_ratio=0,       
        C=0.1, 
        random_state=42
    ),
    
    "log_reg_lasso": LogisticRegression(
        max_iter=5000, 
        class_weight='balanced', 
        solver='saga', 
        l1_ratio=1,           
        C=0.1, 
        random_state=42
    ),
    
    "log_reg_elastic": LogisticRegression(
        max_iter=5000, 
        class_weight='balanced', 
        solver='saga', 
        l1_ratio=0.5,           
        C=0.1, 
        random_state=42
    ),
}

