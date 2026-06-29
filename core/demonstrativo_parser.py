"""Parser for payment statement PDFs."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import pdfplumber

from .logger import ApplicationLogger
from .models import PaymentEntry
from .normalizer import normalize_name, normalize_procedure


class DemonstrativoParser:
    """Parser for Promédica payment statement PDFs."""

    def __init__(self, logger: Optional[ApplicationLogger] = None) -> None:
        """Initialize the parser.

        Args:
            logger: Application logger instance.
        """
        self.logger = logger or ApplicationLogger()

    def parse_file(self, pdf_path: Path) -> list[PaymentEntry]:
        """Parse a single payment statement PDF file.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of PaymentEntry objects.
        """
        entries: list[PaymentEntry] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_entries = self._parse_page(page, page_num)
                    entries.extend(page_entries)

            self.logger.info(
                f"Parsed {len(entries)} payment entries from {pdf_path.name}"
            )
        except Exception as e:
            self.logger.error(f"Error parsing {pdf_path.name}: {str(e)}")

        return entries

    def parse_directory(self, directory: Path) -> list[PaymentEntry]:
        """Parse all PDF files in a directory.

        Args:
            directory: Path to directory containing PDF files.

        Returns:
            List of all PaymentEntry objects found.
        """
        entries: list[PaymentEntry] = []
        pdf_files = list(directory.glob("*.pdf"))

        self.logger.info(f"Found {len(pdf_files)} PDF files in {directory}")

        for pdf_file in pdf_files:
            file_entries = self.parse_file(pdf_file)
            entries.extend(file_entries)

        return entries

    def _parse_page(self, page: pdfplumber.page.Page, page_num: int) -> list[PaymentEntry]:
        """Parse a single page from a payment statement PDF.

        Args:
            page: pdfplumber page object.
            page_num: Page number (0-indexed).

        Returns:
            List of PaymentEntry objects from this page.
        """
        entries: list[PaymentEntry] = []

        # This is a placeholder implementation.
        # In production, you would need to analyze the actual PDF structure
        # and extract the payment data based on the specific Promédica layout.

        try:
            # Extract tables if present
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        # Parse row data
                        pass
        except Exception as e:
            self.logger.warning(f"Could not parse page {page_num + 1}: {str(e)}")

        return entries
