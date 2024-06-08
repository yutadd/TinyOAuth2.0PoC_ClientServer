
from urllib.parse import parse_qs, urlparse
from routes.AuthorizationCodeFlow.getAccessToken import exchangeCodeToAccessToken

from routes.AuthorizationCodeFlow.home import RedirectByState
from util.assembleResponse import returnErrorUIToUA, returnLoginUIToUA
from http.server import BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path.split('?')[0]
        path=path.split('#')[0]
        if path=='/':
            RedirectByState(self)
        elif path=='/login':
            query_components = parse_qs(urlparse(self.path).query)
            returnLoginUIToUA(self)
        elif path=='/authorization_success':
            exchangeCodeToAccessToken(self)
        elif path=='/authorization_fail':
            query_components = parse_qs(urlparse(self.path).query)
            returnErrorUIToUA(context=self,error=query_components.get("error",[None])[0],error_detail=query_components.get('error_detail',[None])[0])
        # TODO:token用のエンドポイントの追加
        else:
            returnErrorUIToUA(self,"invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
    def do_POST(self):
        returnErrorUIToUA(self, "invalid_page", "The authorization server does not support obtaining an authorization code using this method.")