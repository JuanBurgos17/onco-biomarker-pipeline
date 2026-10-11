from pydantic import BaseModel, Field, field_validator
from typing import Dict, List

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