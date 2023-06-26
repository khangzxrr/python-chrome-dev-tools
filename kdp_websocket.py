import threading
import websocket
import time

import asyncio

import json

class KdpWebsocket:
    is_connected = False

    command_response = {}
    event_response = None

    def on_message(self, ws, message):

        jsonMessage = json.loads(message)

        # print(jsonMessage)
        # print('\n')
        

        if 'method' in jsonMessage:
            print(jsonMessage)
            
            if jsonMessage['method'] == 'Page.frameStartedLoading':
                self.event_response = self.event_loop.create_future()

            if jsonMessage['method'] == 'Page.frameStoppedLoading':
                self.event_loop.call_soon_threadsafe(self.event_response.set_result, 'OK')


        if 'id' in jsonMessage:

            response_future = self.command_response[jsonMessage['id']]

            self.event_loop.call_soon_threadsafe(response_future.set_result, jsonMessage) 


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

    async def wait_for_navigate(self):

        if self.event_response == None:
            return
        
        await self.event_response        
        self.event_response = None

        print ('finish navigate')

    async def send(self, requestJsonData):
        
        self.websocket.send(json.dumps(requestJsonData))

        
        self.command_response[requestJsonData['id']] = self.event_loop.create_future()
        command_future = self.command_response[requestJsonData['id']]

        await command_future
        self.command_response.pop(requestJsonData['id'])
        response = command_future.result()

        await asyncio.sleep(0.5)

        await self.wait_for_navigate()

        if requestJsonData['method'] == 'Page.navigate':
            await asyncio.sleep(1)    

        

        return response