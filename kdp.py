import browsers
import requests


import json
import random

import kdp_tab
import kdp_websocket

class Kdp:
    port = '9222'
    host = 'http://localhost:' + port

    tabs = []
    websocket = None

    def make_endpoint(self,endpoint):
        return self.host + endpoint
    
    def get(self, endpoint):
        r = requests.get(self.make_endpoint(endpoint))
        return r.json()

    def get_tabs(self):
        tabs = self.get('/json/list')

        for tab in tabs:
            self.tabs.append(kdp_tab.KdpTab(tab))

    def send_command(self, command):

        command['id'] = random.randint(0, 10000)

        jCommand = json.dumps(command)
        return self.websocket.send(jCommand)

    def connect_to_tab(self, index):

        if index >= len(self.tabs):
            raise Exception('index >= tabs length')
        
        print('connect to tab id: ' + self.tabs[0].id)

        if (self.websocket != None):
            self.websocket.close()

        self.websocket = kdp_websocket.KdpWebsocket()
        self.websocket.connect(self.tabs[0].websocketDebuggerUrl)


    def navigate(self, url):
        return self.send_command({ 'method': 'Page.navigate', 'params': { 'url': url }})

    def find_element_by_id(self, id):
        rootNode = self.send_command({ 'method': 'DOM.getDocument', 'params': { 'depth': 0 } })

        print(rootNode)

        return self.send_command({ 'method': 'DOM.querySelector', 'params': { 'nodeId': rootNode['id'], 'selector': '#' + id}})

    def launch_chrome(self):
        browsers.launch('chrome', args=['-remote-debugging-port=' + self.port, '--remote-allow-origins=' + self.host])
        self.get_tabs()

        self.connect_to_tab(0)

        
