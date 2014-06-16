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

ka.config = {
    gridMaxRows: 3
  , gridMaxColumns: 7
  , gridSortOrder: 'byLetter'
  , gridKeys: {
        byLetter: ['123'].concat('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''))
    }
};

ka.state = {
    currentPageMode: 'grid'
  , gridFocusX: 0
  , gridFocusY: 0
  , gridPage: 0
  , gridTotalPages: 0
  , detachedGridCells: {}
  , gridLookupMatrix: {}
  , gridLookupItemsPerLine: []
  , gridLookupLinesByKey: {} // TODO: needed?
};


function boot() {
    ka.lib.registerShortcuts();

    $.ajax({
        url: '/movies/all',
        success: function (list) {
            var index = list.length;
            while (index--) {
                var movie = list[index];
                ka.lib.addMovieToCortex(list[index]);
            }
            ka.lib.recalcMovieGrid();
            ka.lib.updateMovieGrid();

            ka.state.socketDispatcher = new ka.lib.WebSocketDispatcher('wss://127.0.0.1:' + WEBSOCKET_PORT + '/');
            ka.state.socketDispatcher.bind('receive:movie:item', function (movie) {
                ka.lib.addMovieToCortex(movie);
                ka.lib.recalcMovieGrid();
                ka.lib.updateMovieGrid();
            });
        }
    });
}


document.oncontextmenu = function (event) {
    event.preventDefault();
};


$(document).ready(function () {
    ka.state.maxDetailButton = $('.boom-detail-button').length;

    /* Notify backend that UI is ready. */
    $.ajax({url: BOOT_TOKEN, type: 'PATCH', success: boot});

});
