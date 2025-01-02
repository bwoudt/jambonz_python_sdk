import asyncio
import websockets
import json
import logging
from collections import defaultdict
from urllib.parse import urlparse

class Session:
    def __init__(self, websocket, msg, logger):
        self.websocket = websocket
        self.call_sid = msg['call_sid']
        self.b3 = msg.get('b3')
        self.logger = logger
        self.msgid = msg['msgid']
        self._acked = False
        self.payload = []
        self.data = msg.get('data', {})
        
        # Copy all data fields to session object
        for key, value in self.data.items():
            setattr(self, key, value)

    async def send(self, exec_immediate=True, reply=False):
        queue_command = not exec_immediate
        ack = reply or not self._acked
        
        msg = {
            "type": "ack" if ack else "command",
            **({"msgid": self.msgid} if ack else {}),
            **({"command": "redirect", "queueCommand": queue_command} if not ack else {}),
            **({"data": self.payload} if self.payload else {})
        }
        
        try:
            await self.websocket.send(json.dumps(msg))
            self.logger.debug(f"Sent message: {msg}")
        except Exception as err:
            self.logger.error(f"Error sending command: {err}")
        
        self._acked = True
        self.payload = []

    async def reply(self, exec_immediate=True):
        await self.send(exec_immediate=exec_immediate, reply=True)

    def add_verb(self, verb, payload):
        verb = verb.replace('_', ':')  # Convert gather_play to gather:play format
        self.payload.append({"verb": verb, **payload})
        return self

class JambonzWsClient:
    def __init__(self, url, logger=None):
        self.url = url
        self.logger = logger or logging.getLogger(__name__)
        self.sessions = {}

    async def connect(self):
        self.logger.info(f"Connecting to {self.url}")
        async with websockets.connect(self.url, subprotocols=["ws.jambonz.org"]) as websocket:
            await self.listen(websocket)

    async def listen(self, websocket):
        async for message in websocket:
            await self._on_message(websocket, message)

    async def _on_message(self, websocket, data):
        try:
            msg = json.loads(data)
            msg_type = msg.get('type')
            self.logger.info(f"Received message: {msg}")

            handler = getattr(self, f"_handle_{msg_type}", None)
            if handler:
                await handler(websocket, msg)
            else:
                self.logger.info(f"Unhandled message type: {msg_type}")
        except (ValueError, json.JSONDecodeError) as e:
            self.logger.error(f"Error processing message: {e}")

    async def _handle_session_new(self, websocket, msg):
        session = Session(websocket, msg, self.logger)
        self.sessions[msg['call_sid']] = session
        self.logger.info(f"New session started: {msg['call_sid']}")
        await session.send_ack()

    async def _handle_call_status(self, websocket, msg):
        self.logger.info(f"Call status update: {msg['call_sid']}, Status: {msg['data']['call_status']}")
        session = self.sessions.get(msg['call_sid'])
        if session:
            session.add_verb('call_status', msg['data'])
            await session.execute_verbs()

    async def _handle_verb_hook(self, websocket, msg):
        session = self.sessions.get(msg['call_sid'])
        if session:
            session.add_verb('verb:hook', msg['data'])
            await session.execute_verbs()

    async def _handle_final(self, websocket, msg):
        self.logger.info(f"Final event for session: {msg['call_sid']}, Data: {msg['data']}")
        if msg['data'].get('completion_reason') == 'rate_limit_exceeded':
            response = {"type": "say", "text": "You have exceeded the rate limit."}
        else:
            response = {"type": "say", "text": "Request processed successfully."}
        await websocket.send(json.dumps(response))

    async def _handle_error(self, websocket, msg):
        self.logger.error(f"Error in session {msg['call_sid']}: {msg['error']}")

    async def _handle_close(self, websocket, msg):
        self.logger.info(f"Session closed: {msg['call_sid']}")
        self.sessions.pop(msg['call_sid'], None)

    async def _send_ack(self, websocket, msgid):
        ack = {"type": "ack", "msgid": msgid}
        await websocket.send(json.dumps(ack))
        self.logger.info(f"Sent ACK for msgid: {msgid}")

    async def send_command(self, websocket, command, data):
        response = {"type": "command", "command": command, "data": data}
        await websocket.send(json.dumps(response))
        self.logger.info(f"Sent command: {command}, data: {data}")

class WsRouter:
    def __init__(self):
        self.routes = []

    def use(self, match, client=None):
        if client is None:
            client = match
            match = '*'
        self.routes.append({'match': match, 'client': client})
        return self

    def route(self, path):
        path = urlparse(path).path if isinstance(path, str) else path.path
        
        for route in self.routes:
            # Wildcard match
            if route['match'] == '*':
                return route['client']
            
            # Path matching logic
            url_chunks = [c for c in path.split('/') if c]
            match_chunks = [c for c in route['match'].split('/') if c]
            
            if len(url_chunks) >= len(match_chunks):
                matched = True
                for i in range(len(match_chunks)):
                    if url_chunks[i] != match_chunks[i]:
                        matched = False
                        break
                if matched:
                    return route['client']
        return None

class Client:
    def __init__(self, logger):
        self.logger = logger
        self.handlers = {}

    async def handle(self, websocket, path):
        async def message_handler(msg):
            try:
                data = json.loads(msg)
                msg_type = data.get('type')
                
                if msg_type == 'session:new' or msg_type == 'session:adulting':
                    session = Session(websocket, data, self.logger)
                    if 'session:new' in self.handlers:
                        await self.handlers['session:new'](session, path)
                    await session.reply()
                else:
                    self.logger.debug(f"Client: discarding msg type {msg_type}")
                
            except Exception as e:
                self.logger.error(f"Error handling message: {e}")

        self.handlers['message'] = message_handler
        try:
            async for message in websocket:
                await message_handler(message)
        except websockets.exceptions.ConnectionClosed:
            self.logger.info("WebSocket connection closed")

    def on(self, event, handler):
        self.handlers[event] = handler
