from typing import Callable

import loguru
from loguru import logger

from ._constants import LOGS_DIR


class Filters:
    @staticmethod
    def level(level: str) -> Callable:
        def _wrap(record: 'loguru.Record') -> bool:
            return record['level'].name == level and not record['extra'].get('logger_name')

        return _wrap


format_ = "{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}"

logger.add(LOGS_DIR / 'success.log', format=format_, filter=Filters.level("SUCCESS"))
logger.add(LOGS_DIR / "errors.log", format=format_, filter=Filters.level("ERROR"))
