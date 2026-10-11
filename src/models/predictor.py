import os
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class OncoPredictor:

  def __init__(self, model_path: str = None):
    # Definimos la ruta base del proyecto de manera absoluta usando pathlib
    # Esto evita problemas de rutas relativas dependiendo de dónde se ejecute uvicorn
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    default_model_path = BASE_DIR / "models" / "onco_rf_model.pkl"

    self.model_path = Path(model_path) if model_path else default_model_path
    self.model = self._load_or_train_model()

  def _load_or_train_model(self):
    """Carga el modelo si existe; si no, entrena un modelo base de ejemplo."""
    if self.model_path.exists():
      return joblib.load(self.model_path)

    # Generar un modelo sintético de entrenamiento inicial para demostración
    # Simulamos perfiles de expresión de 5 genes clave en oncología (TP53, BRCA1, EGFR, PTEN, KRAS)
    np.random.seed(42)
    X_train = np.random.rand(100, 5)
    y_train = np.random.choice([0, 1], size=100)  # 0: Bajo Riesgo / 1: Alto Riesgo

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Asegurar que el directorio de modelos exista antes de guardarlo
    self.model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, self.model_path)
    return model

  def predict(self, gene_expression: dict[str, float]) -> dict:
    """Recibe un diccionario de expresión génica, extrae los valores

    y realiza la predicción clínica.
    """
    target_genes = ["TP53", "BRCA1", "EGFR", "PTEN", "KRAS"]
    features = np.array(
        [[gene_expression.get(gene, 0.0) for gene in target_genes]]
    )

    prediction = self.model.predict(features)[0]
    probability = np.max(self.model.predict_proba(features))

    risk_label = (
        "Alto Riesgo / Patogénico" if prediction == 1 else "Bajo Riesgo / Estable"
    )

    return {
        "prediction_class": int(prediction),
        "clinical_interpretation": risk_label,
        "confidence_score": round(float(probability), 4),
    }