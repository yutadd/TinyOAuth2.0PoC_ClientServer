from http.server import BaseHTTPRequestHandler
def returnLoginUIToUA(context: BaseHTTPRequestHandler,query_components: dict[str, list[str]]):
    with open('template/login.html', 'r', encoding='utf-8') as file:
        content = file.read()
    # パラメータをHTMLに埋め込む
    context.send_response(200)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))

def returnErrorUIToUA(context: BaseHTTPRequestHandler,error:str,error_detail:str):
    with open('template/error.html', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('{{error}}', error)
    content = content.replace('{{error_detail}}', error_detail)
    context.send_response(400)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))
def returnReceiveParamClient(context: BaseHTTPRequestHandler):
    with open('template/error.html', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('{{error}}', error)
    content = content.replace('{{error_detail}}', error_detail)
    context.send_response(400)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))