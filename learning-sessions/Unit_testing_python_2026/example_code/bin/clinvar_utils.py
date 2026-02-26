"""Utility functions for fetching clinical significance from ClinVar."""
import requests


def get_clinvar_significance(variation_id):
    """
    Fetches clinical significance from ClinVar for a given Variation ID.

    Parameters
    ----------
    variation_id : str
        The ClinVar Variation ID (e.g., '12345').

    Returns
    -------
    str
        The clinical significance of the variant.

    Raises
    ------
    requests.exceptions.RequestException
        If the API call fails.
    ValueError
        If the Variation ID is not found or data is malformed.
    """
    # ClinVar API endpoint for variant data
    url = ("https://api.ncbi.nlm.nih.gov/variation/v0/beta/"
           f"clinical-significance/variation/{variation_id}")

    # Send GET request
    response = requests.get(url, timeout=10)

    # Raise exception for bad status codes
    response.raise_for_status()

    data = response.json()

    # Parse the nested JSON structure to get the significance
    try:
        significance = data['clinical_significance']['description']
    except KeyError as exc:
        raise ValueError(
            f"Could not find significance data for ID {variation_id}") from exc
    else:
        return significance
