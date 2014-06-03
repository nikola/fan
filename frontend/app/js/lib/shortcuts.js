/**
 *  Process key shortcuts.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};


ka.lib.registerShortcuts = function () {

        var listener = new window.keypress.Listener();

    listener.register_combo({
        keys: 'enter'
      , on_keyup: function () {
            var pages = $('section'),
                notVisible = pages.not(pages.eq(ka.state.gridPage));
            notVisible.css('display', 'none');
            $('#content').css('-webkit-transform', 'translate3d(0, 0%, 0)');
            $('#content').velocity({left: '-=1920'}, 1000);
        }
    });

    listener.register_combo({
        keys: 'home'
      , on_keyup: function () {
            if (ka.state.gridPage > 0) {
                ka.state.gridPage = 0;
                ka.lib.scrollToPage(ka.state.gridPage);
            }
        }
    });

    listener.register_combo({
        keys: 'end'
      , on_keyup: function () {
            if (ka.state.gridPage + 1 < ka.state.gridTotalPages) {
                ka.state.gridPage = ka.state.gridTotalPages - 1;
                ka.lib.scrollToPage(ka.state.gridPage);
            }
        }
    });

    listener.register_combo({
        keys: 'pageup'
      , on_keyup: function () {
            if (ka.state.gridPage > 0) {
                ka.state.gridPage -= 1;
                ka.lib.scrollToPage(ka.state.gridPage);
            }
        }
    });

    listener.register_combo({
        keys: 'pagedown'
      , on_keyup: function () {
            if (ka.state.gridPage + 1 < ka.state.gridTotalPages) {
                ka.state.gridPage += 1;
                ka.lib.scrollToPage(ka.state.gridPage);
            }
        }
    });



    listener.register_combo({
        keys: 'up'
      , on_keydown: function () {
            var gridFocusAbsoluteY = ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY,
                notFirstRow = ka.state.gridFocusY > 0,
                notFirstPage = ka.state.gridPage > 0;

            if (notFirstRow || notFirstPage > 0) {
                if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1].length > ka.state.gridFocusX) { /* Focus can stay in same column. */
                    if (notFirstRow) {
                        ka.state.gridFocusY -= 1;
                        $('#boom-poster-focus').velocity({top: '-=360'}, {duration: 360});
                    } else {
                        ka.state.gridFocusY = ka.config.gridMaxRows - 1;
                        ka.state.gridPage -= 1;
                        $('#boom-poster-focus').velocity({top: '+=720'}, {duration: 720, easing: 'ease'});
                        ka.lib.scrollToPage(ka.state.gridPage);
                    }
                } else { /* Focus must drift to the left. */
                    var driftLeft = '-=' + (ka.state.gridFocusX - (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1].length - 1)) * 260;
                    ka.state.gridFocusX = ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1].length - 1;
                    if (notFirstRow) {
                        ka.state.gridFocusY -= 1;
                        $('#boom-poster-focus').velocity({top: '-=360', left: driftLeft}, {duration: 360});
                    } else {
                        ka.state.gridFocusY = ka.config.gridMaxRows - 1;
                        ka.state.gridPage -= 1;
                        $('#boom-poster-focus').velocity({top: '+=720', left: driftLeft}, {duration: 720, easing: 'easeOutSine'});
                        ka.lib.scrollToPage(ka.state.gridPage);
                    }
                }
            }
        }
    });

    listener.register_combo({
        keys: 'down'
      , on_keydown: function () {
            var gridFocusAbsoluteY = ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY,
                notLastRow = ka.state.gridFocusY + 1 < ka.config.gridMaxRows,
                notLastPage = ka.state.gridPage + 1 < ka.state.gridTotalPages;

            if (notLastRow || notLastPage) {
                if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1].length > ka.state.gridFocusX) {  /* Focus can stay in same column. */
                    if (notLastRow) {
                        ka.state.gridFocusY += 1;
                        $('#boom-poster-focus').velocity({top: '+=360'}, {duration: 360});
                    } else {
                        ka.state.gridFocusY = 0;
                        ka.state.gridPage += 1;
                        $('#boom-poster-focus').velocity({top: '-=720'}, {duration: 720, easing: 'ease'});
                        ka.lib.scrollToPage(ka.state.gridPage);
                    }
                } else { /* Focus must drift to the left. */
                    var driftLeft = '-=' + (ka.state.gridFocusX - (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1].length - 1)) * 260;
                    ka.state.gridFocusX = ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1].length - 1;
                    if (notLastRow) {
                        ka.state.gridFocusY += 1;
                        $('#boom-poster-focus').velocity({top: '+=360', left: driftLeft}, {duration: 360});
                    } else {
                        ka.state.gridFocusY = 0;
                        ka.state.gridPage += 1;
                        $('#boom-poster-focus').velocity({top: '-=720', left: driftLeft}, {duration: 720, easing: 'easeOutSine'});
                        ka.lib.scrollToPage(ka.state.gridPage);
                    }
                }
            }
        }
    });

    listener.register_combo({
        keys: 'left'
      , on_keydown: function () {
            if (ka.state.gridFocusX > 0) {
                ka.state.gridFocusX -= 1;

                $('#boom-poster-focus').css('display', 'block');

                $('#boom-poster-focus').velocity({left: '-=260'}, {
                    duration: 260
                });
            }
        }
    });

    listener.register_combo({
        keys: 'right'
      , on_keydown: function () {
            // console.log('page: ' + ka.state.gridPage)
            if (ka.state.gridFocusX < ka.config.gridMaxColumns - 1  && ka.state.gridLookupItemsPerLine[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY].length > ka.state.gridFocusX + 1) {
                ka.state.gridFocusX += 1;

                $('#boom-poster-focus').css('display', 'block');

                $('#boom-poster-focus').velocity({left: '+=260'}, {
                    duration: 260
                });
            }
        }
    });

    listener.register_combo({
        keys: 'space'
      , on_keydown: function () {
            var uuid = ka.state.gridLookupItemsPerLine[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY][ka.state.gridFocusX];
            $('#boom-poster-' + uuid).eq(0).closest('.boom-movie-grid-info-overlay').toggleClass('active');
        }
    });

};


