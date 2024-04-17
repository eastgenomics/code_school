"""
Codeschool task for 15/04/24
- Get an atlassian API token
- Get number of documents in a particular confluence space with a particular label
- Docs: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about

# e.g. labels = controlled and space = DV
❯ curl --request GET --url 'https://cuhbioinformatics.atlassian.net/wiki/api/v2/labels/2656043029/pages?space-id=2903080965' --user 'email:token' --header 'Accept: application/json'
"""
import argparse
import json
import os
import requests
import sys

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


load_dotenv()

EMAIL = os.environ.get('JIRA_EMAIL')
API_TOKEN = os.environ.get('JIRA_TOKEN')

AUTH = HTTPBasicAuth(EMAIL, API_TOKEN)
HEADERS = {"Accept": "application/json"}

CUH_BASE = "https://cuhbioinformatics.atlassian.net"
LABELS_URL = f"{CUH_BASE}/wiki/api/v2/labels"
SPACES_URL = f"{CUH_BASE}/wiki/api/v2/spaces"


def parse_args():
    """
    Parse command line arguments

    Returns
    -------
    args : Namespace
        Namespace of passed command line argument inputs
    """
    parser = argparse.ArgumentParser(
        description='Settings to search Confluence'
    )

    parser.add_argument(
        '-l',
        '--label',
        type=str,
        required=True,
        help="Label to search for"
    )

    parser.add_argument(
        '-s',
        '--space',
        type=str,
        required=True,
        help='Space to search in'
    )

    return parser.parse_args()


def get_response(base_url):
    """
    Get info from the Atlassian API
    Parameters
    ----------
    base_url :  str
        the URL to query
    Returns
    -------
    all_response_data :  list
        list of dicts with results data from API request
    """

    all_response_data = []
    new_data = True

    while new_data:
        # Make GET request, use timeout of 10 minutes
        response = requests.request(
            "GET",
            url=base_url,
            headers=HEADERS,
            auth=AUTH,
            timeout=600
        )

        # If status of response is OK (200) load response as json
        # if there's extra data there will be a nested 'next' key in '_links'
        # with URL to get the next page of results
        # so add the results to list and change URL for request to new URL
        # otherwise key won't exist so we stop making requests
        if response.ok:
            response_results = json.loads(response.text)
            new_data = response_results.get('_links', {}).get('next')
            results_data = response_results['results']
            all_response_data += results_data
            base_url = f"{CUH_BASE}{new_data}"
        else:
            print("Return code not OK")
            sys.exit(1)

    return all_response_data


def get_id_of_space_or_label(string_to_find, confluence_response, json_key):
    """
    Get the ID of a space or label we are trying to find pages for

    Parameters
    ----------
    string_to_find : str
        string (i.e. label or space) that we're trying to get the ID of
    confluence_response : list
        list of dicts with results data from API request
    json_key : str
        the name of the key that we're searching for in the JSON

    Returns
    -------
    id_of_thing: str
        The ID of the label or space
    """
    id_of_thing = None

    for entry in confluence_response:
        if entry[json_key] == string_to_find:
            id_of_thing = entry['id']

    assert id_of_thing, (
        f"The string {string_to_find} given was not found in the Confluence "
        "response. Please check that the string is a valid label or space key"
    )

    return id_of_thing


def main():
    """
    Main function to get pages in space with label
    """
    args = parse_args()

    # Get all of the possible labels and spaces in our Confluence
    all_labels = get_response(LABELS_URL)
    all_spaces = get_response(SPACES_URL)

    # Get the IDs of the label and space entered as args
    label_id = get_id_of_space_or_label(args.label, all_labels, 'name')
    space_id = get_id_of_space_or_label(args.space, all_spaces, 'key')

    pages_url = (
        f"{CUH_BASE}/wiki/api/v2/labels/{label_id}/pages?space-id={space_id}"
    )

    # Search for all of the pages in that space with that label
    pages_data = get_response(pages_url)

    print(
        f"There are {len(pages_data)} pages with the label {args.label} in "
        f"the space {args.space}:"
    )
    for index, page in enumerate(pages_data):
        print(index+1, page['title'])


if __name__ == '__main__':
    main()
