import json
import secrets
    
    
def _build_initial_config():
    auth_token = secrets.token_urlsafe()
    return {
        "auth_token": auth_token,
        "upstream": "",
        "prefer_entry": "default"
    }
    
try:
    config = json.load(open('config.json', 'r'))
except FileNotFoundError:
    config = _build_initial_config()
    json.dump(config, open('config.json', 'w'))
    
def get(key):
    return config[key]
    
def set(key, value):
    config[key] = value
    json.dump(config, open('config.json', 'w'))
