"""Unit tests for get_clinvar_significance function in bin/clinvar_utils.py."""
import pytest
from bin.clinvar_utils import get_clinvar_significance


@pytest.fixture(name="clinvar_mock")
def mock_clinvar_factory(mocker):
    """A reusable fixture to mock the ClinVar API response."""
    # Patch the request.get method in the clinvar_utils module
    mock = mocker.patch('bin.clinvar_utils.requests.get')
    # Set a default return value
    mock_resp = mocker.Mock()
    mock_resp.json.return_value = {
        'clinical_significance':
            {'description': 'Likely Benign'}
        }
    mock.return_value = mock_resp
    return mock


class TestClinVarUtils:
    """Tests for the get_clinvar_significance function."""

    def test_significance_logic(
        self, clinvar_mock  # pylint: disable=unused-argument
    ):
        """
        Test that the function correctly extracts clinical
        significance from mocked API response.
        """
        # This test uses the fixture directly
        result = get_clinvar_significance('67890')
        assert result == 'Likely Benign'

    def test_key_error(self, clinvar_mock):
        """
        Test that a ValueError is raised when the expected
        keys are missing in the API response.
        """
        # Modify the mock to return a JSON without the expected keys
        clinvar_mock.return_value.json.return_value = {}
        with pytest.raises(
            ValueError,
            match="Could not find significance data for ID 67890"
        ):
            get_clinvar_significance('67890')
