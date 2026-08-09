from .config import LOG_FILE
import logging


def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        format = logging.Formatter(
            fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt = "%Y-%m-%d %H:%M:%S"
        )

        file_h = logging.FileHandler(
            filename = LOG_FILE,
            encoding = "utf-8"
        )
        file_h.setFormatter(format)

        # file_s = logging.StreamHandler()
        # file_s.setFormatter(format)

        logger.addHandler(file_h)
        # logger.addHandler(file_s)

        logger.propagate = False

    return logger


