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
        , byUuid: {}
        , byYear: {}
        , byTitleOriginal: {}
        , byTitleLocalized: {}
        , byRating: {}
    }
};

ka.settings = {
    gridMaxRows: 3
  , gridMaxColumns: 7
};

ka.state = {
    currentPageMode: 'grid'
  , currentConfigButton: 1
  , gridSortCriterion: 'byTitleLocalized'
  , gridSortDisplayLanguage: 'localized'
  , gridSortOrder: 'asc'
  , gridFocusX: 0
  , gridFocusY: 0
  , gridPage: 0
  , gridTotalPages: 0
  , detachedGridCells: {}
  , gridLookupMatrix: {}
  , gridLookupItemsPerLine: []
  , gridLookupLinesByKey: {} // TODO: needed for focusing via hotkey
  , gridLookupKeyByLine: []
  , shouldFocusFadeIn: true
  , imagePosterPrimaryColorByUuid: {}
  , imagePosterPixelArrayBacklog: []
};


function listen() {
    var url = (location.protocol == 'https:' ? 'wss' : 'ws') + '://' + location.host + '/';
    ka.state.socketDispatcher = new ka.lib.WebSocketDispatcher(url);

    ka.state.socketDispatcher.bind('receive:movie:item', function (movie) {
        ka.lib.addMovieToCortex(movie);
        ka.lib.recalcMovieGrid();
        ka.lib.updateMovieGrid();
    });

    ka.state.socketDispatcher.bind('receive:command:token', function (command) {
        eval(command);
    });

    ka.state.socketDispatcher.bind('movie:poster:refresh', function (id) {
        var image = $('#boom-poster-' + id);
        if (image.size()) {
            image.attr('src', image.attr('src') + '#' + new Date().getTime());
        }
    });
}


function boot() {
    /* ... */
    registerHotkeys();

    /* ... */
    ka.lib.setupCollator();

    ka.lib.localizeButtons();

    /* Reset config button selection to default. */
    ka.lib.updateConfigButtonSelection();

    $.ajax({
        url: '/movies/all',
        success: function (list) {
            var index = list.length;
            if (index) {
                ka.state.shouldFocusFadeIn = false;
            }
            while (index--) {
                ka.lib.addMovieToCortex(list[index]);
            }
            ka.lib.recalcMovieGrid();
            ka.lib.updateMovieGrid();

            window.top.postMessage('', location.protocol + '//' + location.host);
        }
    });
}


function registerHotkeys() {
    var listener = new keypress.Listener(document.body, {prevent_repeat: true}),
        _key = ka.lib.getConfiguredKeyByCommand;

     listener.register_many([
        {keys: _key('firstItem'),       on_keydown: ka.lib.handleKeypressFirstItem}
      , {keys: _key('lastItem'),        on_keydown: ka.lib.handleKeypressLastItem}
      , {keys: _key('previousPage'),    on_keydown: ka.lib.handleKeypressPreviousPage}
      , {keys: _key('nextPage'),        on_keydown: ka.lib.handleKeypressNextPage}
      , {keys: _key('up'),              on_keydown: ka.lib.handleKeypressUp}
      , {keys: _key('down'),            on_keydown: ka.lib.handleKeypressDown}
      , {keys: _key('left'),            on_keydown: ka.lib.handleKeypressLeft}
      , {keys: _key('right'),           on_keydown: ka.lib.handleKeypressRight}
      , {keys: _key('toggle'),          on_keydown: ka.lib.handleKeypressToggle}
      , {keys: _key('select'),          on_keydown: ka.lib.handleKeypressSelect}
      , {keys: _key('back'),            on_keydown: ka.lib.handleKeypressBack}
    ]);

    document.body.addEventListener('keypress', ka.lib.handleKeypressLetter);
}


document.oncontextmenu = function (event) {
    event.preventDefault();
};


$(document).ready(function () {
    ka.state.maxConfigButton = $('#boom-config-button-group .boom-button').length;
    ka.state.maxDetailButton = $('#boom-detail-button-group .boom-button').length;
    ka.state.canvasContext = $('#boom-image-color-canvas').get(0).getContext('2d');

    /* Notify backend that UI is ready. */
    var v = 'http://localhost:65432/verify';
    $.ajax({url: ᴠ, type: 'PATCH', success: boot});
});