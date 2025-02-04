"""
file_name = app.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/08/2023
Description: A flask file used to server my personal website
Edit Log:
07/08/2023 
    - Changed file name to app.py from requests.py
    - Conformed to pylint conventions
"""

import logging.config

from flask import Flask, abort
from flask import request, send_from_directory

from apps.tool_repository.tools.endpoint_diagnostics import (
    setup_request,
    commit_endpoint_diagnostics,
)

# Create flask app. Static and template folder point to personal website react build files
app = Flask(
    __name__,
    static_url_path="",
    static_folder="/home/ghaz/PersonalWebsite/build",
    template_folder="/home/ghaz/PersonalWebsite/build",
)

# Set logger config
logging.config.fileConfig("/home/ghaz/flask_gateway/logging.conf")
app.logger = logging.getLogger("MainLogger")

# Handler for log file. So log files are rotated everyday
handler = logging.handlers.TimedRotatingFileHandler("logs/app.log", when="midnight")
handler.prefix = "%Y%m%d"

# Formatter for log file. Log files will be formatted in the format specified below
formatter = logging.Formatter(
    "%(asctime)s | %(pathname)s | \
    %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | \
    %(message)s"
)
handler.setFormatter(formatter)

# Add handler to the app logger
app.logger.addHandler(handler)


@app.before_request
def log_endpoint():
    """
    Logs information about the endpoint accessed and the client that accessed it.

    This function is triggered every time a request is received by the Flask application,
    before the request is processed by any view function.

    Returns:
        None
    """

    app.logger.info("Someone accessed the website %s %s", request.remote_addr,request.path)

    if request.path in {"/", "/projects", "/skills", "/education", "/resume"}:
        setup_request(request, request.path)


@app.after_request
def commit_diagnostics(response):
    """
    Commits diagnostic information about the endpoint accessed and the client that accessed it.

    This function is triggered every time a response is returned by the Flask application,
    after the response has been generated and before it is returned to the client.

    Args:
        response: The Flask response object to be returned to the client.

    Returns:
        The Flask response object.
    """

    if request.args.get("endpoint_id"):
        app.logger.info("Commiting endpoint diagonstic")
        commit_endpoint_diagnostics(
            request.args.get("endpoint_id"),
            f"Html associated with  {request.remote_addr}",
            "",
        )

    return response


@app.route("/")
def home_route():
    """
    A Flask view function that returns the home page of the website.

    Returns:
        A Flask response object containing the contents of the 'index.html' 
        file in the app's static directory.
    """

    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path>")
def render_path(path: str): # pylint: disable=inconsistent-return-statements
    """
    A Flask view function that attempts to return a file based on the provided URL path.

    If the requested path corresponds to a file that should be served, 
    the function returns that file.
    Otherwise, the function aborts the request with a 404 error.

    Args:
        path: A string representing the path component of 
        the requested URL.

    Returns:
        A Flask response object containing the contents of the requested file, 
        or a 404 response if the requested file does not exist.
    """

    # accept paths which we have files for
    if path in {"projects", "skills", "education", "resume"}:
        return send_from_directory(app.static_folder, "index.html")
    # Serve static files for other paths
    if path in {"robots.txt", "sitemap.xml"}:
        return send_from_directory(app.root_path + "/static/", path)

    # Return a 404 error for all other paths
    abort(404)


if __name__ == "__main__":
    app.run(debug=True)
