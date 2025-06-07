import logging
import sys
import os
import json
from logging import Formatter


class CustomJsonFormatter(Formatter):
    def format(self, record):
        json_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "message": record.getMessage(),
            "level": record.levelname,
        }

        optional_fields = ["duration_ms", "request_id", "req", "res", "error"]

        for field in optional_fields:
            value = record.__dict__.get(field)
            if value is not None:
                json_record[field] = value

        if record.levelno == logging.ERROR and record.exc_info:
            json_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(json_record)


def _init_logger():
    logger = logging.getLogger()
    logger.propagate = False

    # Set log level from env
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomJsonFormatter())
    logger.handlers = [handler]

    # Disable Uvicorn access log
    logging.getLogger("uvicorn.access").disabled = True

    return logger


logger = _init_logger()
