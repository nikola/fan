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
// ka.data.cortex.all.on('update', ka.lib.refreshMovieGrid);

ka.config = {
    gridMaxRows: 3
  , gridMaxColumns: 7
  , gridSortOrder: 'byLetter'
  , gridKeys: {
        byLetter: ['123'].concat('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''))
    }
};

ka.state = {
    gridFocusX: 0
  , gridFocusY: 0
  , gridPage: 0
};


function boot() {
    ka.lib.registerShortcuts();

    $.ajax({
        url: '/movies/all',
        success: function (list) {
            var index = list.length;
            while (index--) {
                ka.lib.addMovieToCortex(list[index]);
            }
            ka.lib.recalcMovieGrid();
            ka.lib.redrawMovieGridFull();

            ka.state.socketDispatcher = new ka.lib.WebSocketDispatcher('wss://127.0.0.1:' + WEBSOCKET_PORT + '/');
            ka.state.socketDispatcher.bind('receive:movie:item', function (movie) {
                /* ka.lib.addMovieToCortex(movie);
                ka.lib.recalcMovieGrid();
                ka.lib.redrawMovieGridPartial() */
            });
        }
    });
}


document.oncontextmenu = function (event) {
    event.preventDefault();
};


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
