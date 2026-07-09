"""Smoke tests: the package and its public surface import cleanly."""


def test_package_imports():
    import us_used_vehicle_resales as wg

    assert hasattr(wg, "ModelTracker")


def test_project_modules_import():
    from us_used_vehicle_resales.cleaning import clean_data
    from us_used_vehicle_resales.features import engineer_features
    from us_used_vehicle_resales.config_features_catalog import features_catalog
    from us_used_vehicle_resales.config_models_catalog import models_catalog

    assert callable(clean_data)
    assert callable(engineer_features)
    assert "baseline" in features_catalog
    assert "log_reg_lasso" in models_catalog


def test_champion_feature_set_present():
    from us_used_vehicle_resales.config_features_catalog import features_catalog

    assert "all_in_with_noise" in features_catalog
