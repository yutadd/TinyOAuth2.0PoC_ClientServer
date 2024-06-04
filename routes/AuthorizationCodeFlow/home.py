from http.server import BaseHTTPRequestHandler
from util.assembleResponse import redirectToLoginPage
from http.cookies import SimpleCookie

def RedirectByState(context:BaseHTTPRequestHandler):
    if "Cookie" in context.headers:
        cookie = SimpleCookie(context.headers["Cookie"])
        if "session_id" in cookie:
            # ここでセッションIDの検証を行う（例：データベースで確認）
            context.send_response(200)
            context.send_header('Content-Type', 'text/html; charset=utf-8')
            context.end_headers()
            context.wfile.write(bytes("ログインしています", 'utf-8'))
            return
    redirectToLoginPage(context)
