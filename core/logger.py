"""Logging system for the application."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class ApplicationLogger:
    """Centralized logging system."""

    def __init__(self, output_dir: Optional[Path] = None) -> None:
        """Initialize the logger.

        Args:
            output_dir: Directory for log files. If None, only console logging.
        """
        self.output_dir = output_dir
        self.logger = logging.getLogger("ConferenciaRecebimentos")
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # File handler (if output dir provided)
        self.file_handler: Optional[logging.FileHandler] = None
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            log_file = output_dir / "log.txt"
            self.file_handler = logging.FileHandler(log_file, encoding="utf-8")
            self.file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            self.file_handler.setFormatter(file_format)
            self.logger.addHandler(self.file_handler)

    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def close(self) -> None:
        """Close file handlers."""
        if self.file_handler:
            self.file_handler.close()
