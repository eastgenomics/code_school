"""Unit tests for the calculate_gc_content function in bin/script.py."""
import pytest
from bin.script import calculate_gc_content


class TestGCContent:
    """Class to test valid input scenarios for GC content calculation."""

    def test_basic_sequence(self):
        """Test standard DNA sequence."""
        assert calculate_gc_content("GCGC") == 100.0

    def test_mixed_bases(self):
        """Test a mixture of all bases."""
        assert calculate_gc_content("ATGCGT") == 50.0

    def test_case_insensitivity(self):
        """Test that it handles lowercase and mixed-case letters."""
        assert calculate_gc_content("atgcgt") == 50.0
        assert calculate_gc_content("AtGcGt") == 50.0


class TestGCContentEdgeCases:
    """Class to test empty, invalid, or unusual input scenarios."""

    def test_empty_string(self):
        """Test empty string input."""
        assert calculate_gc_content("") == 0.0

    def test_invalid_input_type(self):
        """Test that a TypeError is raised for non-string inputs."""
        with pytest.raises(TypeError, match="Sequence must be a string"):
            calculate_gc_content(12345)

    def test_rounding(self):
        """Test that the result is rounded correctly."""
        # GC content of "GAT" is 1/3 = 33.3333...%
        assert calculate_gc_content("GAT") == 33.33

    def test_invalid_characters(self):
        """Test that a ValueError is raised for sequences with invalid characters."""
        with pytest.raises(ValueError, match="Sequence contains invalid characters. "
                           "Only A, T, G, C are allowed."):
            calculate_gc_content("ATGCX")