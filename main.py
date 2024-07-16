import time
import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from functools import partial
import urllib.parse as urlparser


HOST_NAME = 'localhost'
PORT_NUMBER = 8000


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, server, *args, **kwargs):
        self._server = server
        super().__init__(*args, **kwargs)

    def do_GET(self):
        url = urlparser.urlparse(self.path)
        params = dict(urlparser.parse_qsl(url.query))
        response, content_type, data = self._server.serve(url.path, params)
        self.send_response(response)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(data)

class Server:
    def __init__(self):
        self._urls = [
            (r'^/display/?$', self.show_display_page),
            (r'^/admin/?$', self.show_admin_page),
            (r'^/update/?$', self.get_data_update),
        ]

    def serve_html_file(self, fname):
        with open(fname, "rb") as f:
            return 200, "text/html", f.read()

    def serve(self, path, params):
        for url in self._urls:
            if re.fullmatch(url[0], path):
                return url[1](params)
        return 404, None, b""

    def show_display_page(self, params):
        return self.serve_html_file("display.html")
    
    def show_admin_page(self, params):
        return 200, "text/html", b"<html><h2>Admin</h2></html>"

    def get_data_update(self, params):
        return 200, "application/json", bytes(json.dumps({"Hi": "JsonTest", "x": 7}), "utf-8")

if __name__ == '__main__':
    server = Server()
    handler = partial(MyHandler, server)
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), handler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    