from functools import wraps

import json
import logging
from flask import Flask, jsonify, request

import parser


app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = ""

logger = logging.getLogger("noobtube_api")


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info("Loading_video_url")
            url = request.args.get("id", None)
            if not url:
                logger.warning("Wrong_URL {0}".format(url))
                return jsonify(error="not valid url"), 400
            return func(url, *args, **kwargs)
        except Exception:
            logger.exception("Unexpected_error")
            return jsonify(error="Unexpected_error"), 500
    return wrapper


@app.route('/ping')
def ping():
    return jsonify(status="pong")


@app.route('/noobtube/video', methods=["GET"])
@error_handler
def send_url(id):
    video = parser.video_info(id)
    urls = parser.get_url(video)
    #return parser.get_best_quality(urls)
    return json.dumps(urls, indent=4)


if __name__ == "__main__":
    app.run(host="192.168.0.73", port=13337, threaded=True)
