import logging
import os


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.INFO, logging.WARNING)


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR


def get_logger(name: str) -> logging.Logger:

    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        info_handler = logging.FileHandler(os.path.join(logs_dir, "info.log"))
        info_handler.setLevel(logging.INFO)
        info_handler.addFilter(InfoFilter())
        info_handler.setFormatter(formatter)

        error_handler = logging.FileHandler(os.path.join(logs_dir, "errors.log"))
        error_handler.setLevel(logging.ERROR)
        error_handler.addFilter(ErrorFilter())
        error_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        logger.addHandler(info_handler)
        logger.addHandler(error_handler)
        logger.addHandler(console_handler)

    return logger