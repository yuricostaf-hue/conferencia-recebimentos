"""Data models for the application."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BoundingBox:
    """Represents a text bounding box in PDF coordinates."""

    x0: float
    """Left coordinate."""
    y0: float
    """Top coordinate."""
    x1: float
    """Right coordinate."""
    y1: float
    """Bottom coordinate."""
    page: int
    """Page number (0-indexed)."""


@dataclass
class AgendaEntry:
    """Represents a single entry from an agenda PDF."""

    data: datetime
    """Date and time of the appointment."""
    paciente: str
    """Patient name."""
    procedimento: str
    """Medical procedure."""
    convenio: str
    """Insurance plan."""
    situacao: str
    """Appointment status."""
    arquivo: str
    """Source PDF filename."""
    pagina: int
    """Page number in PDF (1-indexed)."""
    bbox: BoundingBox
    """Bounding box of the patient name."""
    nome_normalizado: str
    """Normalized patient name."""
    procedimento_normalizado: str
    """Normalized procedure name."""

    def __post_init__(self) -> None:
        """Initialize normalized fields if not provided."""
        if not self.nome_normalizado:
            from .normalizer import normalize_name
            self.nome_normalizado = normalize_name(self.paciente)
        if not self.procedimento_normalizado:
            from .normalizer import normalize_procedure
            self.procedimento_normalizado = normalize_procedure(self.procedimento)


@dataclass
class PaymentEntry:
    """Represents a payment entry from demonstrativo PDF."""

    data: datetime
    """Payment date."""
    paciente: str
    """Patient name."""
    procedimento: str
    """Paid procedure."""
    valor: float
    """Payment value."""
    nome_normalizado: str
    """Normalized patient name."""
    procedimento_normalizado: str
    """Normalized procedure name."""

    def __post_init__(self) -> None:
        """Initialize normalized fields if not provided."""
        if not self.nome_normalizado:
            from .normalizer import normalize_name
            self.nome_normalizado = normalize_name(self.paciente)
        if not self.procedimento_normalizado:
            from .normalizer import normalize_procedure
            self.procedimento_normalizado = normalize_procedure(self.procedimento)


@dataclass
class MatchResult:
    """Result of matching an agenda entry with a payment."""

    agenda_entry: AgendaEntry
    """The agenda entry."""
    payment_entry: Optional[PaymentEntry]
    """The matched payment, or None if no match found."""
    match_score: float
    """Similarity score (0-100)."""
    is_paid: bool
    """Whether the procedure was paid."""
