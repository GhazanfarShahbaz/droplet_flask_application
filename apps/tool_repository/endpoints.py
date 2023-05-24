from datetime import datetime

from flask import Flask
from flask import request, jsonify, send_file
from flask import g as flask_globals

from firebase_admin import credentials, firestore, initialize_app

from os import environ, getenv

from response_processing.event_processing import print_events

from tools.repository.models.event_model import Event
from tools.endpoint_diagnostics import setup_request, commit_endpoint_diagnostics
from tools.process_assignment_requests import process_get_assignment_request, process_create_assignment, process_update_assignment, process_delete_assignment_request
from tools.process_class_requests import process_create_class, process_get_class_request, process_update_class, process_delete_class_request
from tools.process_event_requests import process_create_event, process_get_event, process_get_default_event, process_update_event, process_delete_event
from tools.process_endpoint_diagnostics import process_get_diagnostics
from tools.process_file_storage_requests import process_upload_file, process_delete_file
from tools.process_gmail_requests import get_emails
from tools.process_help_requests import get_command
from tools.process_log_requests import process_get_logs
from tools.process_syllabus_requests import process_get_syllabus_request, process_create_syllabus, process_update_syllabus, process_delete_syllabus_request
from tools.process_translate_request import process_translate
from tools.process_qr_code_requests import processs_generate_link_qr_code
from tools.process_weather_requests import get_weather


from typing import List
from json import loads

import logging.config

app = Flask(__name__)

logging.config.fileConfig('/home/ghaz/flask_gateway/logging.conf')
app.logger = logging.getLogger('MainLogger')

handler = logging.handlers.TimedRotatingFileHandler(
'logs/app.log', when="midnight")

handler.prefix = "%Y%m%d"

