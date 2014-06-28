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
            ka.state.gridSortCriterion = 'byTitleLocalized';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'asc';
        }

        if (ka.state.gridSortCriterion != lastCriterion || ka.state.gridSortOrder != lastOrder) {
            ka.lib.recalcMovieGrid();
            ka.lib.updateMovieGrid();
        }
    }
};


ka.lib.getConfiguredKeyByCommand = function (command) {
    return {
        firstItem:      'home'
      , lastItem:       'end'
      , previousPage:   'pageup'
      , nextPage:       'pagedown'
      , up:             'up'
      , down:           'down'
      , left:           'left'
      , right:          'right'
      , toggle:         'space'
      , select:         'enter'
      , back:           'escape'
    }[command];

};
