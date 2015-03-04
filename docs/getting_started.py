# Load in our dependencies
from flask import Flask, request, jsonify
from flask_json_multidict import get_json_multidict

# Start an application
app = Flask(__name__)

def resolve_request_body():
    """Before every request, resolve `request.body` from either `request.form` or `request.get_json()`"""
    request.body = request.form
    if request.headers['content-type'] == 'application/json':
        request.body = get_json_multidict(request)
app.before_request(resolve_request_body)

@app.route('/', methods=['POST'])
def root():
    """Reply with POST data as we see it"""
    body = request.body
    return jsonify({key: body[key] for key in body})
    # We can also leverage `request.body.getlist` as we do with `request.form`


if __name__ == '__main__':
    app.run(port=9001)
