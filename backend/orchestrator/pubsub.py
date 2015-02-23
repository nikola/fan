# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2015 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (C) 2013-2015 Nikola Klaric'

import simplejson as json
from pants.http import WebSocket


class PubSub(WebSocket):

    def __init__(self, request, queue, registerSelf, *args):
        self.queue = queue
        self.registerSelf = registerSelf

        super(PubSub, self).__init__(request)

    def on_handshake(self, request, headers):
        return request.protocol == 'HTTP/1.1'

    def on_connect(self, *args):
        self.ping()

    def on_pong(self, data):
        self.registerSelf(self)

    def on_read(self, data):
        command, payload = json.loads(data)

        if command == 'movie:play':
            self.queue.put('player:play:%s' % payload)
        elif command == 'loopback:redirect':
            if payload == 'return':
                self.write(unicode('["force:redirect:url", "load.html"]'))

    def on_close(self):
        pass
