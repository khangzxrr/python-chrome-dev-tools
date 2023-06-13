class KdpTab:
    def __init__(self, json):
        self.id = json['id']
        self.title = json['title']
        self.type = json['type']
        self.url = json['url']
        self.websocketDebuggerUrl = json['webSocketDebuggerUrl']