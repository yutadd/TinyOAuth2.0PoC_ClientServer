from http.server import BaseHTTPRequestHandler
import secrets
from urllib.parse import parse_qs, urlparse
import requests
from util.assembleResponse import returnErrorUIToUA, setClientSessionIdAndRedirect
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
            'grant_type': 'code',
            'code': code,
        }
        headers = {'Content-Type': 'application/x-www-urlencoded',
            'Authorization': f'Basic {b64encode("123abcABC:client_P@ssw0rd".encode()).decode()}'}
        try:
            response = requests.post(
                url="http://localhost:8081/act/exchangeToken", headers=headers, data=data_payload)
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
            print(responsedObject)
            if "error" not in responsedObject:
                resource_server_url = "http://localhost:8082/get/resource"
                resource_headers = {
                    'Authorization': f'Bearer {responsedObject["access_token"]}'
                }
                resource_response = requests.get(resource_server_url, headers=resource_headers)
                
                if resource_response.status_code == 200:
                    resource_data = resource_response.json()
                    print("Resource data retrieved successfully:", resource_data)
                    session_id = secrets.token_hex(16)
                    print("[routes/authorization/getacc]session_generated.")
                    register_user(
                    token=responsedObject["access_token"],
                    tokentype=responsedObject["token_type"],
                    token_expires_in=responsedObject["token_expires_in"],
                    refresh_expires_in=responsedObject["refresh_expires_in"],
                    refresh_token=responsedObject["refresh_token"],
                    scope=responsedObject["scope"],
                    sessionID=session_id,
                    username=resource_data["username"]
                    )
                    print("[routes/authorization/getacc]registered_user")
                    setClientSessionIdAndRedirect(context, session_id)
                else:
                    print("Failed to retrieve resource data:", resource_response.status_code, resource_response.text)
                
        except Exception as e:
            print("error catched at [route/catched authorization/getacc]")
            
            returnErrorUIToUA(context, "no response",
                "Requesting accesstoken failed.")
            print(e)
