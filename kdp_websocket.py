import threading
import websocket
import time

import asyncio

import json

class KdpWebsocket:
    is_connected = False

    command_response = {}

    def on_message(self, ws, message):

        jsonMessage = json.loads(message)

        print(jsonMessage)

        # if 'method' in jsonMessage and jsonMessage['method'] == 'Page.lifecycleEvent':
        #     if jsonMessage['params']['name'] == 'load':
        #         self.set_loading(True)
        #     elif jsonMessage['params']['name'] == 'networkIdle':
        #         self.set_loading(False)

        if 'id' in jsonMessage:

            response_future = self.command_response[jsonMessage['id']]

            self.event_loop.call_soon_threadsafe(response_future.set_result, jsonMessage) 
                
        # if  self.is_waiting_for_result() and ('id' in jsonMessage) and (jsonMessage['id'] == self.waiting_id):
        #     self.result = jsonMessage
        #     self.set_is_waiting_for_result(False)   
        

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print('connected and emit is connect future')

        self.event_loop.call_soon_threadsafe(self.is_connected_future.set_result, 'OK')

    async def connect(self, url):

        self.url = url

        self.event_loop = asyncio.get_event_loop()

        self.websocket = websocket.WebSocketApp(self.url,
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
        
        self.websocket_thread = threading.Thread(target=self.websocket.run_forever)
        self.websocket_thread.start()

        self.is_connected_future = self.event_loop.create_future()

        await self.is_connected_future

        print('initiated and connected to websocket')

    def close(self):
        self.websocket.close()

    async def send(self, requestJsonData):
        
        self.websocket.send(json.dumps(requestJsonData))

        
        self.command_response[requestJsonData['id']] = self.event_loop.create_future()
        command_future = self.command_response[requestJsonData['id']]

        await command_future

        response = command_future.result()

        self.command_response.pop(requestJsonData['id'])

        return response