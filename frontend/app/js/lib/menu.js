/**
 *  Render config page items.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.updateConfigButtonSelection = function () {
    $('#boom-config-button-group .boom-active').removeClass('boom-active').css('backgroundColor', 'transparent');
    var selected = $('#boom-config-button-group .boom-button').eq(ka.state.currentConfigButton);
    selected.addClass('boom-active').css('backgroundColor', selected.data('selectColor'));
};


ka.lib.executeConfigSelection = function () {
    var id = $('#boom-config-button-group .boom-button').eq(ka.state.currentConfigButton).attr('id');

    if (id == 'boom-config-button-exit') {
        ka.state.socketDispatcher.push('loopback:command', 'shutdown');
    } else if (id == 'boom-config-button-change-import') {
        window.top.location.href = '/configure.asp#return';
    } else {
        var lastCriterion = ka.state.gridSortCriterion, lastOrder = ka.state.gridSortOrder;

        if (id == 'boom-config-button-sort-title-original-asc') {
            ka.state.gridSortCriterion = 'byTitleOriginal';
            ka.state.gridSortDisplayLanguage = 'original';
            ka.state.gridSortOrder = 'asc';
        } else if (id == 'boom-config-button-sort-title-localized-asc') {
            ka.state.gridSortCriterion = 'byTitleLocalized';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'asc';
        } else if (id == 'boom-config-button-sort-year-desc') {
            ka.state.gridSortCriterion = 'byYear';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'desc';
        } else if (id == 'boom-config-button-sort-year-asc') {
            ka.state.gridSortCriterion = 'byYear';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'asc';
        } else if (id == 'boom-config-button-sort-rating-desc') {
            ka.state.gridSortCriterion = 'byRating';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'desc';
        }

        if (ka.state.gridSortCriterion != lastCriterion || ka.state.gridSortOrder != lastOrder) {
            var uuid = ka.lib.getMovieFromGridFocus().uuid;
            ka.lib.recalcMovieGrid();
            ka.lib.updateMovieGrid();

            var coordinates = ka.state.gridLookupCoordByUuid[uuid];
            ka.state.gridPage = Math.floor(coordinates[1] / ka.settings.gridMaxRows);
            ka.state.gridFocusX = coordinates[0];
            ka.state.gridFocusY = coordinates[1] % ka.settings.gridMaxRows;

            ka.lib.refocusGrid();
            $('#boom-poster-focus').velocity({translateZ: 0, left: '+=780'}, 0);
        }
    }
};


ka.lib.getConfiguredKeyByCommand = function (command) {
    return ka.config.hotkeys[command];
};


ka.lib.closeMenu = function () {
    ka.state.currentPageMode = 'grid';

    $('#boom-movie-grid-container, #boom-movie-detail').velocity({translateZ: 0, left: '-=780', opacity: '+=0.5'}, 360);
    $('#boom-poster-focus').velocity({translateZ: 0, left: '-=780', opacity: '+=1'}, 360);
    $('#boom-movie-config').velocity({translateZ: 0, left: '-=780'}, {duration: 360});

    ka.lib.undesaturateVisiblePosters();
};
