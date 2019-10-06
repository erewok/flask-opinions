"""
Base endpoints and useful endpoints for the rest of the application.
"""
from flask import Blueprint
from flask import current_app
from flask import render_template

from opinions import http
from opinions.core import logger


Base = Blueprint(
    'Base',
    __name__,
    static_folder='static',
    static_url_path='/static/',
    template_folder='templates')


@Base.route('/', methods=['GET'])
def index():
    log = logger.new(function="index", endpoint="/", method='GET')
    version = current_app.config.get("version")
    # Structlog allows arbitrary kwargs in log output
    log.info("Get index", version=version)
    return render_template(
        'index.html',
        version=version)


@Base.route('/health', methods=['GET'])
def health():
    version = current_app.config.get("version")
    return {"status": http.Success.status,
            "message": "Healthy",
            "version": version}
