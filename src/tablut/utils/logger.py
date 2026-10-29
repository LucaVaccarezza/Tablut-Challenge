import logging
import os
import sys

_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%H:%M:%S"
_RESET = "\033[0m"
_COLORS = {
    logging.DEBUG: "\033[36m",  # cyan
    logging.INFO: "\033[32m",  # green
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",  # red
}


class _ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        text = super().format(record)
        color = _COLORS.get(record.levelno)
        return f"{color}{text}{_RESET}" if color else text


def _supports_color(stream: object) -> bool:
    return (
        "NO_COLOR" not in os.environ
        and hasattr(stream, "isatty")
        and bool(stream.isatty())
    )


class Logger:
    def __init__(self, name: str = "tablut", level: int | None = None) -> None:
        self._logger = logging.getLogger(name)
        self._logger.propagate = False
        # Same name returns the same logging.Logger; configure it only once.
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            formatter_cls = (
                _ColorFormatter
                if _supports_color(handler.stream)
                else logging.Formatter
            )
            handler.setFormatter(formatter_cls(_FORMAT, _DATE_FORMAT))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)
        if level is not None:
            self._logger.setLevel(level)

    def debug(self, msg: str, *args: object) -> None:
        self._logger.debug(msg, *args)

    def info(self, msg: str, *args: object) -> None:
        self._logger.info(msg, *args)

    def warning(self, msg: str, *args: object) -> None:
        self._logger.warning(msg, *args)

    def error(self, msg: str, *args: object) -> None:
        self._logger.error(msg, *args)
