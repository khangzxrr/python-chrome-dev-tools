import threading
import websocket
import time

import rel

import json

class KdpWebsocket:
    is_connected = False
    is_waiting = False

    websocket_lock = threading.Lock()

    result_lock = threading.Lock()

    def is_waiting_for_result(self):
        self.result_lock.acquire()
        is_waiting = self.is_waiting
        self.result_lock.release()

        return is_waiting

    def set_is_waiting_for_result(self, is_waiting_for_result):
        self.result_lock.acquire()
        self.is_waiting = is_waiting_for_result
        self.result_lock.release()

    def set_is_connected(self, is_connected):
        self.websocket_lock.acquire()
        
        self.is_connected = is_connected
        
        self.websocket_lock.release()

    def on_message(self, ws, message):

        self.result = message
        self.set_is_waiting_for_result(False)
        

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def is_websocket_connected(self):
        self.websocket_lock.acquire()
        
        is_connected = self.is_connected

        self.websocket_lock.release()

        return is_connected

    def on_open(self, ws):
        self.set_is_connected(True)

        print('on open')


    def connect(self, url):

        self.url = url
        self.is_connected = False

        self.websocket = websocket.WebSocketApp(self.url,
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
        
        self.websocket_thread = threading.Thread(target=self.websocket.run_forever)
        self.websocket_thread.start()



        while not self.is_websocket_connected():
            time.sleep(0.1)

        print('initiated and connected to websocket')

    def close(self):
        self.websocket.close()

    def send(self, requestJsonData):
        self.set_is_waiting_for_result(True)
        self.websocket.send(requestJsonData)

# phai kiem tra ID tra ve
        while self.is_waiting_for_result():
            time.sleep(0.1)

        return json.loads(self.result) 