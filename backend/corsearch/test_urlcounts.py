import json
from pathlib import Path
from unittest import mock

from .app import app


class TestUrlcounts:
    hosts_txt_path = Path("./corsearch/test_data/hosts.txt").absolute()
    urls_json_path = Path("./corsearch/test_data/urls.json").absolute()

    def setup_class(self):
        """Initialize client object to test flask endpoints."""
        self.app_client = app.test_client()

    @mock.patch("corsearch.urlcounts.utils.HOSTS_TXT_PATH", hosts_txt_path)
    def test_urlcounts_success(self):
        """Test the successful cases of '/urlcounts' endpoint."""
        # Read URLs from urls.json file.
        with open(TestUrlcounts.urls_json_path, "r", encoding="utf-8") as in_file_obj:
            json_data = json.load(in_file_obj)

        # Call API endpoint with supplying valid JSON data.
        resp = self.app_client.post("/urlcounts", json=json_data)
        resp_json = resp.get_json()

        assert resp_json["int_count_urls_match_a_host"] == 2
        assert resp_json["int_count_urls_not_match_any_hosts"] == 2
        assert "count=[2] torrentdownloads.test" in list(resp_json["list_count_urls_matched_per_host"])
        assert len(resp_json["list_urls_not_match_any_hosts"]) == 2

    def test_urlcounts_fail(self):
        """Test the fail cases of '/urlcounts' endpoint."""
        # Call API endpoint without JSON data.
        resp = self.app_client.post("/urlcounts", json={})

        assert resp.status_code == 400
        assert resp.text == "Request data is not a valid JSON."
