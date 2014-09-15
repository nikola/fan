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
            ka.lib.updateMenuButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'detail') {
        if ($('#boom-detail-button-group .boom-button:visible.boom-active').index('#boom-detail-button-group .boom-button:visible') > 0) {
            ka.state.currentDetailButton = $('#boom-detail-button-group .boom-button.boom-active').prevAll(':visible').eq(0).text().toLowerCase();

            ka.lib.updateDetailButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusUp();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.moveCompilationFocusUp();
    }
};


ka.lib.handleKeypressDown = function () {
    if (ka.state.currentPageMode == 'config') {
        if (ka.state.currentConfigButton + 1 < ka.state.maxConfigButton) {
            ka.state.currentConfigButton += 1;
            ka.lib.updateMenuButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'detail') {
        if ($('#boom-detail-button-group .boom-button:visible.boom-active').index('#boom-detail-button-group .boom-button:visible') + 1 < $('#boom-detail-button-group .boom-button:visible').size()) {
            ka.state.currentDetailButton = $('#boom-detail-button-group .boom-button.boom-active').nextAll(':visible').eq(0).text().toLowerCase();
            ka.lib.updateDetailButtonSelection();
        }
    } else if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusDown();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.moveCompilationFocusDown();
    }
};


ka.lib.handleKeypressLeft = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusLeft();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.moveCompilationFocusLeft();
    } else if (ka.state.currentPageMode == 'detail-browser') {
        ka.lib.moveDetailBrowserLeft();
    }
};


ka.lib.handleKeypressRight = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusRight();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.moveCompilationFocusRight();
    } else if (ka.state.currentPageMode == 'config') {
        ka.transition.menu.to.grid();
    } else if (ka.state.currentPageMode == 'detail-browser') {
        ka.lib.moveDetailBrowserRight();
    }
};


ka.lib.handleKeypressToggle = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.toggleGridFocus();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.toggleCompilationFocus();
    } else if (ka.state.currentPageMode == 'detail') {
        ka.transition.detail.to.browser();
    } else if (ka.state.currentPageMode == 'detail-browser') {
        ka.transition.browser.to.detail();
    }
};


ka.lib.handleKeypressSelect = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.lib.executeMenuSelection();
    } else if (ka.state.currentPageMode == 'grid') {
        if (ka.lib.isCompilationAtFocus()) {
            ka.transition.grid.to.compilation();
        } else {
            ka.transition.grid.to.detail();
        }
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.transition.compilation.to.detail();
    } else if (ka.state.currentPageMode == 'detail') {
        if (ka.state.currentDetailButton == 'play') {
            $('#boom-movie-grid-container').css('display', 'none');
            $('#boom-movie-detail').velocity('fadeOut', {duration: ka.settings.durationNormal, complete: function () {
                ka.state.currentPageMode = 'play:movie';

                if (!ka.state.isPlayerUpdated) {
                    $('#boom-playback-wait').velocity('fadeIn', {display: 'flex', duration: ka.settings.durationNormal, complete: function () {
                        ka.state.socketDispatcher.push('movie:play', ka.state.currentGridMovieUuid);
                    }});
                } else {
                    ka.state.socketDispatcher.push('movie:play', ka.state.currentGridMovieUuid);
                }
            }});
        } else if (ka.state.currentDetailButton == 'trailer') {
            $('#boom-movie-grid-container').css('display', 'none');
            $('#boom-movie-detail').velocity('fadeOut', {duration: ka.settings.durationNormal, complete: function () {
                ka.state.currentPageMode = 'play:trailer';

                ka.lib.startTrailerPlayer(ka.data.byUuid[ka.state.currentGridMovieUuid].trailer);
            }});
        }
    } else if (ka.state.currentPageMode == 'detail-browser') {
        ka.transition.browser.to.detail();
    }
};


ka.lib.handleKeypressBack = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.transition.menu.to.grid();
    } else if (ka.state.currentPageMode == 'detail') {
        ka.lib.transitionBackFromDetailScreen();
        /* if (ka.state.currentCompilationPosterCount > 0) {
            ka.transition.detail.to.compilation();
        } else {
            ka.transition.detail.to.grid();
        } */
    } else if (ka.state.currentPageMode == 'detail-browser') {
        ka.transition.browser.to.detail();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.transition.compilation.to.grid();
    } else if (ka.state.currentPageMode == 'grid') {
        ka.transition.grid.to.menu();
    } else if (ka.state.currentPageMode == 'play:trailer') {
        ka.lib.closeTrailerPlayer();
    } else if (ka.state.currentPageMode == 'credits') {
        ka.state.licenseTextIndex = -1;
        $('#boom-credit-text').stop();
    }
};


ka.lib.handleKeypressAny = function (evt) {
    if (ka.state.currentPageMode != 'grid') {
        return;
    } else {
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
                    color: '#000000'
                  , backgroundColor: '#ffffff'
                  , borderColor: '#ffffff'
                }, ka.settings.durationNormal).velocity('reverse');
            } else {
                $('#boom-movie-grid-container').velocity('callout.shake');
            }
        } else if (/^[1-7]$/.test(character)) {
            ka.lib.moveFocusToIndex(character - 1);
        }
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
