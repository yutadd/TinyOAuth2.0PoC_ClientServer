from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs, urlparse
from util.http import returnCallbackAnalyzer, returnErrorUIToUA, returnLoginUIToUA

HTTP_PORT=80
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/Login'):
            query_components = parse_qs(urlparse(self.path).query)
            returnLoginUIToUA(self,query_components)
        elif self.path.startswith('/callback'):
            returnCallbackAnalyzer(self)
        else:
            returnErrorUIToUA(self,"invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
    def do_POST(self):
        # クライアント側でクッキー処理はやる
        returnErrorUIToUA(self, "invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer,RequestHandler,HTTP_PORT)