/**
 *  Process global hotkeys.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.registerShortcuts = function () {

    var listener = new keypress.Listener();

    listener.register_combo({
        keys: 'home'
      , on_keyup: function () {
            if (ka.state.currentPageMode == 'grid') {
                if (ka.state.gridPage > 0) {
                    ka.state.gridPage = 0;
                    ka.lib.scrollToPage(ka.state.gridPage);
                    // ka.lib.updateDetailPage();
                }
            }
        }
    });

    listener.register_combo({
        keys: 'end'
      , on_keyup: function () {
            if (ka.state.currentPageMode == 'grid') {
                if (ka.state.gridPage + 1 < ka.state.gridTotalPages) {
                    ka.state.gridPage = ka.state.gridTotalPages - 1;
                    ka.lib.scrollToPage(ka.state.gridPage);
                    // ka.lib.updateDetailPage();
                }
            }
        }
    });

    listener.register_combo({
        keys: 'pageup'
      , on_keyup: function () {
            if (ka.state.currentPageMode == 'grid') {
                if (ka.state.gridPage > 0) {
                    ka.state.gridPage -= 1;
                    ka.lib.scrollToPage(ka.state.gridPage);
                    // ka.lib.updateDetailPage();
                }
            }
        }
    });

    listener.register_combo({
        keys: 'pagedown'
      , on_keyup: function () {
            if (ka.state.currentPageMode == 'grid') {
                if (ka.state.gridPage + 1 < ka.state.gridTotalPages) {
                    ka.state.gridPage += 1;
                    ka.lib.scrollToPage(ka.state.gridPage);
                    // ka.lib.updateDetailPage();
                }
            }
        }
    });



    listener.register_combo({
        keys: 'up'
      , on_keydown: function () {
            if (ka.state.currentPageMode == 'detail') {
                if (ka.state.currentDetailButton > 0) {
                    ka.state.currentDetailButton -= 1;
                    ka.lib.updateDetailButtonSelection();
                }
            } else if (ka.state.currentPageMode == 'grid') {
                var gridFocusAbsoluteY = ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY,
                    notFirstRow = ka.state.gridFocusY > 0,
                    notFirstPage = ka.state.gridPage > 0;

                if (notFirstRow || notFirstPage) {
                    if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1] > ka.state.gridFocusX) { /* Focus can stay in same column. */
                        if (notFirstRow) {
                            ka.state.gridFocusY -= 1;
                            $('#boom-poster-focus').velocity({top: '-=360'}, {duration: 360});
                        } else {
                            ka.state.gridFocusY = ka.config.gridMaxRows - 1;
                            ka.state.gridPage -= 1;
                            $('#boom-poster-focus').velocity({top: '+=720'}, {duration: 720, easing: 'ease-out'});
                            ka.lib.scrollToPage(ka.state.gridPage);
                        }
                    } else { /* Focus must drift to the left. */
                        var driftLeft = '-=' + (ka.state.gridFocusX - (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1] - 1)) * 260;
                        ka.state.gridFocusX = ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1] - 1;
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
                    // ka.lib.updateDetailPage();
                }
            }
        }
    });

    listener.register_combo({
        keys: 'down'
      , on_keydown: function () {
            if (ka.state.currentPageMode == 'detail') {
                if (ka.state.currentDetailButton + 1 < ka.state.maxDetailButton) {
                    ka.state.currentDetailButton += 1;
                    ka.lib.updateDetailButtonSelection();
                }
            } else if (ka.state.currentPageMode == 'grid') {
                var gridFocusAbsoluteY = ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY,
                    notLastRow = ka.state.gridFocusY + 1 < ka.config.gridMaxRows,
                    notLastPage = ka.state.gridPage + 1 < ka.state.gridTotalPages;

                if (notLastRow || notLastPage) {
                    if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1] > ka.state.gridFocusX) {  /* Focus can stay in same column. */
                        if (notLastRow) {
                            ka.state.gridFocusY += 1;
                            $('#boom-poster-focus').velocity({top: '+=360'}, {duration: 360});
                        } else {
                            ka.state.gridFocusY = 0;
                            ka.state.gridPage += 1;
                            $('#boom-poster-focus').velocity({top: '-=720'}, {duration: 720, easing: 'ease-out'});
                            ka.lib.scrollToPage(ka.state.gridPage);
                        }
                    } else { /* Focus must drift to the left. */
                        var driftLeft = '-=' + (ka.state.gridFocusX - (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1] - 1)) * 260;
                        ka.state.gridFocusX = ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1] - 1;
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
                // ka.lib.updateDetailPage();
            }
        }
    });

    listener.register_combo({
        keys: 'left'
      , on_keydown: function () {
            if (ka.state.currentPageMode == 'grid') {
                if (ka.state.gridFocusX > 0) {
                    ka.state.gridFocusX -= 1;

                    $('#boom-poster-focus').css('display', 'block');

                    $('#boom-poster-focus').velocity({left: '-=260'}, {
                        duration: 260
                    });
                    // ka.lib.updateDetailPage();
                }
            }
        }
    });

    listener.register_combo({
        keys: 'right'
      , on_keydown: function () {
            if (ka.state.currentPageMode == 'grid') {
                if (ka.state.gridFocusX < ka.config.gridMaxColumns - 1 && ka.state.gridLookupItemsPerLine[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY] > ka.state.gridFocusX + 1) {
                    ka.state.gridFocusX += 1;

                    $('#boom-poster-focus').css('display', 'block');

                    $('#boom-poster-focus').velocity({left: '+=260'}, {
                        duration: 260
                    });
                    // ka.lib.updateDetailPage();
                }
            }
        }
    });

    listener.register_combo({
        keys: 'space'
      , on_keydown: function () {
            if (ka.state.currentPageMode == 'grid') {
                var uuid = ka.state.gridLookupMatrix[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY][ka.state.gridFocusX].uuid;
                $('#boom-poster-' + uuid).eq(0).closest('.boom-movie-grid-info-overlay').toggleClass('active');
            }
        }
    });

    listener.register_combo({
        keys: 'enter'
      , on_keyup: function () {
            if (ka.state.currentPageMode == 'grid') {
                ka.state.currentPageMode = 'detail';
                ka.state.currentDetailButton = 0;

                ka.lib.updateDetailPage();
                ka.lib.updateDetailButtonSelection();

                $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({left: '-=1920'}, 720);
            } else if (ka.state.currentPageMode == 'detail') {
                ka.state.socketDispatcher.push('movie:play',
                    ka.state.gridLookupMatrix[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY][ka.state.gridFocusX].uuid);
            }
        }
    });

    listener.register_combo({
        keys: 'escape'
      , on_keyup: function () {
            if (ka.state.currentPageMode == 'detail') {
                ka.state.currentPageMode = 'grid';
                $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({left: '+=1920'}, 720);
            }
        }
    });

};

/*
		el.swipeEvents().bind("swipeDown",  function(event){
			event.preventDefault();
			el.moveUp();
		}).bind("swipeUp", function(event){
			event.preventDefault();
			el.moveDown();
		});

		$(window).bind('mousewheel DOMMouseScroll', function(event) {
			event.preventDefault();
			var delta = event.originalEvent.wheelDelta || -event.originalEvent.detail;
			// init_scroll(event, delta);
            var deltaOfInterest = delta,
				timeNow = new Date().getTime();
			// Cancel scroll if currently animating or within quiet period
			if(timeNow - lastAnimation < quietPeriod + settings.animationTime) {
				event.preventDefault();
				return;
			}

			if (deltaOfInterest < 0) {
				el.moveDown()
			} else {
				el.moveUp()
			}
			lastAnimation = timeNow;
		});


		return false;
*/
