import threading
import socket
import logging
import os
import uuid
import jwt
import app_utils
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from http.server import HTTPServer
from prometheus_client import MetricsHandler
from flask import Flask, request, send_file, jsonify, make_response, after_this_request
from functools import wraps

hostName = '0.0.0.0'
os_dir = './'
PROMETHEUS_PORT = 8000
CRAWL_PERIOD = 86400
mongo_utils = None

class PrometheusEndpointServer(threading.Thread):
    """A thread class that holds an http and makes it serve_forever()."""
    def __init__(self, httpd, *args, **kwargs):
        self.httpd = httpd
        super(PrometheusEndpointServer, self).__init__(*args, **kwargs)

    def run(self):
        self.httpd.serve_forever()


def start_prometheus_server():
    try:
        httpd = HTTPServer((hostName, PROMETHEUS_PORT), MetricsHandler)
    except (OSError, socket.error):
        return

    thread = PrometheusEndpointServer(httpd)
    thread.daemon = True
    thread.start()
    logging.info("Exporting Prometheus /metrics/ on port %s", PROMETHEUS_PORT)


server = Flask(__name__)
start_prometheus_server()
server.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            global mongo_utils
            if mongo_utils is None:
                mongo_utils = app_utils.get_mongo_utils()

            data = jwt.decode(token.split()[1], server.config['SECRET_KEY'])
            expire_time = data.get('exp', None)

            if expire_time is None or expire_time < int(datetime.now().timestamp() * 1000):
                return jsonify({
                    'message': 'Token is Expire!!'
                }), 401

            current_user = mongo_utils.get_record_by_public_id(data.get('publicId'))
            if not current_user:
                return jsonify({
                    'message': 'Token is invalid !!'
                }), 401
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@server.route('/generate',  methods=['POST'])
@token_required
def generate(current_user):
    user_data = request.get_json()
    score = app_utils.from_json_to_score(user_data)
    # TODO Call Model
    result = score
    global mongo_utils
    if mongo_utils is None:
        mongo_utils = app_utils.get_mongo_utils()
    json_result = app_utils.from_score_to_json(result, user_data)
    mongo_utils.update_data(current_user.get('publicId'), json_result)
    return json_result


@server.route('/save', methods=['POST'])
@token_required
def save(current_user):
    data_handler = request.get_json()
    public_id = current_user.get('publicId', None)
    global mongo_utils
    if mongo_utils is None:
        mongo_utils = app_utils.get_mongo_utils()
    mongo_utils.update_data(public_id, data_handler)
    return make_response(data_handler, 200)


@server.route('/download', methods=['POST'])
@token_required
def download(current_user):
    user_data = current_user.get('data', [])
    if not user_data:
        return make_response('Null File', 404)

    file_name = user_data[0].get('saveName', 'proto') + '.mid'
    path = os.path.join(os_dir, file_name)
    result = app_utils.from_json_to_score(user_data[0])
    result.write('midi', fp=path)
    return send_file(path, as_attachment=True)


@server.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.get_json()

    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    global mongo_utils
    if mongo_utils is None:
        mongo_utils = app_utils.get_mongo_utils()

    user = mongo_utils.get_record_by_username(auth.get('username'))

    if not user or not user.get('publicId', None):
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.get('password', ''), auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'publicId': user.get('publicId'),
            'exp': 	int(round((datetime.now() + timedelta(minutes=30)).timestamp() * 1000))
        }, server.config['SECRET_KEY'])

        return make_response(jsonify({
            'token': token.decode('UTF-8'),
            'name': user.get('name', ''),
            'data': user.get('data', [])}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        401,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@server.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.get_json()

    # gets name, email and password
    name, username = data.get('name', ''), data.get('username')
    password = data.get('password')

    # checking for existing user
    global mongo_utils
    if mongo_utils is None:
        mongo_utils = app_utils.get_mongo_utils()
    user = mongo_utils.get_record_by_username(username)

    if not user:
        # database ORM object
        user_record = {
            'publicId': str(uuid.uuid4()),
            'userName': username,
            'name': name,
            'password': generate_password_hash(password),
            'data': []
        }
        # insert user
        mongo_utils.insert_new_record(user_record)
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('UserName already exists. Please Log in.', 202)


if __name__ == '__main__':
    server.run()
