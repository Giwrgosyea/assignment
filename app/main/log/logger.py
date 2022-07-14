import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, name, filename=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "(%(asctime)s) [%(levelname)s] %(name)s:%(funcName)s:%(message)s:line %(lineno)d"
        )

        if filename:
            handler = logging.handlers.RotatingFileHandler(
                "./logs/log_file.log", maxBytes=1024 * 1024 * 100, backupCount=20
            )
        else:
            handler = logging.StreamHandler()

        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.propagate = False

    def get_logger(self):
        return self.logger
