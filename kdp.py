import browsers
import requests


import json
import random

import asyncio

import kdp_tab
import kdp_websocket

class Kdp:
    port = '9222'
    host = 'http://localhost:' + port 

    target = None
    websocket = None

    def make_endpoint(self,endpoint):
        return self.host + endpoint
    
    def get(self, endpoint):
        r = requests.get(self.make_endpoint(endpoint))
        return r.json()
    

    def get_tabs(self):
        tabs = self.get('/json/list')

        tab_list = []

        for tab in tabs:
            tab_list.append(kdp_tab.KdpTab(tab))

        return tab_list

    def send_command(self, command):
        
        if self.target is not None and 'sessionId' in self.target:
            command['sessionId'] = self.target['sessionId']

        command['id'] = random.randint(0, 10000)

        result = asyncio.get_event_loop().run_until_complete(self.websocket.send(command))
        return result
    
    def navigate(self,  url):
        self.send_command({   'method': 'Page.navigate', 'params': { 'url': url }})
        
    
    def attach_target(self, target):
        attachResult = self.send_command({ 'method': 'Target.attachToTarget', 'params': { 'targetId': target['targetId'], 'flatten': True}})
     
        return attachResult['result']
    
    def get_targets(self):
        return self.send_command({ 'method': 'Target.getTargets'})['result']['targetInfos']
    
    def get_current_window(self):
        return self.target
    
    def close(self):


        closeResult = self.send_command({ 'method': 'Target.closeTarget', 'params': { 'targetId': self.target['targetId']}})['result']
        
        self.target.pop('sessionId')

        return closeResult

    def get_document(self):
        document = self.send_command({ 'method': 'DOM.getDocument' })

        if 'error' in document:
            raise Exception('error getting document')
        
        return document['result']
    

    def seperate_nodes(self, nodes):
        return list(map(lambda nodeId: { 'nodeId': nodeId }, nodes['nodeIds']))
    
    def find_all_element_by_selector(self, selector):
        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelectorAll', 'params': { 'nodeId': document['root']['nodeId'], 'selector': selector}})

        if ('error' in result):
            raise Exception('Element is not found with selector ' + selector)
        
        return self.seperate_nodes(result['result'])
                              
    
    def find_all_element_by_xpath(self, xpath):
        document = self.get_document()
        search_result = self.send_command({ 'method': 'DOM.performSearch', 'params': { 'query': xpath }})

        result = self.send_command({ 'method': 'DOM.getSearchResults', 'params': { 'searchId': search_result['result']['searchId'], 'fromIndex': 0, 'toIndex': 1    }})

        return self.seperate_nodes(result['result'])
    
    def delete_all_cookies(self):
        return self.send_command({ 'method': 'Network.clearBrowserCookies', 'params': {}})
    
    def get_cookies(self):
        return self.send_command({ 'method': 'Network.getCookies', 'params': {}})['result']['cookies']
    
    def current_url(self):
        return self.send_command({ 'method': 'Runtime.evaluate', 'params': { 'expression': ' window.location.href'}})['result']['result']['value']
    
    def execute_script(self, script):
        return self.send_command({ 'method': 'Runtime.evaluate', 'params': { 'expression': script}})

    def click_by_css_selector(self, selector):

        expression = 'document.querySelector("%s").click()' % selector

        return self.send_command({ 'method': 'Runtime.evaluate', 'params': { 'expression': expression}})

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
        
        return self.seperate_nodes(result['result'])

    def find_element_by_class_name(self, class_name):
        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelector', 'params': { 'nodeId': document['root']['nodeId'], 'selector': '.' + class_name}})

        if ('error' in result):
            raise Exception('Element is not found with class name ' + class_name)
        
        return result['result']
    
    def find_element_by_id(self, id):

        document = self.get_document()
        result = self.send_command({ 'method': 'DOM.querySelector', 'params': { 'nodeId': document['root']['nodeId'], 'selector': '#' + id}})

        if ('error' in result):
            raise Exception('Element is not found with id ' + id)
        
        return result['result']
    
    def check_node_id(self, node):
        if 'nodeId' not in node:
            raise Exception('not found nodeId')
        
    def open_new_tab(self):
        self.send_command({ 'method': 'Target.createTarget', 'params': { 'url': ''}})
    
    def get_attribute(self, node, attribute_name):
        self.check_node_id(node)

        result = self.send_command({ 'method': 'DOM.getAttributes', 'params': { 'nodeId': node['nodeId']}})

        if attribute_name not in result['result']['attributes']:
            raise Exception('not found attribute name ' + attribute_name)

        index_of_attribute = result['result']['attributes'].index(attribute_name)
        return result['result']['attributes'][index_of_attribute + 1] 
    
    def describe_node(self, node):
        self.check_node_id(node)
        
        result = self.send_command({ 'method': 'DOM.describeNode', 'params': { 'nodeId': node['nodeId'] }})

        return result['result']
    
    def get_window_handles(self):
        result = self.send_command({ 'method': 'Target.getTargets'})

        return result['result']['targetInfos']
    
    def enable_features(self):
        self.send_command({ 'method': 'Page.enable', 'params': {}})

    def switch_to_window(self, target):

        attachResult = self.attach_target(target)

        self.target = target
        self.target['sessionId'] = attachResult['sessionId']

        self.enable_features()

    def get_window_for_current_target(self):
        return self.send_command({ 'method': 'Browser.getWindowForTarget', 'params': {}})['result']

    def maximize_window(self):

        window = self.get_window_for_current_target()
        print(self.send_command({ 'method': 'Browser.setWindowBounds', 'params': { 'windowId': window['windowId'], 'bounds': { 'windowState': 'maximized' }} }))
        

    def launch_chrome(self, *user_args):

        args = list(user_args)
        args.extend(['--remote-debugging-port=' + self.port, '--remote-allow-origins=' + self.host])
        
        browsers.launch('chrome', args=args)
        
        websocketUrl = self.get('/json/version')['webSocketDebuggerUrl']

        self.websocket = kdp_websocket.KdpWebsocket()


        asyncio.get_event_loop().run_until_complete(self.websocket.connect(websocketUrl))
        
        targets = self.get_targets()

        self.switch_to_window(targets[0])

        
