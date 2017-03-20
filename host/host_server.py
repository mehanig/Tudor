#!/usr/bin/env python

"""
Very simple HTTP server in python.

Usage::
    ./host_server.py 4263

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Start a record::
    curl -d "ACTION=START&PATH=./Tests.mp4" http://localhost/recorder

Stop a record::
    curl -d "ACTION=STOP&PATH=./Tests.mp4" http://localhost/recorder

Stop all ffmpeg processes::
    curl -d "ACTION=KILL_ALL&PATH=any" http://localhost/recorder

Look how many processes is running::
    curl http://localhost//monitoring

"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from ffmpeg_runner import FFmpegRunner


class HostService(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._set_headers()
            self.wfile.write(b"<html><body><h1>SRS, OK.</h1></body></html>")
        if self.path == "/monitoring":
            self._set_headers()
            data = "{data}".format(data=len(FFmpegRunner.proc_list))
            self.wfile.write(data.encode())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        if self.path == "/recorder":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            post_params = parse_qs(post_data.decode())
            if FFmpegRunner.is_correct(post_params):
                FFmpegRunner(post_params).act()
                self._set_headers()
                self.wfile.write(b"<html><body><h1>OK</h1></body></html>")


def run(server_class=HTTPServer, handler_class=HostService, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting Henry server on port ' + str(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
