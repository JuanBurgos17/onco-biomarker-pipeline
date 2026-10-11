# OncoBiomarker Precision API 🧬🔬

> Pipeline clínico automatizado para el análisis de perfiles de expresión génica y predicción de riesgo oncológico mediante Machine Learning, desarrollado bajo principios de arquitectura limpia, validación estricta de datos y contenedores Docker.

---

## 🚀 Descripción del Proyecto
Este proyecto simula un entorno de producción en bioinformática clínica y medicina de precisión. Su objetivo es recibir datos clínicos y perfiles de expresión de secuenciación (RNA-seq), validar estrictamente los esquemas de entrada, ejecutar inferencias mediante modelos de Machine Learning (Random Forest) y registrar trazas de auditoría y métricas de rendimiento para la toma de decisiones clínicas.

---

## Stack Tecnológico
* **Lenguaje:** Python 3.10
* **Framework Backend:** FastAPI (Arquitectura RESTful con validación por Pydantic)
* **Machine Learning & Ciencia de Datos:** Scikit-Learn, NumPy, Pandas, Joblib
* **Pruebas Automatizadas:** Pytest, Httpx (TestClient)
* **Contenedorización:** Docker
* **Monitoreo y Auditoría:** Logging estructurado y middleware de observabilidad

---

## Repositorio
El proyecto sigue una estructura modular y limpia para facilitar la escalabilidad y el mantenimiento:

```text
proyecto_bionco/
├── .github/workflows/      # Automatización CI/CD (GitHub Actions) poximamente
├── models/                 # Modelos entrenados serializados (.pkl)
├── src/                    # Código fuente principal del sistema
│   ├── api/                # Endpoints FastAPI y esquemas de Pydantic
│   ├── core/               # Configuración global y sistema de logging
│   ├── models/             # Capa de Machine Learning (Predictor)
│   └── utils/              # Funciones auxiliares y utilidades reutilizables
├── tests/                  # Pruebas automatizadas (pytest)
├── .dockerignore           # Exclusiones para la imagen de Docker
├── Dockerfile              # Configuración de contenedorización
├── pytest.ini              # Configuración del entorno de pruebas
├── requirements.txt        # Dependencias fijadas por versiones
└── README.md               # Documentación técnica del proyecto