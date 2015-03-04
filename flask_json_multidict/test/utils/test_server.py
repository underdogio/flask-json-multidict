# Load in our dependencies
from flask import Flask, request, jsonify
from flask_json_multidict import get_json_multidict

# Define our application
test_server = Flask(__name__)


@test_server.route('/')
def root():
    """Endpoint to verify server is up"""
    return 'Hello World!'


@test_server.route('/echo', methods=['GET', 'POST'])
def echo():
    """Echo back `form`/`json` data"""
    # Grab body as either from `request.get_json` or `request.form`
    body = request.form
    if request.headers['content-type'] == 'application/json':
        body = get_json_multidict(request)

    # Serialize request information for asserting
    return jsonify({
        'method': request.method,
        'content-type': request.headers['content-type'],
        'body': {key: body[key] for key in body}
    })


@test_server.route('/list', methods=['GET', 'POST'])
def list():
    """Echo back `form`/`json` data"""
    body = request.form
    if request.headers['content-type'] == 'application/json':
        body = get_json_multidict(request)

    # Serialize request information for asserting
    return jsonify({
        'method': request.method,
        'content-type': request.headers['content-type'],
        'body': {key: body.getlist(key) for key in body}
    })
