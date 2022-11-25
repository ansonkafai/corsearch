from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse

from ..config import HOSTS_TXT_PATH


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


def process_urls(urls_list: List) -> Dict[str, Any]:
    """Process URLs according to the requirements.

    Args:
        urls_list: The URLs list to process.

    Returns:
        The process result dict in the below format:
        {
            "int_count_urls_match_a_host": <The count of URLs that did match a host>,
            "int_count_urls_not_match_any_hosts": <The count of URLs that did not match any hosts>,
            "list_count_urls_matched_per_host":
                <A list of all unique hosts for which there was a matching URL with a count of URLs that matched>,
            "list_urls_not_match_any_hosts": <A list of all URLs that did not match any hosts>,
        }
    """
    # Application must deduplicate the URLs that were POSTed to ensure that only unique URLs are counted.
    urls_list = list(set(urls_list))

    # Application must read data into memory from a text file called “hosts.txt” which will contain a list of hosts.
    hosts_list = read_hosts_txt(HOSTS_TXT_PATH)

    dict_count_urls_submitted_per_host: Dict[str, int] = {}
    list_urls_not_match_any_hosts = []

    for url in urls_list:
        # Get the domain name portion of the URL.
        domain_name = urlparse(url).netloc

        if domain_name not in hosts_list:
            # Prepare a list of all URLs that did not match any hosts.
            list_urls_not_match_any_hosts.append(url)

        # For each host, keep a count of how many matching URLs are submitted,
        # regardless of whether there is a match or not.
        dict_count_urls_submitted_per_host[domain_name] = dict_count_urls_submitted_per_host.get(domain_name, 0) + 1

    # Keep a count of how many URLs don’t match any hosts.
    int_count_urls_not_match_any_hosts = len(list_urls_not_match_any_hosts)

    # Keep a count of how many URLs match a host.
    int_count_urls_match_a_host = len(urls_list) - int_count_urls_not_match_any_hosts

    # Prepare a list of all unique hosts for which there was a matching URL with a count of URLs that matched.
    list_count_urls_matched_per_host = [
        f"count=[{val}] {key}" for (key, val) in dict_count_urls_submitted_per_host.items() if val > 0
    ]

    return {
        "int_count_urls_match_a_host": int_count_urls_match_a_host,
        "int_count_urls_not_match_any_hosts": int_count_urls_not_match_any_hosts,
        "list_count_urls_matched_per_host": list_count_urls_matched_per_host,
        "list_urls_not_match_any_hosts": list_urls_not_match_any_hosts,
    }
