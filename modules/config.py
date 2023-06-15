import logging
import logging.handlers
from logging.handlers import RotatingFileHandler

from logging import Logger, Formatter, StreamHandler


class FetchDataError(Exception):
    pass


def set_logger() -> Logger:
    logger: Logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    logging.getLogger("discord.http").setLevel(logging.INFO)

    dt_fmt: str = "%Y-%m-%d %H:%M:%S"
    formatter: Formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )

    file_handler: RotatingFileHandler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=8 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)

    console_handler: StreamHandler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
