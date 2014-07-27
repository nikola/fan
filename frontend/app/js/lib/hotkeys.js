/**
 *  Process global hotkeys.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.handleKeypressFirstItem = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusFirstItem();

    }
};


ka.lib.handleKeypressLastItem = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusLastItem();
    }
};


ka.lib.handleKeypressPreviousPage = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusPageUp();

    }
};


ka.lib.handleKeypressNextPage = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusPageDown();
    }
};


ka.lib.handleKeypressUp = function () {
    if (ka.state.currentPageMode == 'config') {
        if (ka.state.currentConfigButton > 0) {
            ka.state.currentConfigButton -= 1;
            ka.lib.updateConfigButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'detail') {
        if (ka.state.currentDetailButton > 0) {
            ka.state.currentDetailButton -= 1;
            ka.lib.updateDetailButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusUp();
    }
};


ka.lib.handleKeypressDown = function () {
    if (ka.state.currentPageMode == 'config') {
        if (ka.state.currentConfigButton + 1 < ka.state.maxConfigButton) {
            ka.state.currentConfigButton += 1;
            ka.lib.updateConfigButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'detail') {
        if (ka.state.currentDetailButton + 1 < ka.state.maxDetailButton) {
            ka.state.currentDetailButton += 1;
            ka.lib.updateDetailButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusDown();
    }
};


ka.lib.handleKeypressLeft = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusLeft();
    }
};


ka.lib.handleKeypressRight = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusRight();
    } else if (ka.state.currentPageMode == 'config') {
        ka.lib.closeMenu();
    }
};


ka.lib.handleKeypressToggle = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.toggleFocus();
    }
};


ka.lib.handleKeypressSelect = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.lib.executeConfigSelection();
    } else if (ka.state.currentPageMode == 'grid') {
        ka.lib.selectFocus();
    } else if (ka.state.currentPageMode == 'detail') {
        if (ka.state.currentDetailButton == 0) {
            $('#boom-movie-detail').velocity('fadeOut', {duration: 360, complete: function () {
                ka.state.currentPageMode = 'play:movie';

                ka.state.socketDispatcher.push('movie:play', ka.lib.getMovieFromGridFocus().uuid);
            }});
        } else if (ka.state.currentDetailButton == 2) {
            $('#boom-movie-detail').velocity('fadeOut', {duration: 360, complete: function () {
                ka.state.currentPageMode = 'play:trailer';
                $('#boom-movie-trailer')
                    .css('display', 'block')
                    .attr('src', 'https://www.youtube.com/embed/' + ka.lib.getMovieFromGridFocus().trailer
                        + '?autoplay=1'
                        + '&autohide=1'
                        + '&controls=2'
                        + '&enablejsapi=1'
                        + '&hl=2'
                        + '&iv_load_policy=3'
                        + '&modestbranding=1'
                        + '&origin=127.0.0.1'
                        + '&rel=0'
                        + '&showinfo=0'
                    );
            }});
        }

    }
};


ka.lib.handleKeypressBack = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.lib.closeMenu();
    } else if (ka.state.currentPageMode == 'detail') {
        ka.state.currentPageMode = 'grid';

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({translateZ: 0, left: '+=1920'}, {duration: 720}); /* , complete: function () {
            ka.state.currentPageMode = 'grid';
        }}); */
    } else if (ka.state.currentPageMode == 'grid') {
        ka.state.currentPageMode = 'config';

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({translateZ: 0, left: '+=780', opacity: '-=0.5'}, 360);
        $('#boom-poster-focus').velocity({translateZ: 0, left: '+=780', opacity: '-=1'}, 360);
        $('#boom-movie-config').velocity({translateZ: 0, left: '+=780'}, {duration: 360}); /*, complete: function () {
            ka.state.currentPageMode = 'config';
        }}); */

        ka.lib.desaturateVisiblePosters();
    } else if (ka.state.currentPageMode == 'play:trailer') {
        ka.state.currentPageMode = 'detail';

        $('#boom-movie-trailer')
            .css('display', 'none')
            .removeAttr('src');

        $('#boom-movie-detail').velocity('fadeIn', 360);
    }
};


ka.lib.handleKeypressLetter = function (evt) {
    var character = String.fromCharCode(evt.keyCode);

    if (/^[a-z]$/i.test(character)) {
        var key = character.toUpperCase();
        if (key in ka.state.gridLookupLinesByKey) {
            var line = ka.state.gridLookupLinesByKey[key][0] % ka.settings.gridMaxRows;
            ka.state.gridPage = Math.floor(ka.state.gridLookupLinesByKey[key][0] / ka.settings.gridMaxRows);
            ka.state.gridFocusX = 0;
            ka.state.gridFocusY = line;

            ka.lib.refocusGrid();

            $('#boom-movie-grid-key-' + key).velocity({
                colorRed: 0, colorGreen: 0, colorBlue: 0
              , backgroundColorRed: 255, backgroundColorGreen: 255, backgroundColorBlue: 255
              , borderColorRed: 255, borderColorGreen: 255, borderColorBlue: 255
            }, {duration: 360}).velocity('reverse');
        } else {
            $('#boom-movie-grid-container').velocity('callout.shake');
        }
    } else if (/^[0-9]$/.test(character)) {

    }
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
