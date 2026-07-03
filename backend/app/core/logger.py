import json
import logging
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Formats python log records into standardized JSON logs.
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
        }
        
        # Include dynamic extra attributes if supplied
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_data.update(record.extra)
            
        return json.dumps(log_data)

def get_structured_logger(name: str = "ai_assistant") -> logging.Logger:
    """
    Initializes and returns a structured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent handler duplication
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        
    # Prevent propagation to default root loggers to avoid duplicate unformatted printing
    logger.propagate = False
    
    return logger

# Global default logger
logger = get_structured_logger()
