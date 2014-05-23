/**
 *  Application loop.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

function boot() {
    var dispatcher = new ka.lib.WebSocketDispatcher('wss://127.0.0.1:' + WEBSOCKET_PORT + '/');


            // console.log(navigator.userAgent);
            // var socket = new WebSocket('wss://127.0.0.1:' + WEBSOCKET_PORT + '/');

            /*
            $('<div>', {
                    // 'text': 'socket: ' + WEBSOCKET_PORT // socket
                'text': 'console: ' + console
                }).appendTo('body');
            */

            /*
            socket.onopen = function (evt) {
                // socket.send('test1');
                // socket.send('test2');
            };
            */

            // console.log(ka.lib.WebSocketDispatcher);
            // console.log(dispatcher);
            // return;

            dispatcher.bind('receive:movie:item', function (record) {
                $('<div>', {
                    'text': record
                }).appendTo('body');
            });

            /*
            socket.onmessage = function (evt) {
                // TODO: refactor in order to retrieve actual name of bridge every time
                bridge = window[evt.data];
                // bridge.shutdown();
                // console.log(bridge);
                $('<div>', {
                    'text': evt.data
                }).appendTo('body');

            };
            */
}

document.oncontextmenu = function (evt) {
    evt.preventDefault();
};

document.addEventListener('DOMContentLoaded', function(event) {
    /* Notify backend that UI is ready. */
    $.ajax({url: '/ready', type: 'PATCH', success: boot});

    /*
    setTimeout(function () {
        // todo: websocket.close()
        // https://developer.mozilla.org/en-US/docs/WebSockets/Writing_WebSocket_client_applications
        bridge.shutdown();
    }, 3000);
    */


    /*
    setTimeout(function () {
        $('#app-logo').animate({opacity: 0}, 500, 'linear');
        $('#app-info').animate({opacity: 0}, 500, 'linear');
        $('.spinner').animate({borderRadius: 0, padding: 0, width: '100%', height: '100%'}, 1000, 'linear');
        $('.spinner div').animate({marginLeft: 256, marginRight: 256, opacity: 0}, 1000, 'linear');
        $('.spinner .container').animate({marginTop: 512, opacity: 0}, 1000, 'linear', function () {

        });
    }, 3000); */
});
