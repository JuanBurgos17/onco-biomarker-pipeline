from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional


class PatientClinicalInput(BaseModel):
    patient_id: str = Field(..., description="Identificador único del paciente (ej. TCGA-02-0001)")
    age: int = Field(..., ge=0, le=120, description="Edad del paciente en años")
    tumor_stage: str = Field(..., description="Estadio tumoral (ej. Stage I, Stage II, Stage III, Stage IV)")
    gene_expression_profile: Dict[str, float] = Field(
        ..., 
        description="Diccionario con perfiles de expresión génica normalizados (Gen: Valor TPM/FPKM)"
    )

    @field_validator('tumor_stage')
    @classmethod
    def validate_tumor_stage(cls, value: str) -> str:
        valid_stages = ["stage i", "stage ii", "stage iii", "stage iv", "unknown"]
        if value.lower() not in valid_stages:
            raise ValueError(f"Estadio tumoral inválido. Debe ser uno de: {valid_stages}")
        return value


# Esquema para peticiones por lotes utilizando la validación robusta
class BatchPredictionRequest(BaseModel):
    patients: List[PatientClinicalInput] = Field(..., description="Lista de pacientes para predicción en lote")


class PredictionResponse(BaseModel):
    patient_id: str
    predicted_risk_class: str
    confidence_score: float
    interpretation: str
    feature_contributions: Optional[Dict[str, float]] = Field(
        default=None,
        description="Impacto local de cada biomarcador/gen calculado mediante valores SHAP"
    )


# Esquema para la respuesta por lotes
class BatchPredictionResponse(BaseModel):
    total_processed: int
    predictions: List[PredictionResponse]