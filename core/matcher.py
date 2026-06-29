"""Matching logic for agenda and payment entries."""

from datetime import datetime, timedelta
from typing import Optional

from rapidfuzz import fuzz

from .logger import ApplicationLogger
from .models import AgendaEntry, MatchResult, PaymentEntry


class Matcher:
    """Matches agenda entries with payment entries."""

    # Fuzzy matching threshold (0-100)
    SIMILARITY_THRESHOLD = 95

    # Maximum date difference in days
    MAX_DATE_DIFFERENCE = 30

    def __init__(self, logger: Optional[ApplicationLogger] = None) -> None:
        """Initialize the matcher.

        Args:
            logger: Application logger instance.
        """
        self.logger = logger or ApplicationLogger()

    def match_entries(
        self,
        agenda_entries: list[AgendaEntry],
        payment_entries: list[PaymentEntry],
    ) -> list[MatchResult]:
        """Match agenda entries with payment entries.

        Args:
            agenda_entries: List of agenda entries.
            payment_entries: List of payment entries.

        Returns:
            List of MatchResult objects.
        """
        results: list[MatchResult] = []

        for agenda_entry in agenda_entries:
            # Find best matching payment entry
            best_match: Optional[PaymentEntry] = None
            best_score: float = 0

            for payment_entry in payment_entries:
                if self._is_compatible(agenda_entry, payment_entry):
                    score = self._calculate_score(agenda_entry, payment_entry)
                    if score > best_score:
                        best_score = score
                        best_match = payment_entry

            is_paid = best_match is not None and best_score >= self.SIMILARITY_THRESHOLD

            result = MatchResult(
                agenda_entry=agenda_entry,
                payment_entry=best_match,
                match_score=best_score,
                is_paid=is_paid,
            )
            results.append(result)

            if is_paid:
                self.logger.debug(
                    f"Matched: {agenda_entry.paciente} - {agenda_entry.procedimento} "
                    f"(score: {best_score:.1f})"
                )

        return results

    def _is_compatible(
        self, agenda_entry: AgendaEntry, payment_entry: PaymentEntry
    ) -> bool:
        """Check if entries are compatible for matching.

        Args:
            agenda_entry: Agenda entry.
            payment_entry: Payment entry.

        Returns:
            True if entries might match.
        """
        # Check date proximity
        date_diff = abs((agenda_entry.data - payment_entry.data).days)
        if date_diff > self.MAX_DATE_DIFFERENCE:
            return False

        # Check name similarity
        name_ratio = fuzz.ratio(
            agenda_entry.nome_normalizado, payment_entry.nome_normalizado
        )
        if name_ratio < 80:  # Lower threshold for pre-filtering
            return False

        return True

    def _calculate_score(
        self, agenda_entry: AgendaEntry, payment_entry: PaymentEntry
    ) -> float:
        """Calculate match score between two entries.

        Args:
            agenda_entry: Agenda entry.
            payment_entry: Payment entry.

        Returns:
            Match score (0-100).
        """
        # Name similarity
        name_score = fuzz.ratio(
            agenda_entry.nome_normalizado, payment_entry.nome_normalizado
        )

        # Procedure similarity
        procedure_score = fuzz.ratio(
            agenda_entry.procedimento_normalizado,
            payment_entry.procedimento_normalizado,
        )

        # Date proximity (100 if same day, decreasing with distance)
        date_diff = abs((agenda_entry.data - payment_entry.data).days)
        date_score = max(0, 100 - (date_diff * 3))

        # Weighted average
        # Name is most important, procedure is second, date is tertiary
        final_score = (name_score * 0.5) + (procedure_score * 0.35) + (date_score * 0.15)

        return final_score
