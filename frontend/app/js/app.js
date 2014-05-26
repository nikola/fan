/**
 *  Application loop.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

function boot() {
    var dispatcher = new ka.lib.WebSocketDispatcher('wss://127.0.0.1:' + WEBSOCKET_PORT + '/');
    dispatcher.bind('receive:movie:item', function (record) {
        /* $('<div>', {
            'text': record
        }).appendTo('body'); */
        // console.log(record)
        // http://image.tmdb.org/t/p/original/9gZZyQ8XStpUJBFU1ceU4xx1crv.jpg
        // http://image.tmdb.org/t/p/w130/qKkFk9HELmABpcPoc1HHZGIxQ5a.jpg
        $('<img>', {
            'src': 'https://127.0.0.1:' + HTTP_PORT + '/movie/poster/' + record + '.jpg/150' // record.replace('http:', 'https:').replace('/original/', '/w150/')
          , 'width': 150
        }).appendTo('body');
    });
}

/* document.oncontextmenu = function (evt) {
    evt.preventDefault();
}; */

document.addEventListener('DOMContentLoaded', function(event) {
    /* Notify backend that UI is ready. */
    $.ajax({url: BOOT_TOKEN, type: 'PATCH', success: boot});

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
