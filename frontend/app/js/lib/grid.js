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


ka.lib.recalcMovieGrid = function () {
    ka.state.gridLookupItemsPerLine = [];
    ka.state.gridLookupLinesByKey = {};
    ka.state.gridTotalPages = 1;

    var currentRowIndex = 0, currentColumnIndex, currentCellIndex = 0,
        keys = ka.config.gridKeys[ka.config.gridSortOrder], keyCount = keys.length;

    for (var key, keyIndex = 0; keyIndex < keyCount; keyIndex++) {
        key = keys[keyIndex];
        if (key in ka.data.cortex[ka.config.gridSortOrder]) {
            var items = ka.data.cortex[ka.config.gridSortOrder][key], count = items.count();
            if (count) {
                currentColumnIndex = 0;
                for (var movieIndex = 0; movieIndex < count; movieIndex++) {
                    if (movieIndex % ka.config.gridMaxColumns == 0) {
                        ka.state.gridLookupItemsPerLine.push([]);
                    }

                    ka.state.gridLookupItemsPerLine[ka.state.gridLookupItemsPerLine.length - 1][currentColumnIndex] = items.values()[movieIndex];

                    var currentLine = Math.floor(currentCellIndex / ka.config.gridMaxColumns);
                    if (key in ka.state.gridLookupLinesByKey) {
                        var lines = ka.state.gridLookupLinesByKey[key];
                        if (lines.indexOf(currentLine) == -1) {
                            lines.push(currentLine);
                        }
                    } else {
                        var lines = [currentLine];
                    }
                    ka.state.gridLookupLinesByKey[key] = lines;

                    currentCellIndex++;
                    currentColumnIndex++;

                    if (currentColumnIndex == ka.config.gridMaxColumns) {
                        currentRowIndex++;
                        currentColumnIndex = 0;
                    }

                    if (currentRowIndex == ka.config.gridMaxRows) {
                        ka.state.gridTotalPages += 1;
                        currentRowIndex = 0;
                    }
                }

                if (currentColumnIndex) {
                    currentCellIndex += (ka.config.gridMaxColumns - currentColumnIndex);

                    currentRowIndex++;

                    if (currentRowIndex == ka.config.gridMaxRows) {
                        ka.state.gridTotalPages += 1;
                        currentRowIndex = 0;
                    }
                }
            }
        }
    }
};


ka.lib.redrawMovieGridFull = function () {
    for (var row = 0, matrix = ka.state.gridLookupItemsPerLine, rows = matrix.length; row < rows; row++) {
        for (var column = 0, line = matrix[row], columns = line.length; column < columns; column++) {
            ka.lib.renderMovieGridCell(ka.state.gridLookupItemsPerLine[row][column]);
        }
        for (; column < ka.config.gridMaxColumns; column++) {
            ka.lib.renderMovieGridCell();
        }
    }

    if (ka.state.gridLookupItemsPerLine.length) {
        $('#boom-poster-focus').velocity('fadeIn', 1440);
    }
};


ka.lib.redrawMovieGridPartial = function () {

};


function disabled() {
    ka.state.gridLookupItemsPerLine = [];
    ka.state.gridLookupLinesByKey = {};
    ka.state.gridTotalPages = 0;

    var filledLines = 0, lastFilledLines = null, totalLines = 0,
        currentCellIndex = 0,
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
                        movieUuid =  movie.uuid;

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

                    // console.log(currentCellIndex)

                    var currentLine = Math.floor(currentCellIndex / ka.config.gridMaxColumns);
                    if (key in ka.state.gridLookupLinesByKey) {
                        var lines = ka.state.gridLookupLinesByKey[key];
                        if (lines.indexOf(currentLine) == -1) {
                            lines.push(currentLine);
                        }
                    } else {
                        var lines = [currentLine];
                    }
                    ka.state.gridLookupLinesByKey[key] = lines;

                    if ($('.boom-movie-grid-item').length > currentCellIndex) {
                        ka.lib.renderMovieGridCell(movie, $('.boom-movie-grid-item').eq(currentCellIndex));
                    } else {
                        ka.lib.renderMovieGridCell(movie);
                    }

                    // ka.lib.renderMovieGridCell(movie);

                    currentCellIndex++;

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
                        $('<div class="boom-movie-grid-item empty"></div>').appendTo('#content');
                        currentCellIndex++;
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


ka.lib.renderMovieGridCell = function (movie, target) {
    if (typeof movie != 'undefined') {
        var movieTitle = movie.titleOriginal;
        if (movieTitle.indexOf(':') > 9) {
            movieTitle = movieTitle.substr(0, movieTitle.indexOf(':') + 1) + '<br>' + movieTitle.substr(movieTitle.indexOf(':') + 1);
        }
        var cell = $(
            '<div class="boom-movie-grid-item">'
              + '<div id="boom-movie-grid-item-' + movie.uuid + '" class="boom-movie-grid-info-overlay">'
                  + '<div class="boom-movie-grid-info-overlay-image">'
                      + '<img id="boom-poster-' + movie.uuid + '" src="/movie/poster/' + movie.uuid + '.jpg/200">'
                  + '</div>'
                  + '<div class="boom-movie-grid-info-overlay-text">'
                      + '<div class="boom-movie-grid-info-overlay-title">' + movieTitle + '</div>'
                      + '<div class="boom-movie-grid-info-overlay-text-additional">' + movie.releaseYear + '<br>' + movie.runtime + ' minutes</div>'
                  + '</div>'
              + '</div>'
          + '</div>'
        );
    } else {
        var cell = $('<div class="boom-movie-grid-item"></div>');
    }

    if (typeof target != 'undefined') {
        cell.insertBefore(target);
    } else {
        cell.appendTo('#content');
    }

    // cell.find('img').on('load', ka.lib.setPrimaryPosterColor);
};


ka.lib.scrollToPage = function (page) {
    $('#content').css('-webkit-transform', 'translate3d(0, -' + page + '00%, 0)');
};
