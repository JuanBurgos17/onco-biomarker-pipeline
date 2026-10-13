import os
from pathlib import Path
import joblib
import numpy as np
import shap
from sklearn.ensemble import RandomForestClassifier


class OncoPredictor:

    def __init__(self, model_path: str = None):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        default_model_path = BASE_DIR / "models" / "onco_rf_model.pkl"

        self.model_path = Path(model_path) if model_path else default_model_path
        self.model = self._load_or_train_model()
        
        # Inicializar el TreeExplainer de SHAP optimizado para modelos de árboles (Random Forest)
        self.explainer = shap.TreeExplainer(self.model)

    def _load_or_train_model(self):
        """Carga el modelo si existe; si no, entrena un modelo base de ejemplo."""
        if self.model_path.exists():
            return joblib.load(self.model_path)

        np.random.seed(42)
        X_train = np.random.rand(100, 5)
        y_train = np.random.choice([0, 1], size=100)  # 0: Bajo Riesgo / 1: Alto Riesgo

        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)

        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, self.model_path)
        return model

    def predict(self, gene_expression: dict[str, float]) -> dict:
        """Recibe un diccionario de expresión génica, extrae los valores,
        realiza la predicción clínica y calcula los valores SHAP de explicabilidad.
        """
        target_genes = ["TP53", "BRCA1", "EGFR", "PTEN", "KRAS"]
        features_array = np.array(
            [[gene_expression.get(gene, 0.0) for gene in target_genes]]
        )

        prediction = self.model.predict(features_array)[0]
        probability = np.max(self.model.predict_proba(features_array))

        risk_label = (
            "Alto Riesgo / Patogénico" if prediction == 1 else "Bajo Riesgo / Estable"
        )

        # Calcular los valores SHAP locales para esta instancia
        # shap_values retorna un arreglo. Para clasificación binaria, extraemos la clase predicha o el valor de impacto.
        shap_values = self.explainer(features_array)
        
        # Obtenemos los valores SHAP para la predicción del paciente actual
        # En modelos binarios de scikit-learn con shap.TreeExplainer, shap_values.values tiene forma (1, n_features) o (1, n_features, n_classes)
        vals = shap_values.values
        if len(vals.shape) == 3:
            # Si tiene dimensión de clases, tomamos la clase predicha
            local_shap = vals[0, :, int(prediction)]
        else:
            local_shap = vals[0]

        # Mapear cada gen con su respectivo valor de impacto SHAP
        feature_contributions = {
            gene: round(float(shap_val), 4)
            for gene, shap_val in zip(target_genes, local_shap)
        }

        return {
            "prediction_class": int(prediction),
            "clinical_interpretation": risk_label,
            "confidence_score": round(float(probability), 4),
            "feature_contributions": feature_contributions,
        }