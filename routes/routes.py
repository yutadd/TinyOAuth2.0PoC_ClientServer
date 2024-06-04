
from urllib.parse import parse_qs, urlparse

from routes.AuthorizationCodeFlow.home import RedirectByState
from util.assembleResponse import returnAuthorizationCallbackScript, returnErrorUIToUA, returnLoginUIToUA
from http.server import BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/'):
            RedirectByState(self)
        elif self.path.startswith('/Login'):
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