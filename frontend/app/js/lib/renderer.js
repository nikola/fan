/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};
if (!('state' in ka)) ka.state = {};
if (!('config' in ka)) ka.config = {};

ka.config.gridMaxRows = 3;
ka.config.gridMaxColumns = 7;


ka.lib.getLuminance = function (color) {
    var red = color[0], green = color[1], blue = color[2],
        channelRed = red / 255,
        luminanceRed = (channelRed <= 0.03928) ? channelRed / 12.92 : Math.pow(((channelRed + 0.055) / 1.055), 2.4),
        channelGreen = green / 255,
        luminanceGreen = (channelGreen <= 0.03928) ? channelGreen / 12.92 : Math.pow(((channelGreen + 0.055) / 1.055), 2.4),
        channelBlue = blue / 255,
        luminanceBlue = (channelBlue <= 0.03928) ? channelBlue / 12.92 : Math.pow(((channelBlue + 0.055) / 1.055), 2.4);
    return 0.2126 * luminanceRed + 0.7152 * luminanceGreen + 0.0722 * luminanceBlue;
};


ka.lib.renderMovieThumbnail = function () {
    ka.state.gridLookup = [];
    ka.state.gridTotalPages = 0;

    var ITEMS_PER_LINE = 7, LINES_PER_PAGE = 3;

    var keys = ['123'].concat('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')), key;

    var filledLines = 0, lastFilledLines = null, itemsPerLine, startSection = true, tablePerKey, letterIndicator,
        totalLines = 0;

    for (var index = 0; index < 27; index++) {
        key = keys[index];
        if (key in ka.data.cortex.byLetter) {
            var movies = ka.data.cortex.byLetter[key];
            if (movies.count()) {


                itemsPerLine = 0;
                tablePerKey = -1;
                for (var m = 0; m < movies.values().length; m++) {
                    if (lastFilledLines !== null && (m == 0 || startSection)) {
                        /* Update height of letter indicator. */
                        letterIndicator.css('height', lastFilledLines * 360);
                    }

                    if (startSection) {
                        var section = $('<section>', {
                            class: 'boom-movie-grid-page'
                        }).appendTo($('#content'));

                        ka.state.gridTotalPages += 1;
                    }

                    if (m == 0 || startSection) {
                        tablePerKey++;
                        letterIndicator = $('<table class="boom-movie-grid-letter-indicator"><tr><td class="boom-movie-grid-letter-cell"></td></tr></table>', {
                        }).appendTo(section);

                        $('<span>', {
                            class: 'boom-movie-grid-letter-indicator-text'
                          , text: key
                        }).appendTo(letterIndicator.find('td'));

                        var table = $('<table>', {
                            id: 'boom-movie-grid-table-' + key + '-' + tablePerKey
                          , class: 'boom-movie-grid-table'
                        }).appendTo(section);

                        lastFilledLines = 0;

                        // ka.state.gridLookup.push(rowLookup);
                    }

                    startSection = false;

                    if (m % ITEMS_PER_LINE == 0) {
                        var row = $('<tr>', {
                            class: 'boom-movie-grid-line'
                        }).appendTo(table);
                        lastFilledLines++;

                        // var rowLookup = [];
                        if (typeof ka.state.gridLookup[totalLines] == 'undefined') {
                            ka.state.gridLookup[totalLines] = [];
                            totalLines++;
                        }

                    }

                    var cell = $('<td>', {
                        id: 'boom-movie-grid-item-' + movies.values()[m].uuid
                      , class: 'boom-movie-grid-item'
                    }).appendTo(row);

                    var title = movies.values()[m].titleOriginal;
                    if (title.indexOf(':') > 9) {
                        title = title.substr(0, title.indexOf(':') + 1) + '<br>' + title.substr(title.indexOf(':') + 1);
                    }

                    // TODO: remove obsolete <a> element
                    // var hover = $('<div class="ih-item square effect6 top_to_bottom"><a href="#"><div class="img"></div><div class="info"><h3>' + title + '</h3><p>' + movies.values()[m].releaseYear + '<br>' + movies.values()[m].runtime + ' minutes</p></div></a></div>').appendTo(cell);
                    var hover = $('<div class="ih-item square effect6 top_to_bottom"><div class="img"></div><div class="info"><h3>' + title + '</h3><p>' + movies.values()[m].releaseYear + '<br>' + movies.values()[m].runtime + ' minutes</p></div></div>').appendTo(cell);

                    var uuid =  movies.values()[m].uuid;

                    $('<img>', {
                        src: 'https://127.0.0.1:' + HTTP_PORT + '/movie/poster/' + uuid + '.jpg/200'
                      , id: 'boom-poster-' + uuid
                      , width: 200
                      , height: 300
                      , load: function (evt) {
                            /* var colorThief = new ColorThief(),
                                primaryColors = colorThief.getPalette($(this).get(0), 5),
                                colorLuminance = [
                                    ka.lib.getLuminance(primaryColors[0])
                                  , ka.lib.getLuminance(primaryColors[1])
                                  , ka.lib.getLuminance(primaryColors[2])
                                ],
                                primaryColorRGB = primaryColors[colorLuminance.indexOf(Math.min.apply(Math, colorLuminance))];
                            */

                            var row = $(this).data('boom.grid-row'),
                                column = $(this).data('boom.grid-column');

                            // $(this).closest('.square').find('h3').css('backgroundColor', '#' + ((1 << 24) + (primaryColorRGB[0] << 16) + (primaryColorRGB[1] << 8) + primaryColorRGB[2]).toString(16).slice(1));


                            ka.state.gridLookup[row][column] = {
                                uuid: $(this).attr('id').slice(12)
                            };
                        }
                      , data: {
                            'boom.debug-title': title // TODO: REMOVE !!!
                          , 'boom.grid-row': ka.state.gridLookup.length - 1
                          , 'boom.grid-column': itemsPerLine
                        }
                    }).appendTo(hover.find('.img'));

                    // console.log('Movie: ' + movies.values()[m].titleOriginal + ' line: ' + (ka.state.gridLookup.length - 1) + ' column: ' + itemsPerLine);


                    itemsPerLine += 1;

                    if (itemsPerLine == ITEMS_PER_LINE) {
                        filledLines += 1;
                        itemsPerLine = 0;
                    }

                    if (filledLines == LINES_PER_PAGE) {
                        startSection = true;
                        filledLines = 0;
                    }



                }



                if (itemsPerLine) {
                    for (var c = itemsPerLine; c < ITEMS_PER_LINE; c++) {
                        $('<td>', {
                            class: 'boom-movie-grid-item'
                        }).appendTo(row);
                    }

                    filledLines += 1;

                    if (filledLines == LINES_PER_PAGE) {
                        startSection = true;
                        filledLines = 0;
                    }
                }
            }
        }
    }

    /* Set height on last indicator. */
    letterIndicator.css('height', lastFilledLines * 360);

    /* if (indicatorFlipFlop) {
         letterIndicator.css('background-color', 'red');
    } else {
        letterIndicator.css('background-color', 'green');
    } */

    $('<div>', {
        id : 'boom-poster-focus'
      , css: {
            position: 'fixed'
          , border: '6px solid #ffffff'
          , width: '216px'
          , height: '316px'
          , top: '16px'
          , left: '116px'
        }
    }).appendTo('body');

    ka.state.gridFocusX = 0;
    ka.state.gridFocusY = 0;
    ka.state.gridPage = 0;

    var listener = new window.keypress.Listener();

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
                if (ka.state.gridLookup[gridFocusAbsoluteY - 1].length > ka.state.gridFocusX) { /* Focus can stay in same column. */
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
                    var driftLeft = '-=' + (ka.state.gridFocusX - (ka.state.gridLookup[gridFocusAbsoluteY - 1].length - 1)) * 260;
                    ka.state.gridFocusX = ka.state.gridLookup[gridFocusAbsoluteY - 1].length - 1;
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
                if (ka.state.gridLookup[gridFocusAbsoluteY + 1].length > ka.state.gridFocusX) {  /* Focus can stay in same column. */
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
                    var driftLeft = '-=' + (ka.state.gridFocusX - (ka.state.gridLookup[gridFocusAbsoluteY + 1].length - 1)) * 260;
                    ka.state.gridFocusX = ka.state.gridLookup[gridFocusAbsoluteY + 1].length - 1;
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
            if (ka.state.gridFocusX < ka.config.gridMaxColumns - 1  && ka.state.gridLookup[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY].length > ka.state.gridFocusX + 1) {
                ka.state.gridFocusX += 1;

                $('#boom-poster-focus').css('display', 'block');

                $('#boom-poster-focus').velocity({left: '+=260'}, {
                    duration: 260
                });
            }
        }
    });

};

ka.lib.scrollToPage = function (page) {
    // if (typeof settings.beforeMove == 'function') settings.beforeMove(page_index, next);

    $('#content').css('-webkit-transform', 'translate3d(0, -' + page + '00%, 0)');
};


/*
var settings = $.extend({}, defaults, options),
			el = $(this),

			lastAnimation = 0,
			quietPeriod = 500;



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