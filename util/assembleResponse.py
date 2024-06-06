from http.server import BaseHTTPRequestHandler
def returnLoginUIToUA(context: BaseHTTPRequestHandler):
    with open('template/login.html', 'r', encoding='utf-8') as file:
        content = file.read()
    context.send_response(200)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))
def returnLoggedinContent(context: BaseHTTPRequestHandler):
    context.send_response(200)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    # TODO:getPrivateContentFromResourceServer
    context.wfile.write(bytes("ログインしています", 'utf-8'))
    return
def returnErrorUIToUA(context: BaseHTTPRequestHandler,error:str,error_detail:str):
    with open('template/error.html', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('{{error}}', error)
    content = content.replace('{{error_detail}}', error_detail)
    context.send_response(400)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))
def returnWIPpage(context: BaseHTTPRequestHandler):
    with open('template/WIP.html', 'r', encoding='utf-8') as file:
        content = file.read()
    context.send_response(200)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))
def redirectToLoginPage(context: BaseHTTPRequestHandler):
    context.send_response(302)
    context.send_header('Location', '/login')
    context.end_headers()

def setClientSessionId(context:BaseHTTPRequestHandler,session_id:str):
    context.send_response(302)
    cookie = f"ClientServerSession_id={session_id}; HttpOnly; Path=/"
    context.send_header('Set-Cookie', cookie)
    context.send_header('Location', f'http://localhost/')
    context.end_headers()
