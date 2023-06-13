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

        return self.websocket.send(command)

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
    
    def get_document(self):
        document = self.send_command({ 'method': 'DOM.getDocument', 'params': { 'depth': -1 } })

        if 'error' in document:
            raise Exception('error getting document')
        
        return document['result']
    
    # def find_elements_by_xpath(self, xpath):
    #     result = self.send_command({ 'method': 'Runtime.evaluate', 'params': { 'expression': xpath}})

    #     if ('error' in result):
    #         raise Exception('Element is not found with xpath ' + xpath)
        
    #     return result['result']
    
    def find_all_element_by_selector(self, selector):
        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelectorAll', 'params': { 'nodeId': document['root']['nodeId'], 'selector': selector}})

        if ('error' in result):
            raise Exception('Element is not found with selector ' + selector)
        
        return result['result']

    def find_element_by_selector(self, selector):
        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelector', 'params': { 'nodeId': document['root']['nodeId'], 'selector': selector}})

        if ('error' in result):
            raise Exception('Element is not found with selector ' + selector)
        
        return result['result']

    def find_all_element_by_class_name(self, class_name):
        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelectorAll', 'params': { 'nodeId': document['root']['nodeId'], 'selector': '.' + class_name}})

        if ('error' in result):
            raise Exception('Element is not found with class name ' + class_name)
        
        return result['result']

    def find_element_by_class_name(self, class_name):
        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelector', 'params': { 'nodeId': document['root']['nodeId'], 'selector': '.' + class_name}})

        if ('error' in result):
            raise Exception('Element is not found with class name ' + class_name)
        
        return result['result']

    def find_all_element_by_id(self, id):

        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelectorAll', 'params': { 'nodeId': document['root']['nodeId'], 'selector': '#' + id}})

        if ('error' in result):
            raise Exception('Element is not found with id ' + id)
        
        return result['result']
    
    def find_element_by_id(self, id):

        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelector', 'params': { 'nodeId': document['root']['nodeId'], 'selector': '#' + id}})

        if ('error' in result):
            raise Exception('Element is not found with id ' + id)
        
        return result['result']
    
    def get_property(self, node, property_name):
        
        if 'nodeId' not in node:
            raise Exception('not found nodeId')
        
        result = self.send_command({ 'method': 'DOM.describeNode', 'params': { 'nodeId': node['nodeId'] }})

        return result['result']

    def launch_chrome(self):
        browsers.launch('chrome', args=['-remote-debugging-port=' + self.port, '--remote-allow-origins=' + self.host])
        self.get_tabs()

        self.connect_to_tab(0)

        
