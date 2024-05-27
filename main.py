from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from util.http import returnErrorUIToUA, returnLoginUIToUA, returnReceiveParamClient

HTTP_PORT=80
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/Login'):
            returnLoginUIToUA(self)
        else:
            returnErrorUIToUA(self,"invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
    def do_POST(self):
        # クライアント側でクッキー処理はやる
        if self.path.startswith('/callback'):
            returnReceiveParamClient(self)
        else:
            returnErrorUIToUA(self, "invalid_page", "The authorization server does not support obtaining an authorization code using this method."
        )
def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer,RequestHandler,HTTP_PORT)