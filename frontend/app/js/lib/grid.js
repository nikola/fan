/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};


ka.lib.setPrimaryPosterColor = function () {
    var colorThief = new ColorThief(),
        primaryColors = colorThief.getPalette($(this).get(0), 5),
        colorLuminance = [
            ka.lib.getLuminance(primaryColors[0])
          , ka.lib.getLuminance(primaryColors[1])
          , ka.lib.getLuminance(primaryColors[2])
        ],
        primaryColorRGB = primaryColors[colorLuminance.indexOf(Math.min.apply(Math, colorLuminance))];

    $(this).closest('.boom-movie-grid-info-overlay').find('.boom-movie-grid-info-overlay-title').css('backgroundColor', '#' + ((1 << 24) + (primaryColorRGB[0] << 16) + (primaryColorRGB[1] << 8) + primaryColorRGB[2]).toString(16).slice(1));
};


ka.lib.refreshMovieGrid = function () {
    // var previousMovieFragments = $('#content .boom-movie-grid-info-overlay').detach();
    // $('section').remove();

    ka.state.gridLookupItemsPerLine = [];
    ka.state.gridLookupLinesByKey = {};
    ka.state.gridTotalPages = 0;

    var filledLines = 0, lastFilledLines = null, totalLines = 0, totalItems = 0,
        itemsPerLine, startNewPage = true, tablesPerKey;
        /* groupNameElement */

    var keys = ka.config.gridKeys[ka.config.gridSortOrder], keyCount = keys.length;
    for (var key, keyIndex = 0; keyIndex < keyCount; keyIndex++) {
        key = keys[keyIndex];
        if (key in ka.data.cortex[ka.config.gridSortOrder]) {
            var items = ka.data.cortex[ka.config.gridSortOrder][key], count = items.count();
            if (count) {
                itemsPerLine = 0;
                tablesPerKey = -1;
                for (var movie, movieIndex = 0; movieIndex < count; movieIndex++) {
                    var movie = items.values()[movieIndex],
                        movieUuid =  movie.uuid,
                        movieTitle = movie.titleOriginal,
                        movieReleaseYear = movie.releaseYear,
                        movieRuntime = movie.runtime;
                    if (movieTitle.indexOf(':') > 9) {
                        movieTitle = movieTitle.substr(0, movieTitle.indexOf(':') + 1) + '<br>' + movieTitle.substr(movieTitle.indexOf(':') + 1);
                    }

                    if (lastFilledLines !== null && (movieIndex == 0 || startNewPage)) {
                        /* Update height of indicator. */
                        // groupNameElement.css('height', lastFilledLines * 360);
                    }

                    if (movieIndex == 0 || startNewPage) {
                        tablesPerKey++;
                        ka.state.gridTotalPages += 1;



                        /* groupNameElement = $(
                            '<table class="boom-movie-grid-letter-indicator">'
                                + '<tr>'
                                    + '<td class="boom-movie-grid-letter-cell">'
                                        + '<span class="boom-movie-grid-letter-indicator-text">' + key + '</span>'
                                    + '</td>'
                                + '</tr>'
                          + '</table>'
                        ).appendTo('#content'); */

                        // var table = $('<table id="boom-movie-grid-table-' + key + '-' + tablesPerKey + '" class="boom-movie-grid-table"></table>')
                        //     .appendTo('#content');

                        lastFilledLines = 0;
                    }

                    startNewPage = false;

                    if (movieIndex % ka.config.gridMaxColumns == 0) {
                        // var row = $('<tr>', {class: 'boom-movie-grid-line'}).appendTo(table);
                        lastFilledLines++;

                        if (typeof ka.state.gridLookupItemsPerLine[totalLines] == 'undefined') {
                            ka.state.gridLookupItemsPerLine[totalLines] = [];
                            totalLines++;
                        }
                    }

                    ka.state.gridLookupItemsPerLine[ka.state.gridLookupItemsPerLine.length - 1][itemsPerLine] = movieUuid;

                    var currentLine = Math.floor(totalItems / ka.config.gridMaxColumns);
                    if (key in ka.state.gridLookupLinesByKey) {
                        var lines = ka.state.gridLookupLinesByKey[key];
                        if (lines.indexOf(currentLine) == -1) {
                            lines.push(currentLine);
                        }
                    } else {
                        var lines = [currentLine];
                    }
                    ka.state.gridLookupLinesByKey[key] = lines;

                    var cell = $(
                        '<div class="boom-movie-grid-item">'
                          + '<div id="boom-movie-grid-item-' + movieUuid + '" class="boom-movie-grid-info-overlay">'
                              + '<div class="boom-movie-grid-info-overlay-image">'
                                  + '<img id="boom-poster-' + movieUuid + '" src="/movie/poster/' + movieUuid + '.jpg/200">'
                              + '</div>'
                              + '<div class="boom-movie-grid-info-overlay-text">'
                                  + '<div class="boom-movie-grid-info-overlay-title">' + movieTitle + '</div>'
                                  + '<div class="boom-movie-grid-info-overlay-text-additional">' + movieReleaseYear + '<br>' + movieRuntime + ' minutes</div>'
                              + '</div>'
                          + '</div>'
                      + '</div>'
                    ).appendTo('#content');
                    totalItems++;

                    // cell.find('img').on('load', ka.lib.setPrimaryPosterColor);

                    itemsPerLine += 1;

                    if (itemsPerLine == ka.config.gridMaxColumns) {
                        filledLines += 1;
                        itemsPerLine = 0;
                    }

                    if (filledLines == ka.config.gridMaxRows) {
                        startNewPage = true;
                        filledLines = 0;
                    }
                }

                if (itemsPerLine) {
                    for (var c = itemsPerLine; c < ka.config.gridMaxColumns; c++) {
                        $('<div class="boom-movie-grid-item"></div>').appendTo('#content');
                        totalItems++;
                    }

                    filledLines += 1;

                    if (filledLines == ka.config.gridMaxRows) {
                        startNewPage = true;
                        filledLines = 0;
                    }
                }
            }
        }
    }

    /* Update height of last indicator. */
    // groupNameElement.css('height', lastFilledLines * 360);

    // TODO: fade in
    $('#boom-poster-focus').css('display', 'block');
};


ka.lib.scrollToPage = function (page) {
    $('#content').css('-webkit-transform', 'translate3d(0, -' + page + '00%, 0)');
};
