from .init_apps import socketio
from flask_jwt_extended import decode_token
from jwt import ExpiredSignatureError, InvalidSignatureError
from flask import request, Request
from werkzeug.local import LocalProxy

request: Request

auth_users = {}

print("socketio_api")
@socketio.on('connect')
def test_connect():
    print("CONNECTED")
    socketio.emit('my response', {'data': 'Connected'})

@socketio.on('join')
def join(json_body):
    print("joined")
    print(json_body)
    decoded_token = None
    try:
        decoded_token = decode_token(json_body["access_token"])
    except (InvalidSignatureError, ExpiredSignatureError) as e:
        print("JWT Token expired or invalid:")
        print(e)
        return False

    print('request.sid')
    print(request.sid)
    auth_users[decoded_token["identity"]["user_id"]] = {'sid': request.sid, 'expires':decoded_token['exp']}
    print("auth_users:")
    print(auth_users)
    return True
    

