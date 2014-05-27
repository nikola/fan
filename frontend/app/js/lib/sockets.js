/**
 *  WebSocket utility class.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

ka.lib.WebSocketDispatcher = function (url, undefined) {
    var callbacks = {};

    function dispatch(name, payload) {
        if (name in callbacks) {
            for (var chain = callbacks[name], c = 0; c < chain.length; c++) {
              chain[c](payload);
            }
        }
    }

    var connection = new WebSocket(url);

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
        dispatch('close',null)
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
