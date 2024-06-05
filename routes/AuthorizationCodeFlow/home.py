from http.server import BaseHTTPRequestHandler
from util.assembleResponse import redirectToLoginPage, returnLoggedinContent
from http.cookies import SimpleCookie

def RedirectByState(context:BaseHTTPRequestHandler):
    if "Cookie" in context.headers:
        cookie = SimpleCookie(context.headers["Cookie"])
        if "session_id" in cookie:
            # ここでセッションIDの検証を行う（例：データベースで確認）
            returnLoggedinContent(context)
    redirectToLoginPage(context)
