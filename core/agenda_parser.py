"""Parser for medical agenda PDFs."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import pdfplumber

from .logger import ApplicationLogger
from .models import AgendaEntry, BoundingBox
from .normalizer import normalize_name, normalize_procedure


class AgendaParser:
    """Parser for Promédica agenda PDFs."""

    def __init__(self, logger: Optional[ApplicationLogger] = None) -> None:
        """Initialize the parser.

        Args:
            logger: Application logger instance.
        """
        self.logger = logger or ApplicationLogger()

    def parse_file(self, pdf_path: Path) -> list[AgendaEntry]:
        """Parse a single agenda PDF file.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of AgendaEntry objects.
        """
        entries: list[AgendaEntry] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_entries = self._parse_page(page, page_num, pdf_path.name)
                    entries.extend(page_entries)

            self.logger.info(
                f"Parsed {len(entries)} entries from {pdf_path.name}"
            )
        except Exception as e:
            self.logger.error(f"Error parsing {pdf_path.name}: {str(e)}")

        return entries

    def parse_directory(self, directory: Path) -> list[AgendaEntry]:
        """Parse all PDF files in a directory.

        Args:
            directory: Path to directory containing PDF files.

        Returns:
            List of all AgendaEntry objects found.
        """
        entries: list[AgendaEntry] = []
        pdf_files = list(directory.glob("*.pdf"))

        self.logger.info(f"Found {len(pdf_files)} PDF files in {directory}")

        for pdf_file in pdf_files:
            file_entries = self.parse_file(pdf_file)
            entries.extend(file_entries)

        return entries

    def _parse_page(
        self, page: pdfplumber.page.Page, page_num: int, filename: str
    ) -> list[AgendaEntry]:
        """Parse a single page from a PDF.

        Args:
            page: pdfplumber page object.
            page_num: Page number (0-indexed).
            filename: Source PDF filename.

        Returns:
            List of AgendaEntry objects from this page.
        """
        entries: list[AgendaEntry] = []

        # This is a placeholder implementation.
        # In production, you would need to analyze the actual PDF structure
        # and extract the table/text data based on the specific Promédica layout.
        #
        # For now, we demonstrate the structure:
        # - Extract text with bounding boxes
        # - Parse dates, times, patient names, procedures
        # - Create AgendaEntry objects

        try:
            # Extract tables if present
            tables = page.extract_tables()
            if not tables:
                text_dict = page.extract_text_dict()
                # Parse text-based layout
                pass
            else:
                # Parse table-based layout
                for table in tables:
                    for row in table:
                        # Parse row data
                        pass
        except Exception as e:
            self.logger.warning(f"Could not parse page {page_num + 1}: {str(e)}")

        return entries
