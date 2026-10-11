import time
from fastapi import FastAPI, HTTPException, Request
from src.api.schemas import PatientClinicalInput
from src.models.predictor import OncoPredictor
from src.core.logger import logger

app = FastAPI(
    title="OncoBiomarker Precision API",
    description="Pipeline clínico de análisis genómico y predicción de biomarcadores oncológicos.",
    version="1.0.0"
)

# Inicializar el predictor
predictor = OncoPredictor()

# Middleware de Monitoreo de Rendimiento y Auditoría
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Procesar la petición
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"Path: {request.url.path} | Method: {request.method} | "
        f"Status: {response.status_code} | Duration: {process_time:.2f}ms"
    )
    return response

@app.get("/")
def health_check():
    logger.info("Health check endpoint solicitado.")
    return {"status": "online", "system": "OncoBiomarker Pipeline Active"}

@app.post("/api/v1/predict/")
def predict_patient_risk(data: PatientClinicalInput):
    try:
        logger.info(f"Procesando análisis clínico para el paciente: {data.patient_id} (Estadio: {data.tumor_stage})")
        
        # Ejecutar la predicción utilizando el modelo de ML
        result = predictor.predict(data.gene_expression_profile)
        
        logger.info(f"Predicción exitosa para {data.patient_id}: {result['clinical_interpretation']}")
        
        return {
            "patient_id": data.patient_id,
            "age": data.age,
            "tumor_stage": data.tumor_stage,
            "analysis_result": result
        }
    except Exception as e:
        logger.error(f"Error procesando paciente {data.patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))