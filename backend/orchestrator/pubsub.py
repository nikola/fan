# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import json

from pants.http import WebSocket

from settings import DEBUG

from . import SERVER_HEADERS


class PubSub(WebSocket):

    def __init__(self, queue, request, userAgent, bridgeToken, registerSelf, *args):
        self.queue = queue
        self.userAgent = userAgent
        self.bridgeToken = bridgeToken
        self.registerSelf = registerSelf

        super(PubSub, self).__init__(request)

    def on_handshake(self, request, headers=SERVER_HEADERS):
        return DEBUG or (request.protocol == 'HTTP/1.1' and request.headers.get('User-Agent', None) == self.userAgent)

    def on_connect(self, *args):
        self.ping()

    def on_pong(self, data):
        self.registerSelf(self)

    def on_read(self, data):
        command, payload = json.loads(data)
        if command == 'movie:play':
            self.queue.put('player:play:%s' % payload)
        elif command == 'loopback:command':
            self.write(unicode('["receive:command:token", "__%s__.%s()"]'% (self.bridgeToken, payload)))
        elif command == 'loopback:redirect':
            if payload == 'return':
                self.write(unicode('["force:redirect:url", "load.asp"]'))

    def on_close(self):
        pass
