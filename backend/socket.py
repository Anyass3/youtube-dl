
from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from starlette.routing import WebSocketRoute
from starlette.types import Message, Receive, Scope, Send
import json
import typing

from pydantic import BaseModel

from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.endpoints import WebSocketEndpoint


class SocketConnections:
    events: typing.Dict[str, typing.Dict]
    websockets: typing.List[WebSocket]
    downloads: []


socket_connections: typing.Dict[str, SocketConnections] = {}
# events: typing.Dict[str, typing.Dict] = {}


class Socket:

    def __init__(self, id: str, *args):
        self.id = id
        try:
            self.websockets = socket_connections[id]['websockets']
        except Exception as e:
            assert e
        # self.downloads = socket_connections[id]['downloads']

    def disconnect(self):
        try:
            [ws.close() for ws in self.websockets]
        except Exception as e:
            assert e

    async def on(self, event: str, func: typing.Callable):
        try:
            socket_connections[self.id]['events'][event] = func
        except Exception as e:
            assert e

    async def emit(self, event: str, *data):
        if event == 'download_start':
            print('download_start', self.websockets)
        try:
            [await ws.send_json({'event': event, 'data': data}) for ws in self.websockets]
        except Exception as e:
            if event == 'download_start':
                print('\n\tdownload_start error\n')
            assert e

    async def broadcast(self, event: str, *data):
        for id in socket_connections:
            try:
                [await ws.emit(event, *data) for ws in socket_connections[id]['websockets']]
            except Exception as e:
                assert e


class SocketRoute(WebSocketEndpoint):
    encoding = 'json'

    async def on_connect(self, websocket):
        await websocket.accept()
        await websocket.send_json({'event': 'ready', 'data': []})
        temp_id = uuid4().hex
        websocket.id = temp_id

        socket_connections[temp_id] = {
            'websockets': [websocket], 'events': {}, 'downloads': []}
        socket = Socket(temp_id)

        async def setSocket_id(socket_id):
            try:
                socket_connections[socket_id]['websockets'].append(
                    socket_connections[temp_id]['websockets'][0])

            except:
                socket_connections[socket_id] = socket_connections[temp_id]

            websocket.id = socket_id
            await socket.emit('connected', websocket.id, temp_id)
            socket_connections.__delitem__(temp_id)
        await socket.on('socket_id', setSocket_id)

    async def on_receive(self, websocket, payload):
        # print(payload)
        try:
            await socket_connections[websocket.id]['events'][payload['event']](*payload['data'])
        except Exception as E:
            print('ERRROR', E)
            assert(E)

    async def on_disconnect(self, websocket, close_code):
        websockets = socket_connections[websocket.id]['websockets']
        socket_connections[websocket.id]['websockets'].remove(websocket)
        # if len(websockets) == 1:
        #     socket_connections.__delitem__(websocket.id)
        # else:
        #     socket_connections[websocket.id]['websockets'].remove(websocket)


router = APIRouter(routes=[WebSocketRoute('/ws', SocketRoute)])


@router.get('/wss')
async def hey():
    return 'hello'

# async def websocket_endpoint(websocket: WebSocket):
#     socket = Socket(websocket)
#     await socket.connect()
# try:
#     while True:
#         data = await websocket.receive_text()
#         await socket.send_personal_message(f"You wrote: {data}")
#         await socket.broadcast(f"Client # says: {data}")
# except WebSocketDisconnect:
#     socket.disconnect()
#     await socket.broadcast(f"Client # left the chat")
