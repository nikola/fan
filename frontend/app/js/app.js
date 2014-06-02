/**
 *  Application loop.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {};

ka.data = {
    cortex: {
        all: new Cortex([])
        , byYear: new Cortex({})
        , byUuid: new Cortex({})
        , byLetter: new Cortex({})
    }
};
ka.data.cortex.all.on('update', ka.lib.refreshMovieGrid);

ka.config = {
    gridMaxRows: 3
  , gridMaxColumns: 7
};

ka.state = {
    gridFocusX: 0
  , gridFocusY: 0
  , gridPage: 0
};


function boot() {
    $.ajax({
        url: '/movies/all',
        success: function (list) {
            var index = list.length;
            while (index--) {
                ka.lib.addMovie(list[index]);
            }

            // ka.data.cortex.all.forEach(function (item, index) { console.log(item.titleOriginal.getValue(), '->', item.titleSortable.getValue())})
        }
    });

    var dispatcher = new ka.lib.WebSocketDispatcher('wss://127.0.0.1:' + WEBSOCKET_PORT + '/');
    dispatcher.bind('receive:movie:item', function (record) {
        /* $('<div>', {
            'text': record
        }).appendTo('body'); */
        // console.log(record)
        // http://image.tmdb.org/t/p/original/9gZZyQ8XStpUJBFU1ceU4xx1crv.jpg
        // http://image.tmdb.org/t/p/w130/qKkFk9HELmABpcPoc1HHZGIxQ5a.jpg
        $('<img>', {
            'src': 'https://127.0.0.1:' + HTTP_PORT + '/movie/poster/' + record + '.jpg/300' // record.replace('http:', 'https:').replace('/original/', '/w150/')
          , 'width': 300
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
