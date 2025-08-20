from sanic import Sanic
from niquests import get
from sanic.response import HTTPResponse, empty, json, text, html
from traceback import format_exception
from sysconfig import get_path
from os import system
from subprocess import run
from sys import exit

import flower_optimizer.config


app = Sanic("FlowerOptimizer")

total_entrys = ['bjdata', 'gzdata', 'shdata']
auth_token = flower_optimizer.config.get('auth_token')
index_html = open('static/index.html', 'r', encoding='utf8').read()

@app.get('/sub')
async def sub(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    upstream = flower_optimizer.config.get('upstream')
    if upstream == "":
        return text('Upstream Misconfigured', status=503)
    try:
        resp = get(upstream)
    except Exception as exc:
        return text('Fetch Upstream Failed, Detail: \n\n' + '\n'.join(format_exception(exc)), status=500)
    data = resp.text
    entry = flower_optimizer.config.get('prefer_entry')
    if entry != 'default':
        if entry not in total_entrys:
            raise ValueError('Unknown Entry.')
        for current_entry in total_entrys:
            if current_entry != entry:
                data = data.replace(current_entry, entry)
    headers = dict(resp.headers)
    del headers['content-encoding']
    return text(data, resp.status_code, headers, resp.headers['Content-Type'])
    
@app.post('/config')
async def update_config(request):
    if "auth" not in request.args or auth_token != request.args["auth"][0]:
         return empty(status=403)
    if 'key' not in request.json or 'value' not in request.json:
        return empty(status=400)
    flower_optimizer.config.set(request.json["key"], request.json["value"])
    return empty()

@app.get('/config')
async def read_config(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    return json(flower_optimizer.config.config)

@app.get('/')
async def index(request):
    return html(index_html)
    #return html(open('static/index.html', 'r', encoding='utf8').read())
    
@app.get('/service')
async def service(request):
    return html(open('static/service.html', 'r', encoding='utf8').read())
    
@app.get('/ping')
async def ping(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    return text('pong')
    
@app.get('/service/install')
async def install_service(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    system('static\\install_service.bat ' + get_path('scripts') + '\\sanic.exe ' + '\\'.join(__file__.split('\\')[:-2]))
    exit(0)
    
@app.get('/service/uninstall')
async def uninstall_service(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    return text(str(system('static\\nssm.exe remove flower_optimizer')))
    
@app.get('/service/start')
async def start_service(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    system('static\\control_service.bat start')
    exit(0)
    
@app.get('/service/stop')
async def stop_service(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    return text(str(system('static\\control_service.bat stop')))
    
@app.get('/service/query')
async def query_service(request):
    if "auth" not in request.args:
        return text('Auth Token Missing', status = 401)
    if auth_token != request.args["auth"][0]:
        return text('Auth Token Incorrect', status=403)
    return text(run([__file__ + '\\..\\..\\static\\control_service.bat','queryex'], capture_output=True).stdout.decode('utf8'))
   
    