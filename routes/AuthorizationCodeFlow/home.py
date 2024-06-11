from http.server import BaseHTTPRequestHandler

from util.db.user import get_user_by_sessionid
from util.assembleResponse import redirectToLoginPage, returnLoggedinContent
from http.cookies import SimpleCookie

def RedirectByState(context:BaseHTTPRequestHandler):
    if "Cookie" in context.headers:
        cookie = SimpleCookie(context.headers["Cookie"])
        if "ClientServerSession_id" in cookie:
            session_id=context.headers.get('Cookie', '').split('ClientServerSession_id=')[-1].split(';')[0]
            if get_user_by_sessionid(session_id):
                returnLoggedinContent(context,session_id=session_id)
                return
    redirectToLoginPage(context)
