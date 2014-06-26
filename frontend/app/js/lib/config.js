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
    /* if (ka.state.currentDetailButton > 0) {
        $('#boom-movie-detail-shade').velocity({opacity: 0.75}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandIn', {duration: 360, display: 'flex'});
    } else {
        $('#boom-movie-detail-shade').velocity({opacity: 0}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandOut', 360);
    } */
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
