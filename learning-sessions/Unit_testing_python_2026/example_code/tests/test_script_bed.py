"""Unit tests for the calculate_gc_content function in bin/script_bed.py."""
import pytest
from bin.script_bed import calculate_total_bed_length


@pytest.fixture(name="valid_bed")
def valid_bed_factory(tmp_path):
    """Creates a valid 3-line BED file."""
    f = tmp_path / "valid.bed"
    f.write_text("chr1\t100\t200\nchr2\t0\t50")
    return f


@pytest.fixture(name="malformed_bed")
def malformed_bed_factory(tmp_path):
    """Creates a BED file with text in the coordinate columns."""
    f = tmp_path / "text_coords.bed"
    f.write_text("chr1\tstring_data\t200")
    return f


class TestBedDocumentationContract:
    """Verifies that the function adheres to its docstring specifications."""

    def test_returns_correct_int(self, valid_bed):
        """Verifies the 'Returns' section of the docstring."""
        result = calculate_total_bed_length(valid_bed)
        assert isinstance(result, int)
        assert result == 150

    def test_raises_file_not_found(self):
        """Verifies the 'Raises FileNotFoundError' section."""
        with pytest.raises(FileNotFoundError):
            calculate_total_bed_length("imaginary_file.bed")

    def test_raises_type_error(self, malformed_bed):
        """Verifies the 'Raises TypeError' section."""
        with pytest.raises(TypeError, match="must be numeric"):
            calculate_total_bed_length(malformed_bed)

    def test_raises_value_error(self, tmp_path):
        """Verifies the 'Raises ValueError' section."""
        f = tmp_path / "invalid_coords.bed"
        f.write_text("chr1\t200\t100")  # start > end
        with pytest.raises(ValueError, match="start > end"):
            calculate_total_bed_length(f)

    def test_empty_file_returns_zero(self, tmp_path):
        """Verifies that an empty BED file returns 0."""
        f = tmp_path / "empty.bed"
        f.write_text("")
        result = calculate_total_bed_length(f)
        assert result == 0
