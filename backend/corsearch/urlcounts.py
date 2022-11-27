from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse

from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from .logger import log_error
from .config import HOSTS_TXT_PATH


class UrlcountsResponseSchema(Schema):
    """Define response schema of endpoint '/urlcounts'.

    For field types, see - https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html
    """
    count_urls_match_a_host = fields.Int(metadata={"description": "Count of how many URLs match a host."},)
    count_urls_not_match_any_hosts = fields.Int(
        metadata={"description": "Count of how many URLs don’t match any hosts."},
    )
    count_urls_matched_per_host = fields.List(
        cls_or_instance=fields.Str,
        metadata={
            "description":
                "A list of all unique hosts for which there was a matching URL with a count of URLs that matched."
        },
    )
    urls_not_match_any_hosts = fields.List(
        cls_or_instance=fields.Str,
        metadata={"description": "A list of all URLs that did not match any hosts."},
    )


class UrlcountsAPI(MethodResource, Resource):
    """CLass to define Urlcounts API endpoints."""

    # To add Swagger markup, use the doc decorator. See https://flask-apispec.readthedocs.io/en/latest/usage.html
    @doc(description="Corsearch Technical Challenge - Urlcounts.")
    # Use use_kwargs to declare request parsing behavior. See https://flask-apispec.readthedocs.io/en/latest/usage.html
    @use_kwargs(
        args={"urls": fields.List(
            cls_or_instance=fields.Str,
            required=True, metadata={"description": "Input URL to process."}
        )},
        location="json",
    )
    # Use marshal_with to declare response marshalling. See https://flask-apispec.readthedocs.io/en/latest/usage.html
    @marshal_with(UrlcountsResponseSchema)
    def post(self, **kwargs):
        """Post method of Corsearch Urlcounts endpoint."""
        # Retrieve input URLs from request.
        input_urls = kwargs.get("urls", None)
        if not input_urls:
            return "Request data is not valid.", 400

        try:
            # Process submitted URLs.
            result_dict = process_urls(kwargs.get("urls", None))
        except Exception as ex:
            log_error(msg=str(ex))
            return f"Unexpected error: {ex.args}", 500

        return result_dict, 200


def read_hosts_txt(hosts_txt_path: Path) -> List:
    """Read a list of hosts from file 'hosts.txt'.

    Args:
        hosts_txt_path: Path of file 'hosts.txt'.
    Returns:
        A list of hosts in file 'hosts.txt'.
    """
    hosts_list = []

    # Opening the file in read mode.
    with open(hosts_txt_path, "r") as file_obj:
        # Reading the file.
        hosts_list = file_obj.read().split("\n")

    # Deduplicate the hosts.
    hosts_list = list(set(hosts_list)) if hosts_list else hosts_list

    return hosts_list


def extract_domain_name(url: str) -> str:
    """Get the domain name portion of the URL.

    Args:
        url: The URL to extract domain name from.

    Returns:
        The domain name portion of the URL.
    """
    # Extract the host name from url, i.e. including the www or subdomain.
    hostname = urlparse(url).netloc

    # Remove www from domain name.
    return hostname.replace("www.", "")


def process_urls(urls_list: List) -> Dict[str, Any]:
    """Process URLs according to the requirements.

    Args:
        urls_list: The URLs list to process.

    Returns:
        Result dict in the below format:
        {
            "count_urls_match_a_host": {The count of URLs that did match a host},
            "count_urls_not_match_any_hosts": {The count of URLs that did not match any hosts},
            "count_urls_matched_per_host":
                {List of all unique hosts for which there was a matching URL with a count of URLs that matched},
            "urls_not_match_any_hosts": {A list of all URLs that did not match any hosts},
        }
    """
    # Requirement:
    # Application must deduplicate the URLs that were POSTed to ensure that only unique URLs are counted.
    urls_list = list(set(urls_list))

    # Requirement:
    # Application must read data into memory from a text file called “hosts.txt” which will contain a list of hosts.
    hosts_list = read_hosts_txt(HOSTS_TXT_PATH)

    count_urls_submitted_per_host: Dict[str, int] = {}
    dict_count_urls_matched_per_host: Dict[str, int] = {}
    urls_not_match_any_hosts = []

    for url in urls_list:
        # Requirement: Get the domain name portion of the URL.
        domain_name = extract_domain_name(url)

        if domain_name not in hosts_list:
            # Requirement: Prepare a list of all URLs that did not match any hosts.
            urls_not_match_any_hosts.append(url)
        else:
            dict_count_urls_matched_per_host[domain_name] = dict_count_urls_matched_per_host.get(domain_name, 0) + 1

        # Requirement:
        # For each host, keep a count of how many matching URLs are submitted,
        # regardless of whether there is a match or not.
        count_urls_submitted_per_host[domain_name] = count_urls_submitted_per_host.get(domain_name, 0) + 1

    # Requirement: Keep a count of how many URLs don’t match any hosts.
    count_urls_not_match_any_hosts = len(urls_not_match_any_hosts)

    # Requirement: Keep a count of how many URLs match a host.
    count_urls_match_a_host = len(urls_list) - count_urls_not_match_any_hosts

    # Requirement:
    # Prepare a list of all unique hosts for which there was a matching URL with a count of URLs that matched.
    count_urls_matched_per_host = [
        f"count=[{val}] {key}" for (key, val) in dict_count_urls_matched_per_host.items() if val > 0
    ]

    return {
        "count_urls_match_a_host": count_urls_match_a_host,
        "count_urls_not_match_any_hosts": count_urls_not_match_any_hosts,
        "count_urls_matched_per_host": count_urls_matched_per_host,
        "urls_not_match_any_hosts": urls_not_match_any_hosts,
    }
