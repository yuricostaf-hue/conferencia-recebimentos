"""Tests for the normalizer module."""

import pytest

from core.normalizer import normalize_name, normalize_procedure, remove_accents


class TestRemoveAccents:
    """Tests for accent removal."""

    def test_remove_accents_basic(self) -> None:
        """Test basic accent removal."""
        assert remove_accents("José") == "Jose"
        assert remove_accents("Márcia") == "Marcia"
        assert remove_accents("Moçambique") == "Mocambique"

    def test_remove_accents_no_accents(self) -> None:
        """Test string without accents."""
        assert remove_accents("John") == "John"
        assert remove_accents("TEST") == "TEST"


class TestNormalizeName:
    """Tests for name normalization."""

    def test_normalize_name_basic(self) -> None:
        """Test basic name normalization."""
        assert normalize_name("José") == "JOSE"
        assert normalize_name("Márcia") == "MARCIA"

    def test_normalize_name_lowercase(self) -> None:
        """Test that lowercase is converted to uppercase."""
        assert normalize_name("john doe") == "JOHN DOE"

    def test_normalize_name_extra_spaces(self) -> None:
        """Test that extra spaces are removed."""
        assert normalize_name("John  Doe") == "JOHN DOE"

    def test_normalize_name_empty(self) -> None:
        """Test empty string."""
        assert normalize_name("") == ""
        assert normalize_name(None) == ""


class TestNormalizeProcedure:
    """Tests for procedure normalization."""

    def test_normalize_procedure_basic(self) -> None:
        """Test basic procedure normalization."""
        assert normalize_procedure("Consulta") == "CONSULTA"
        assert normalize_procedure("Videoendoscopia nasal") == "VIDEOENDOSCOPIA NASAL"

    def test_normalize_procedure_accents(self) -> None:
        """Test procedure with accents."""
        assert normalize_procedure("Cerúmen") == "CERUMEN"

    def test_normalize_procedure_empty(self) -> None:
        """Test empty procedure."""
        assert normalize_procedure("") == ""
        assert normalize_procedure(None) == ""
