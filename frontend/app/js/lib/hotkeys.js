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
        // ka.state.currentPageMode = 'play';

        ka.state.socketDispatcher.push('movie:play',
            ka.state.gridLookupMatrix[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY][ka.state.gridFocusX].uuid);
    }
};


ka.lib.handleKeypressBack = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.state.currentPageMode = 'grid';

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({left: '-=780', opacity: '+=0.5'}, 360);
        $('#boom-poster-focus').velocity({left: '-=780', opacity: '+=1'}, 360);
        $('#boom-movie-config').velocity({left: '-=780'}, 360);

        ka.lib.undesaturateVisiblePosters();
    } else if (ka.state.currentPageMode == 'detail') {
        ka.state.currentPageMode = 'grid';

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({left: '+=1920'}, 720);
    } else if (ka.state.currentPageMode == 'grid') {
        ka.state.currentPageMode = 'config';

        // ka.lib.updateConfigButtonSelection();

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({left: '+=780', opacity: '-=0.5'}, 360);
        $('#boom-poster-focus').velocity({left: '+=780', opacity: '-=1'}, 360);
        $('#boom-movie-config').velocity({left: '+=780'}, 360);

        ka.lib.desaturateVisiblePosters();
    }
};


ka.lib.handleKeypressLetter = function (evt) {
    var character = String.fromCharCode(evt.keyCode);
    if (/^[a-z]$/.test(character)) {
        // console.log(character);
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
