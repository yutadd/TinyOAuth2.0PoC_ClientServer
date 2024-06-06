from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests
from util.assembleResponse import returnErrorUIToUA
from base64 import b64encode

def getAccessTokenByCode(context:BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    code=query_components.get("code",[None])[0]
    if code is None:
        returnErrorUIToUA(context=context,error="unknown error",error_detail="Authorization server not returned code. That's all we know")
    else:
        data_payload={
            'grant_type':'authorization_code',
            'code':code,
            'success_redirect_url':'http://localhost/token_success',
            'fail_redirect_url':'http://localhost/token_fail',
            }
        headers={'Content-Type':'application/x-www-urlencoded',
            'Authorization':f'Basic {b64encode("1:password".encode()).decode()}'}
        response=requests.post(url="http://localhsot:8080/act/exchangeToken",headers=headers)
        '''{
        "access_token":"2YotnFZFEjr1zCsicMWpAA",
        "token_type":"example",
        "expires_in":3600,
        "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA",
        "example_parameter":"example_value"
        }'''
        responsedObject=response.json()
        # TODO:insert to DB