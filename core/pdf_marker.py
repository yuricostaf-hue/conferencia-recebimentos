"""PDF marking utilities for drawing strike-through lines."""

from pathlib import Path
from typing import Optional

import fitz

from .logger import ApplicationLogger
from .models import AgendaEntry, MatchResult


class PDFMarker:
    """Marks paid procedures in agenda PDFs."""

    # Line color for marking (RGB tuple)
    MARK_COLOR = (0, 0, 0)  # Black
    MARK_WIDTH = 2  # Line width

    def __init__(self, logger: Optional[ApplicationLogger] = None) -> None:
        """Initialize the marker.

        Args:
            logger: Application logger instance.
        """
        self.logger = logger or ApplicationLogger()

    def mark_pdf(
        self,
        input_path: Path,
        output_path: Path,
        match_results: list[MatchResult],
    ) -> bool:
        """Mark paid procedures in a PDF.

        Args:
            input_path: Path to original PDF.
            output_path: Path for marked PDF.
            match_results: List of match results to mark.

        Returns:
            True if successful, False otherwise.
        """
        try:
            doc = fitz.open(input_path)

            # Group results by file and page
            marks_by_page: dict[int, list[MatchResult]] = {}
            for result in match_results:
                if result.is_paid and result.agenda_entry.arquivo == input_path.name:
                    page_num = result.agenda_entry.pagina - 1  # Convert to 0-indexed
                    if page_num not in marks_by_page:
                        marks_by_page[page_num] = []
                    marks_by_page[page_num].append(result)

            # Mark each page
            for page_num, results in marks_by_page.items():
                if page_num < len(doc):
                    page = doc[page_num]
                    self._mark_page(page, results)

            # Save marked PDF
            output_path.parent.mkdir(parents=True, exist_ok=True)
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()

            self.logger.info(f"Marked PDF saved: {output_path.name}")
            return True

        except Exception as e:
            self.logger.error(f"Error marking PDF {input_path.name}: {str(e)}")
            return False

    def _mark_page(self, page: fitz.Page, results: list[MatchResult]) -> None:
        """Draw strike-through lines on a page.

        Args:
            page: PDF page.
            results: Match results to mark.
        """
        for result in results:
            bbox = result.agenda_entry.bbox
            # Convert coordinates to fitz.Rect
            # Note: PDF coordinates have origin at bottom-left
            page_height = page.rect.height
            rect = fitz.Rect(
                bbox.x0,
                page_height - bbox.y1,
                bbox.x1,
                page_height - bbox.y0,
            )

            # Draw a line through the text (horizontal strike-through)
            midpoint_y = (rect.y0 + rect.y1) / 2
            line = (
                fitz.Point(rect.x0, midpoint_y),
                fitz.Point(rect.x1, midpoint_y),
            )
            page.draw_line(line[0], line[1], color=self.MARK_COLOR, width=self.MARK_WIDTH)
