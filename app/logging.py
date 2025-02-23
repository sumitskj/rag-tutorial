import logging.config

# Logging Configuration
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        }
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "app.log",  # Logs will be saved in 'app.log'
        },
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "fastapi": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Apply logging configuration
logging.config.dictConfig(LOG_CONFIG)

# Create a logger instance
logger = logging.getLogger("fastapi")
