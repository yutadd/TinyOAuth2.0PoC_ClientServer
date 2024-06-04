from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs, urlparse
from util.http import returnAuthorizationCallbackScript, returnErrorUIToUA, returnLoginUIToUA

HTTP_PORT=80
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/Login'):
            query_components = parse_qs(urlparse(self.path).query)
            returnLoginUIToUA(self)
        elif self.path.startswith('/authorization_success'):
            returnAuthorizationCallbackScript(self)
        elif self.path.startswith('/authorization_fail'):
            query_components = parse_qs(urlparse(self.path).query)
            returnErrorUIToUA(context=self,error=query_components.get("error",[None]),error_detail=query_components.get('error_detail',[None]))
        # TODO:token用のエンドポイントの追加
        else:
            returnErrorUIToUA(self,"invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
    def do_POST(self):
        returnErrorUIToUA(self, "invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer,RequestHandler,HTTP_PORT)