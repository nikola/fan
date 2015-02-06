/**
 *  fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
 *  Copyright (C) 2013-2015 Nikola Klaric.
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.

 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *
 *  @author Nikola Klaric (nikola@klaric.org)
 *  @copyright Copyright (C) 2013-2015 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.WebSocketDispatcher = function (url) {
    var connection = new WebSocket(url),
        callbacks = {};

    function dispatch(name, payload) {
        if (name in callbacks) {
            for (var chain = callbacks[name], c = 0; c < chain.length; c++) {
              chain[c](payload);
            }
        }
    }

    connection.onopen = function () {
        dispatch('open', null);
    };

    connection.onmessage = function (evt) {
        var data = JSON.parse(evt.data),
            name = data[0],
            payload = data[1];
        dispatch(name, payload);
    };

    connection.onclose = function () {
        dispatch('close', null);
    };

    this.bind = function (name, callback) {
        callbacks[name] = callbacks[name] || [];
        callbacks[name].push(callback);
        return this;
    };

    this.push = function (name, payload) {
        connection.send(JSON.stringify([name, payload]));
        return this;
    };
};
