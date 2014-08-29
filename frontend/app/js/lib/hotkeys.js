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
            ka.lib.updateConfigButtonSelection();
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
    }
};


ka.lib.handleKeypressRight = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.moveFocusRight();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.moveCompilationFocusRight();
    } else if (ka.state.currentPageMode == 'config') {
        ka.lib.closeMenu();
    }
};


ka.lib.handleKeypressToggle = function () {
    if (ka.state.currentPageMode == 'grid') {
        ka.lib.toggleGridFocus();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.toggleCompilationFocus();
    }
};


ka.lib.handleKeypressSelect = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.lib.executeConfigSelection();
    } else if (ka.state.currentPageMode == 'grid') {
        ka.lib.selectGridFocus();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.lib.selectCompilationFocus();
    } else if (ka.state.currentPageMode == 'detail') {
        if (ka.state.currentDetailButton == 'play') {
            $('#boom-movie-grid-container').css('display', 'none');
            $('#boom-movie-detail').velocity('fadeOut', {duration: 360, complete: function () {
                ka.state.currentPageMode = 'play:movie';

                if (!ka.state.isPlayerUpdated) {
                    $('#boom-playback-wait').velocity('fadeIn', {display: 'flex', duration: 360, complete: function () {
                        ka.state.socketDispatcher.push('movie:play', ka.state.currentGridMovieUuid);
                    }});
                } else {
                    ka.state.socketDispatcher.push('movie:play', ka.state.currentGridMovieUuid);
                }
            }});
        } else if (ka.state.currentDetailButton == 'trailer') {
            $('#boom-movie-grid-container').css('display', 'none');
            $('#boom-movie-detail').velocity('fadeOut', {duration: 360, complete: function () {
                ka.state.currentPageMode = 'play:trailer';

                ka.lib.startTrailerPlayer(ka.data.byUuid[ka.state.currentGridMovieUuid].trailer);
            }});
        }
    }
};


ka.lib.handleKeypressBack = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.lib.closeMenu();
    } else if (ka.state.currentPageMode == 'detail') {
        if (ka.state.currentCompilationPosterCount) {
            ka.state.currentPageMode = 'grid-compilation';

            $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail').velocity({translateZ: 0, left: '+=1920'}, 720);
        } else {
            ka.state.currentPageMode = 'grid';

            $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({translateZ: 0, left: '+=1920'}, {duration: 720, complete: function () {
                ka.lib.expandScrollableGrid();

                ka.lib.recalcMovieGrid();

                ka.lib.updateMovieGrid();
            }});
        }
    } else if (ka.state.currentPageMode == 'grid') {
        ka.state.currentPageMode = 'config';

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({translateZ: 0, left: '+=780', opacity: '-=0.5'}, 360);
        $('#boom-poster-focus').velocity({translateZ: 0, left: '+=780', opacity: '-=1'}, 360);
        $('#boom-movie-config').velocity({translateZ: 0, left: '+=780'}, {duration: 360});

        ka.lib.desaturateVisiblePosters();
    } else if (ka.state.currentPageMode == 'grid-compilation') {
        ka.state.currentPageMode = 'grid';

        ka.lib.zoomInGridPage(function () {
            ka.lib.expandScrollableGrid();

            ka.lib.recalcMovieGrid();

            ka.lib.updateMovieGrid();
        });
    } else if (ka.state.currentPageMode == 'play:trailer') {
        ka.lib.closeTrailerPlayer();
    } else if (ka.state.currentPageMode == 'credits') {
        ka.state.licenseTextIndex = -1;
        $('#boom-credit-text').stop();
    }
};


ka.lib.handleKeypressLetter = function (evt) {
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
                }, {duration: 360}).velocity('reverse');
            } else {
                $('#boom-movie-grid-container').velocity('callout.shake');
            }
        } else if (/^[0-9]$/.test(character)) {

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
