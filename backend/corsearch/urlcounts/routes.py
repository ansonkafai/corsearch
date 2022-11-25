from flask import Blueprint, request, jsonify

from ..config import HOSTS_TXT_PATH
from ..logger import log_error
from .utils import process_urls

urlcounts_blueprint = Blueprint("urlcounts", __name__)


@urlcounts_blueprint.route("/urlcounts", methods=["POST"])
def urlcounts():
    # The POST body data should be valid JSON.
    if not request.data or not request.json:
        return "Request data is not a valid JSON.", 400
    if "urls" not in request.json:
        return "Item 'urls' cannot be found from request JSON.", 400

    try:
        # Process submitted URLs.
        urls_list = request.json["urls"]
        result_dict = process_urls(urls_list)
    except Exception as ex:
        log_error(msg=str(ex))
        return f"Unexpected error: {ex.args}", 500

    return jsonify(result_dict), 200
