import logging
from pathlib import Path


LOG_LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]
DATA_DIRECTORY = Path(__file__).parents[2] / "data"


def set_up_logging(verbosity: int) -> None:
    # Add handler with formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "{asctime} [{levelname}] {name} - {message}", style="{"
    )
    handler.setFormatter(formatter)

    # Add handler to root logger
    logger = logging.getLogger()
    logger.addHandler(handler)

    # Determine log level for root logger
    level = LOG_LEVELS[min(verbosity, len(LOG_LEVELS) - 1)]
    logger.setLevel(level)
