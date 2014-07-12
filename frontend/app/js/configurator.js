/**
 *  Configurator screen.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {};

function registerHotkeys() {
    var listener = new keypress.Listener(document.body, {prevent_repeat: true}),
        _hotkeys = ka.config.hotkeys;

     listener.register_many([
        {keys: _hotkeys['firstItem'],       on_hotkeysdown: ka.lib.handleKeypressFirstItem}
      , {keys: _hotkeys['lastItem'],        on_hotkeysdown: ka.lib.handleKeypressLastItem}
      , {keys: _hotkeys['previousPage'],    on_hotkeysdown: ka.lib.handleKeypressPreviousPage}
      , {keys: _hotkeys['nextPage'],        on_hotkeysdown: ka.lib.handleKeypressNextPage}
      , {keys: _hotkeys['up'],              on_hotkeysdown: ka.lib.handleKeypressUp}
      , {keys: _hotkeys['down'],            on_hotkeysdown: ka.lib.handleKeypressDown}
      , {keys: _hotkeys['left'],            on_hotkeysdown: ka.lib.handleKeypressLeft}
      , {keys: _hotkeys['right'],           on_hotkeysdown: ka.lib.handleKeypressRight}
      , {keys: _hotkeys['toggle'],          on_hotkeysdown: ka.lib.handleKeypressToggle}
      , {keys: _hotkeys['select'],          on_hotkeysdown: ka.lib.handleKeypressSelect}
      , {keys: _hotkeys['back'],            on_hotkeysdown: ka.lib.handleKeypressBack}
    ]);

    document.body.addEventListener('keypress', ka.lib.handleKeypressLetter);
}


document.oncontextmenu = function (event) {
    event.preventDefault();
};


$(document).ready(function () {
    /* ... */
    registerHotkeys();

    $.ajax({
        url: '/movies/top250',
        success: function (list) {
            for (var index = 0; index < 10; index++) {
                $('<li>', {
                    text: list[index][0] + ' (' + list[index][1] + ')'
                }).appendTo('#boom-top250-list');
            }
        }
    });

    $.ajax({
        url: '/drives/mounted',
        success: function (list) {
            console.log(list);
            for (var index = 0; index < list.length; index++) {
                $('<li>', {
                    html: '<i class="fa fa-lg fa-square-o"></i> ' + list[index][1] + ' (' + list[index][0] + ':)'
                }).appendTo('#boom-drives-list');
            }
        }
    });
});