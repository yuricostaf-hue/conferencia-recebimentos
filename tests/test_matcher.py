"""Tests for the matcher module."""

from datetime import datetime, timedelta

import pytest

from core.matcher import Matcher
from core.models import AgendaEntry, BoundingBox, PaymentEntry


@pytest.fixture
def logger() -> None:
    """Fixture for logger."""
    return None


@pytest.fixture
def matcher(logger) -> Matcher:
    """Fixture for matcher."""
    return Matcher(logger)


@pytest.fixture
def sample_bbox() -> BoundingBox:
    """Fixture for bounding box."""
    return BoundingBox(x0=10, y0=20, x1=100, y1=30, page=0)


def test_matcher_compatibility(matcher: Matcher, sample_bbox: BoundingBox) -> None:
    """Test compatibility checking."""
    today = datetime.now()

    agenda = AgendaEntry(
        data=today,
        paciente="JOSE SILVA",
        procedimento="CONSULTA",
        convenio="UNIMED",
        situacao="Realizado",
        arquivo="agenda.pdf",
        pagina=1,
        bbox=sample_bbox,
        nome_normalizado="JOSE SILVA",
        procedimento_normalizado="CONSULTA",
    )

    # Same date - should be compatible
    payment_same = PaymentEntry(
        data=today,
        paciente="Jose Silva",
        procedimento="Consulta",
        valor=100.0,
        nome_normalizado="JOSE SILVA",
        procedimento_normalizado="CONSULTA",
    )

    assert matcher._is_compatible(agenda, payment_same) is True

    # Different date (too far) - should not be compatible
    payment_far = PaymentEntry(
        data=today + timedelta(days=40),
        paciente="Jose Silva",
        procedimento="Consulta",
        valor=100.0,
        nome_normalizado="JOSE SILVA",
        procedimento_normalizado="CONSULTA",
    )

    assert matcher._is_compatible(agenda, payment_far) is False


def test_matcher_score(matcher: Matcher, sample_bbox: BoundingBox) -> None:
    """Test score calculation."""
    today = datetime.now()

    agenda = AgendaEntry(
        data=today,
        paciente="Jose Silva",
        procedimento="Consulta",
        convenio="UNIMED",
        situacao="Realizado",
        arquivo="agenda.pdf",
        pagina=1,
        bbox=sample_bbox,
        nome_normalizado="JOSE SILVA",
        procedimento_normalizado="CONSULTA",
    )

    payment = PaymentEntry(
        data=today,
        paciente="Jose Silva",
        procedimento="Consulta",
        valor=100.0,
        nome_normalizado="JOSE SILVA",
        procedimento_normalizado="CONSULTA",
    )

    score = matcher._calculate_score(agenda, payment)
    assert 90 <= score <= 100  # Perfect match should have high score