formatter = logging.Formatter(fmt='%(asctime)s | %(pathname)s | %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

APP_PATH: str = "/tools"

cred = credentials.Certificate(environ["FIRESTORE_TOKEN"])
initialize_app(cred)

@app.before_request   
def log_request() -> None:
    """
    Logs the incoming request.

    This function logs the incoming request, including the IP address of the request and the path of the request.
    If the request includes JSON data, the function logs this as well. The function then validates the request
    user using the `validate_user` function. If the user is invalid, the function returns a status dictionary with
    "Status": "Invalid Request". The function then sets up the request with `setup_request`.

    Returns:
        None.
    """
    
    app.logger.info(f" {request.remote_addr} {APP_PATH}{request.path}")
    app.logger.info(request.json)
    
    content_type: str = request.content_type
    request_form = None 
    
    if content_type == "multipart/form-data":
        request_form = loads(request.form["json"])
        request.json = request_form
    else:
        request_form = request.json
    
    if not validate_user(request_form.get("username"), request_form.get("password")):
        return {"Status": "Invalid Request"}
    
    setup_request(request, f"tools{request.path}")


@app.after_request
def commit_diagnostics(response):
    """
    Commits endpoint diagonstic information after handling a request.

    This function takes a response object and checks if the request includes an "endpoint_id" parameter.
    If the parameter is present, the function logs a message and commits endpoint diagnostic information
    using the `commit_endpoint_diagnostics` function. The function then returns the original response.

    Args:
        response: A Flask response object representing the response to a request.

    Returns:
        The original Flask response object.

    Raises:
        None.
    """
    
    if request.args.get("endpoint_id"):
        app.logger.info("Commiting endpoint diagonstic")
        commit_endpoint_diagnostics(request.args.get("endpoint_id"), f"Html associated with  {request.remote_addr}", "")
        
    return response


def get_login(from_server=False) -> dict:
    """
    Retrieves login information from Firebase.

    This function retrieves login information from Firebase Firestore. If the `from_server` argument is
    False (default), the function checks if the server is currently allowing login by checking if the "allow"
    field of the "allow" document in the collection named in `FIRESTORE_SERVER` is True. If the field is False,
    the function returns None. If the field is True or the `from_server` argument is True, the function sets
    the "allow" field to False and retrieves the login information from the document specified in `FIRESTORE_DOC_ID`.

    Args:
        from_server: A boolean indicating whether the request is coming from a server.

    Returns:
        A dictionary containing the login information.

    Raises:
        None
    """    
        
    db = firestore.client()
    users_ref = db.collection(environ["FIRESTORE_SERVER"])
    login_allow = users_ref.document('allow')

    if not from_server and login_allow.get().to_dict()["allow"] is False:
        return None

    login_allow.update({
        u'allow': False
    })

    return users_ref.document(environ["FIRESTORE_DOC_ID"]).get().to_dict()


def validate_user(username: str, password: str) -> bool:
    """
    Validates the user login credentials.

    This function takes a string `username` representing the user's login username and a string `password`
    representing the user's login password. The function retrieves the login information using the `get_login`
    function and checks whether the provided `username` and `password` match the login information. If the
    login information matches, the function returns True. Otherwise, the function logs a message and returns
    False.

    Args:
        username: A string representing the user's login username.
        password: A string representing the user's login password.

    Returns:
        A boolean indicating whether or not the user's login credentials are valid.

    Raises:
        None.
    """
    
    token = get_login()

    if token and (username and username == token["username"]) and (password and password == token["password"]):
        return True

    app.logger.info(
        f'Invalid Username and Password were supplied {request.remote_addr} /tools/{request.path} on {datetime.now()}'
    )
    return False


@app.route("/createEvent", methods=["POST"])
def create_event():
    request_form = request.json

    if request_form.get("eventForm"):
        process_create_event(request_form.get("eventForm"))

    return "Success"

@app.route("/addEventsFromCSV", methods=["POST"])
def add_events_from_csv():
    request_form = request.json


@app.route("/getEvent", methods=["POST"])
def get_events():
    request_form = request.json
    event_list: List[Event] = []

    if request_form.get("defaultForm"):
        event_list = process_get_default_event(
            request_form.get("defaultForm"))
    elif request_form.get("filterForm"):
        event_list = process_get_event(request_form.get("filterForm"))
    else:
        event_list = process_get_event({})

    return jsonify(event_list) if request_form.get("stringifyResult") is None else jsonify(print_events(event_list, set()))


@app.route("/updateEvent", methods=["POST"])
def update_event():
    request_form = request.json

    if request_form.get("filterForm"):
        process_update_event(request_form.get("filterForm"))

    return "Success"


@app.route("/deleteEvent", methods=["POST"])
def delete_event():
    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_event(request_form.get("deleteForm"))

    return "Success"


@app.route("/addClass", methods=["POST"])
def add_class():
    request_form = request.json

    if request_form.get("classForm"):
        process_create_class(request_form.get("classForm"))

    return {}


@app.route("/getClass", methods=["POST"])
def get_class():
    request_form = request.json

    if request_form.get("filterForm"):
        process_get_class_request(request_form.get("filterForm"))

    return {}


@app.route("/updateClass", methods=["POST"])
def update_class():
    request_form = request.json

    if request_form.get("updateForm"):
        process_update_class(request_form.get("updateForm"))

    return {}


@app.route("/deleteClass", methods=["POST"])
def delete_class():
    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_class_request(request_form.get("deleteForm"))

    return {}


@app.route("/addSyllabus", methods=["POST"])
def add_syllabus():
    request_form = request.json

    if request_form.get("syllabusForm"):
        process_create_syllabus(request_form.get("syllabusForm"))

    return {}


@app.route("/getSyllabus", methods=["POST"])
def get_syllabus():
    request_form = request.json

    if request_form.get("filterForm"):
        process_get_syllabus_request(request_form.get("filterForm"))

    return {}


@app.route("/updateSyllabus", methods=["POST"])
def update_syllabus():
    request_form = request.json
    
    if request_form.get("updateForm"):
        process_update_syllabus(request_form.get("updateForm"))

    return {}


@app.route("/deleteSyllabus", methods=["POST"])
def delete_syllabus():
    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_syllabus_request(request_form.get("deleteForm"))

    return {}


@app.route("/addAssignment", methods=["POST"])
def add_assignment():
    request_form = request.json

    if request_form.get("assignmentForm"):
        process_create_assignment(request_form.get("assignmentForm"))

    return {}


@app.route("/getAssignment", methods=["POST"])
def get_assignment():
    request_form = request.json

    if request_form.get("filterForm"):
        process_get_assignment_request(request_form.get("filterForm"))

    return {}


@app.route("/updateAssignment", methods=["POST"])
def update_assignment():
    request_form = request.json

    if request_form.get("updateForm"):
        process_update_assignment(request_form.get("updateForm"))

    return {}


@app.route("/deleteAssignment", methods=["POST"])
def delete_assignment():
    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_assignment_request(request_form.get("deleteForm"))

    return {}


@app.route("/getCurrentWeather", methods=["POST"])
def get_current_weather():
    request_form = request.json

    return get_weather()


@app.route("/getGmailEmails", methods=["POST"])
def get_gmail_emails():
    request_form = request.json

    return get_emails(request_form.get("authorizationFile"), request_form.get("labelFilters"), request_form.get("maxResults"), request_form.get("snippet"))


@app.route("/getTranslation", methods=["POST"])
def get_translation():
    request_form = request.json

    return process_translate(request_form.get("translationForm"))


@app.route("/uploadFile", methods=["POST"])
def upload_file():
    file = request.files["file"]

    return process_upload_file(file, request.mimetype)


@app.route("/deleteFile", methods=["POST"])
def delete_file():
    request_form = request.json

    return process_delete_file(request_form.get("deleteForm"))


@app.route("/sendTextMessage", methods=["POST"])
def send_message():
    request_form = request.json


@app.route("/generateLinkQRCode", methods=["POST"])
def generate_qr_code_for_link():
    request_form = request.json

    qr_io = processs_generate_link_qr_code(request_form["qrForm"])

    app.logger.info(qr_io)

    return send_file(qr_io, mimetype='image/jpeg')

@app.route("/getEndpointDiagnostics", methods=["POST"])
def get_endpoints_data():
    request_form = request.json
    
    return process_get_diagnostics(request_form.get("filterForm"))


@app.route("/getHelp", methods=["POST"])
def get_help():
    request_form = request.json

    return get_command(request_form.get("command"))


@app.route("/getLogs", methods=["POST"])
def get_logs():
    request_form = request.json

    return process_get_logs()


@app.route("/setEnvironmentVariable", methods=["POST"])
def set_environment_variable():
    request_form = request.json

    environment_form = request_form.get("environmentForm")
    key: str = environment_form["key"]
    value: str = environment_form["value"]

    if getenv(key) and not environ[environment_form["overwrite"]]:
        return {"Status": "Needs overwrite permission"}

    db = firestore.client()
    users_ref = db.collection(environ["FIRESTORE_SERVER"])
    environment_document = users_ref.document(
        environ["FIRESTORE_ENVIRONMENT_ID"])

    environment_document.update({
        key: value
    })

    environ[key] = value
    return {"Status": "Success"}


if __name__ == "__main__":
    app.run(debug=True)
