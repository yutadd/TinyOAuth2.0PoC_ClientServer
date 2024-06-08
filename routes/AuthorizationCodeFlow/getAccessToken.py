from http.server import BaseHTTPRequestHandler
import secrets
from urllib.parse import parse_qs, urlparse
import requests
from util.assembleResponse import returnErrorUIToUA, setClientSessionId
from base64 import b64encode

from util.db.user import register_user


def exchangeCodeToAccessToken(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    code = query_components.get("code", [None])[0]
    if code is None:
        returnErrorUIToUA(context=context, error="unknown error",
            error_detail="Authorization server not returned code. That's all we know")
    else:
        data_payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'success_redirect_url': 'http://localhost/token_success',
            'fail_redirect_url': 'http://localhost/token_fail',
        }
        headers = {'Content-Type': 'application/x-www-urlencoded',
            'Authorization': f'Basic {b64encode("1:password".encode()).decode()}'}
        try:
            response = requests.post(
                url="http://localhost:8080/act/exchangeToken", headers=headers, data=data_payload)
            '''{
            "access_token":"2YotnFZFEjr1zCsicMWpAA",
            "token_type":"example",
            "expires_in":3600,
            "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA",
            refresh_token TEXT NOT NULL,
            scope TEXT NOT NULL,
            session_id TEXT NOT NULL
            }'''
            responsedObject = response.json()
            if "error" not in responsedObject:
                session_id = secrets.token_hex(16)
                register_user(
                    token=responsedObject["access_token"],
                    tokentype=responsedObject["token_type"],
                    expires_in=responsedObject["expires_in"],
                    refresh_token=responsedObject["refresh_token"],
                    scope=responsedObject["scope"],
                    sessionID=session_id
                )
                setClientSessionId(context, session_id)
        except Exception as e:
            returnErrorUIToUA(context, "no response",
                "Requesting accesstoken failed.")
            print(e)
