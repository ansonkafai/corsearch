import json
from pathlib import Path
from unittest import mock

from corsearch.app import app


class TestUrlcounts:
    # Retrieve the full path of test input files.
    hosts_txt_path = Path("./corsearch/tests/hosts.txt").absolute()
    urls_json_path = Path("./corsearch/tests/urls.json").absolute()

    def setup_class(self):
        """Test instance setup."""
        # Initialize client object to test flask endpoints.
        self.app_client = app.test_client()

    @mock.patch("corsearch.urlcounts.HOSTS_TXT_PATH", hosts_txt_path)
    def test_urlcounts_success(self):
        """Test the successful cases of '/urlcounts' endpoint."""
        # Read input URLs from urls.json file.
        with open(TestUrlcounts.urls_json_path, "r", encoding="utf-8") as in_file_obj:
            json_data = json.load(in_file_obj)

        # Call API endpoint with supplying valid JSON data (i.e. the input URLs).
        resp = self.app_client.post("/urlcounts", json=json_data)
        resp_json = resp.get_json()

        # Unit test assertions.
        assert resp_json["count_urls_match_a_host"] == 2
        assert resp_json["count_urls_not_match_any_hosts"] == 2
        assert "count=[2] torrentdownloads.test" in list(resp_json["count_urls_matched_per_host"])
        assert sorted(resp_json["urls_not_match_any_hosts"]) == sorted(
            ["http://dummydummyhostname/dummytest2", "http://dummydummyhostname/dummytest1"]
        )

    def test_urlcounts_fail(self):
        """Test the fail cases of '/urlcounts' endpoint."""
        # Call API endpoint without JSON data. Expected response: 422 Unprocessable Entity
        resp = self.app_client.post("/urlcounts", json=None)
        assert resp.status_code == 422

        # Call API endpoint without any items in JSON data. Expected response: 422 Unprocessable Entity
        resp = self.app_client.post("/urlcounts", json={})
        assert resp.status_code == 422

        # Call API endpoint with "urls"=None in JSON data. Expected response: 422 Unprocessable Entity
        resp = self.app_client.post("/urlcounts", json={"urls": None})
        assert resp.status_code == 422

        # Call API endpoint with empty "urls" list in JSON data. Expected response: 400 Bad request
        resp = self.app_client.post("/urlcounts", json={"urls": []})
        assert resp.status_code == 400
