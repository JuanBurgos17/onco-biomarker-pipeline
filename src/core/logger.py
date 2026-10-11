import logging
import sys

def setup_logging():
    """Configura un formato de logging limpio y estructurado para producción."""
    logger = logging.getLogger("OncoBiomarkerPipeline")
    logger.setLevel(logging.INFO)
    
    # Evitar duplicidad de handlers si ya están configurados
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logging()