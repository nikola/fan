/**
 *  Application loop.
 *
 *  @author Nikola Klaric (nikola@klaric.org)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

ka.data = {
    byId: {}
  , byYear: {}
  , byTitleOriginal: {}
  , byTitleLocalized: {}
  , byRating: {}
  , byBudget: {}
  , asList: []
  , indexById: {}
};

ka.settings = {
    gridMaxRows: 3
  , gridMaxColumns: 7
  , compilationPosterOffsetTop: -18
  , compilationPosterOffsetLeft: 12

  , durationUltraShort: 45
  , durationVeryShort: 90
  , durationShort: 180
  , durationNormal: 360
  , durationLong: 720
};

ka.state = {
    view: 'grid'
  , actualScreenMode: null

  , currentConfigButton: 1

  , lastGridMovieId: null
  , lastGridMovieListSnapshot: null
  , lastGridMovieIndexSnapshot: null

  , currentCompilationFocusIndex: null
  , currentCompilationPosterCount: 0
  , currentCompilationColumnSize: null

  , hasDeferredGridUpdate: false

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
  , gridLookupLinesByKey: {}
  , gridLookupKeyByLine: []
  , gridLookupCoordById: {}
  , shouldFocusFadeIn: true
  , imagePosterPrimaryColorById: {}
  , imagePosterPixelArrayBacklog: []
  , desaturationImageCache: {}
  , isProcessingInitialItems: false
  , processingInitialItemsCount: null
  , isPlayerUpdated: false
  , occludedGridItems: null

  , currentDetailBrowserPosterColumn: null
  , uncachedBackdropDelayTimer: null
  , detachedBrowserPosterByKey: {}

  , setOfKnownPosters: {}
  , setOfUnknownPosters: {}
};


function c4b77b2bcc804808a9ab107b8e2ac434() {
    var script = window.top.document.getElementsByTagName('script')[0];
    script.parentNode.removeChild(script);

    var url = (location.protocol == 'https:' ? 'wss' : 'ws') + '://' + location.host + '/';
    ka.state.socketDispatcher = new ka.lib.WebSocketDispatcher(url);

    ka.state.socketDispatcher.bind('receive:movie:item', function (movie) {
        ka.state.setOfUnknownPosters[movie.id] = true;

        ka.lib.addMovie(movie);

        ka.lib.updateMovieGridOnAdd(true); /* immediate mode */
    });

    ka.state.socketDispatcher.bind('receive:command:token', function (command) {
        eval(command);
    });

    ka.state.socketDispatcher.bind('resume:detail:screen', function () {
        $('#boom-movie-grid-container').css('display', 'block');
        $('#boom-movie-detail').velocity('fadeIn', {duration: ka.settings.durationNormal, complete: function () {
            ka.state.view = 'detail';
        }});
    });

    ka.state.socketDispatcher.bind('player:update:complete', function () {
        $('#boom-playback-wait').css('display', 'none');
        ka.state.isPlayerUpdated = true;
    });

    ka.state.socketDispatcher.bind('movie:poster:refresh', function (id) {
        $(".boom-movie-grid-image[src^='/movie/poster/" + id + "']").each(function () {
            $(this).attr('src', $(this).attr('src') + '#' + new Date().getTime());
        });
    });
}


function a4b4e7515096403cb29247517b276397() {
    var listener = ka.state.hotkeyListener = new keypress.Listener(document.body, {prevent_repeat: true}),
        _hotkeys = ka.config.hotkeys;

     listener.register_many([
        {keys: _hotkeys['firstItem'],       on_keydown: ka.lib.handleKeypressFirstItem}
      , {keys: _hotkeys['lastItem'],        on_keydown: ka.lib.handleKeypressLastItem}
      , {keys: _hotkeys['previousPage'],    on_keydown: ka.lib.handleKeypressPreviousPage}
      , {keys: _hotkeys['nextPage'],        on_keydown: ka.lib.handleKeypressNextPage}
      , {keys: _hotkeys['up'],              on_keydown: ka.lib.handleKeypressUp}
      , {keys: _hotkeys['down'],            on_keydown: ka.lib.handleKeypressDown}
      , {keys: _hotkeys['left'],            on_keydown: ka.lib.handleKeypressLeft}
      , {keys: _hotkeys['right'],           on_keydown: ka.lib.handleKeypressRight}
      , {keys: _hotkeys['toggle'],          on_keydown: ka.lib.handleKeypressToggle}
      , {keys: _hotkeys['select'],          on_keydown: ka.lib.handleKeypressSelect}
      , {keys: _hotkeys['back'],            on_keydown: ka.lib.handleKeypressBack}
    ]);

    listener.sequence_combo('up up down down left right left right b a', function() {
        /* TODO */
    }, true);

    document.body.addEventListener('keypress', ka.lib.handleKeypressAny);

    ka.lib.setupCollator();

    ka.lib.localizeButtons();

    /* Reset config button selection to default. */
    ka.lib.updateMenuButtonSelection();

    $.ajax({
        url: '/movies/all',
        success: function (list) {
            /* list = list.slice(0, 9); */

            var index = list.length, movie;
            if (index) {
                ka.state.shouldFocusFadeIn = false;
                ka.state.isProcessingInitialItems = true;
                ka.state.processingInitialItemsCount = index;

                while (index--) {
                    movie = list[index];
                    ka.state.setOfKnownPosters[movie.id] = true;
                    ka.lib.addMovie(movie);
                }
                ka.lib.recalcMovieGrid();
                ka.lib.updateMovieGridOnChange();
            } else {
                ed59df96be5e4cdc88fe356cd99c4ac6();
            }
        }
    });
}


function ed59df96be5e4cdc88fe356cd99c4ac6() {
    window.top.postMessage('', location.protocol + '//' + location.host);
}


/* Prevent all input events. */
document.oncontextmenu = document.onmousedown = document.onselectstart = function (evt) {
    evt.preventDefault();
};


window.onerror = function (message, filename, lineno, colno, error) {
    console.error(message);
};


/* Disable back button. */
window.history.pushState(null, null, 'c7b4165ce062400e90f943066564582a');
window.onpopstate = function () {
    window.history.pushState(null, null, 'c7b4165ce062400e90f943066564582a');
};


$(document).ready(function () {
    ka.state.maxConfigButton = $('#boom-menu .boom-button').length;
    ka.state.canvasContext = $('#boom-image-color-canvas').get(0).getContext('2d');
    /* console.log(ka.state.canvasContext.webkitBackingStorePixelRatio == 1);
    console.log(window.devicePixelRatio == 1); */

    $('#boom-movie-detail-poster-foreground').on('load', ka.lib.browser.backdrop.onLoaded);
    $('#boom-detail-poster-left').data('boom.isHidden', true).find(' img').on('load', ka.lib.browser.poster.onLoaded);

    $.get(
        'https://www.youtube.com/iframe_api'
      , null
      , function () {

        }
      , 'script'
    );

    var v = 'http://localhost:59741/verify';
    $.ajax({url: ᴠ, type: 'PATCH', success: a4b4e7515096403cb29247517b276397});
});
