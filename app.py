import threading
import socket
import logging
import os
from http.server import HTTPServer
from prometheus_client import MetricsHandler
from flask import Flask, request, send_file

hostName = "0.0.0.0"
dir = './'
PROMETHEUS_PORT = 8000
CRAWL_PERIOD = 86400


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


@server.route('/generate',  methods=['POST'])
def generate():
    data_handler = request.get_json()
    return data_handler


@server.route('/save', methods=['POST'])
def save():
    data_handler = request.get_json()
    return data_handler


@server.route('/download/<path:filename>', methods=['POST'])
def download(filename):
    path = os.path.join(dir, filename)
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    server.run()
