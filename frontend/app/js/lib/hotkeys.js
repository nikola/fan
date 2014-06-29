/**
 *  Process global hotkeys.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.handleKeypressFirstItem = function () {
    if (ka.state.currentPageMode == 'grid') {
        if (ka.state.gridFocusX > 0) {
            var distance = 260 * ka.state.gridFocusX;
            ka.state.gridFocusX = 0;

            $('#boom-poster-focus').css('display', 'block');

            $('#boom-poster-focus').velocity({left: '-=' + distance}, {
                duration: 260
            });
        }
    }
};


ka.lib.handleKeypressLastItem = function () {
    if (ka.state.currentPageMode == 'grid') {
        var items = ka.state.gridLookupItemsPerLine[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY];
        if (ka.state.gridFocusX < items - 1) {
            var distance = 260 * (items - ka.state.gridFocusX - 1);
            ka.state.gridFocusX = items - 1;

            $('#boom-poster-focus').css('display', 'block');

            $('#boom-poster-focus').velocity({left: '+=' + distance}, {
                duration: 260
            });
        }
    }
};


ka.lib.handleKeypressPreviousPage = function () {
    if (ka.state.currentPageMode == 'grid') {
        if (ka.state.gridPage > 0) {
            ka.state.gridPage -= 1;
            ka.lib.scrollToPage(ka.state.gridPage);
            // ka.lib.updateDetailPage();
        }
    }
};


ka.lib.handleKeypressNextPage = function () {
    if (ka.state.currentPageMode == 'grid') {
        if (ka.state.gridPage + 1 < ka.state.gridTotalPages) {
            ka.state.gridPage += 1;
            ka.lib.scrollToPage(ka.state.gridPage);
            // ka.lib.updateDetailPage();
        }
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
};


ka.lib.handleKeypressLeft = function () {
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
};


ka.lib.handleKeypressRight = function () {
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
};


ka.lib.handleKeypressToggle = function () {
    if (ka.state.currentPageMode == 'grid') {
        var uuid = ka.state.gridLookupMatrix[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY][ka.state.gridFocusX].uuid;

        $('#boom-movie-grid-item-' + uuid)
            .toggleClass('active')
            .find('.boom-movie-grid-info-overlay-title').text(ka.lib.getLocalizedTitleByUuid(uuid));
    }
};


ka.lib.handleKeypressSelect = function () {
    if (ka.state.currentPageMode == 'config') {
        ka.lib.executeConfigSelection();
    } else if (ka.state.currentPageMode == 'grid') {
        ka.state.currentPageMode = 'detail';
        ka.state.currentDetailButton = 0;

        ka.lib.updateDetailPage();
        ka.lib.updateDetailButtonSelection();

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({left: '-=1920'}, 720);
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
