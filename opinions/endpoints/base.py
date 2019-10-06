"""
Base endpoints and useful endpoints for the rest of the application.
"""
from datetime import datetime
import uuid

from flask import Blueprint
from flask import current_app
from flask import render_template

from opinions.core import logger
from opinions.json_encoding import jsonify


Base = Blueprint(
    'Base',
    __name__,
    static_folder='static',
    static_url_path='/static/',
    template_folder='templates')


@Base.route('/', methods=['GET'])
def index():
    """
    Basic index with a template rendered, a log message,
    and a value retrieved from config.
    """
    log = logger.new(function="index", endpoint="/", method='GET')
    version = current_app.config.get("version")
    # Structlog allows arbitrary kwargs in log output
    log.info("Get index", version=version)
    return render_template(
        'index.html',
        version=version)


@Base.route('/health', methods=['GET'])
def health():
    """
    We will need a health endpoint for our load balancers to make sure this app is alive.
    """
    return "ok"


@Base.route('/json', methods=['GET'])
def json_encoder():
    """
    Sometimes it's useful to control the way in which JSON is serialized and
    deserialized in our application. For instance, we can make sure that
    datetime objects all use ISO 8601 formatting:

    In [12]: resp = requests.get("http://localhost:8000/json")

    In [13]: resp.json()
    Out[13]:
      {'status': 'success',
       'uuid_example': 'ff2a8e68-a071-4677-b19b-0a5d90c1191a',
       'datetime_example': '2019-10-06T01:45:05.523241',
       'message': 'JSON Payload encoded with rapidjson',
       'version': '0.0.1'}
    """
    version = current_app.config.get("version")
    return jsonify({"status": "success",
                    "uuid_example": uuid.uuid4(),
                    "datetime_example": datetime.utcnow(),
                    "message": "JSON Payload encoded with rapidjson",
                    "version": version})
