/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};


ka.lib.refreshMovieGrid = function () {
    ka.state.gridLookup = [];
    ka.state.gridTotalPages = 0;

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
                    var movieUuid =  movies.values()[m].uuid,
                        movieTitle = movies.values()[m].titleOriginal,
                        movieReleaseYear = movies.values()[m].releaseYear,
                        movieRuntime = movies.values()[m].runtime;
                    if (movieTitle.indexOf(':') > 9) {
                        movieTitle = movieTitle.substr(0, movieTitle.indexOf(':') + 1) + '<br>' + movieTitle.substr(movieTitle.indexOf(':') + 1);
                    }

                    if (lastFilledLines !== null && (m == 0 || startSection)) {
                        /* Update height of indicator. */
                        letterIndicator.css('height', lastFilledLines * 360);
                    }

                    if (startSection) {
                        var section = $('<section class="boom-movie-grid-page"></section>')
                            .appendTo($('#content'));

                        ka.state.gridTotalPages += 1;
                    }

                    if (m == 0 || startSection) {
                        tablePerKey++;
                        letterIndicator = $('<table class="boom-movie-grid-letter-indicator"><tr><td class="boom-movie-grid-letter-cell"></td></tr></table>')
                            .appendTo(section);

                        $('<span class="boom-movie-grid-letter-indicator-text">' + key + '</span>')
                            .appendTo(letterIndicator.find('td'));

                        var table = $('<table id="boom-movie-grid-table-' + key + '-' + tablePerKey + '" class="boom-movie-grid-table"></table>')
                            .appendTo(section);

                        lastFilledLines = 0;
                    }

                    startSection = false;

                    if (m % ka.config.gridMaxColumns == 0) {
                        var row = $('<tr>', {class: 'boom-movie-grid-line'}).appendTo(table);
                        lastFilledLines++;

                        if (typeof ka.state.gridLookup[totalLines] == 'undefined') {
                            ka.state.gridLookup[totalLines] = [];
                            totalLines++;
                        }
                    }

                    ka.state.gridLookup[ka.state.gridLookup.length - 1][itemsPerLine] = movieUuid;

                    var cell = $(
                        '<td id="boom-movie-grid-item-' + movieUuid + '" class="boom-movie-grid-item">'
                          + '<div class="boom-movie-grid-info-overlay">'
                              + '<div class="boom-movie-grid-info-overlay-image">'
                                  + '<img id="boom-poster-' + movieUuid + '" src="/movie/poster/' + movieUuid + '.jpg/200">'
                              + '</div>'
                              + '<div class="boom-movie-grid-info-overlay-text">'
                                  + '<div class="boom-movie-grid-info-overlay-title">' + movieTitle + '</div>'
                                  + '<div class="boom-movie-grid-info-overlay-text-additional">' + movieReleaseYear + '<br>' + movieRuntime + ' minutes</div>'
                              + '</div>'
                          + '</div>'
                        + '</td>').appendTo(row);

                    cell.find('img').on('load', ka.lib.setPrimaryPosterColor);

                    itemsPerLine += 1;

                    if (itemsPerLine == ka.config.gridMaxColumns) {
                        filledLines += 1;
                        itemsPerLine = 0;
                    }

                    if (filledLines == ka.config.gridMaxRows) {
                        startSection = true;
                        filledLines = 0;
                    }
                }

                if (itemsPerLine) {
                    for (var c = itemsPerLine; c < ka.config.gridMaxColumns; c++) {
                        $('<td class="boom-movie-grid-item"></td>').appendTo(row);
                    }

                    filledLines += 1;

                    if (filledLines == ka.config.gridMaxRows) {
                        startSection = true;
                        filledLines = 0;
                    }
                }
            }
        }
    }

    /* Update height of last indicator. */
    letterIndicator.css('height', lastFilledLines * 360);



    ka.lib.registerShortcuts()


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