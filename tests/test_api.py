from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_check():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {
      "status": "online",
      "system": "OncoBiomarker Pipeline Active",
  }


def test_predict_endpoint_valid_data():
  payload = {
      "patient_id": "TCGA-02-0001",
      "age": 45,
      "tumor_stage": "Stage II",
      "gene_expression_profile": {
          "TP53": 2.5,
          "BRCA1": 1.1,
          "EGFR": 0.4,
          "PTEN": 1.8,
          "KRAS": 0.9,
      },
  }
  response = client.post("/api/v1/predict/", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["patient_id"] == "TCGA-02-0001"
  assert "analysis_result" in data
  assert "clinical_interpretation" in data["analysis_result"]


def test_predict_endpoint_invalid_stage():
  # Probando el validador estricto de Pydantic para un estadio tumoral no válido
  payload = {
      "patient_id": "TCGA-02-0002",
      "age": 50,
      "tumor_stage": "Stage V",  # Estadio inválido
      "gene_expression_profile": {"TP53": 1.0},
  }
  response = client.post("/api/v1/predict/", json=payload)
  assert response.status_code == 422  # Error de validación de Pydantic