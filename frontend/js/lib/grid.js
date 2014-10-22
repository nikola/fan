/**
 *  fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
 *  Copyright (C) 2013-2014 Nikola Klaric.
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.

 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *
 *  @author Nikola Klaric (nikola@klaric.org)
 *  @copyright Copyright (C) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.grid = {

    focus: {

        show: function () {
            return $('#boom-grid-focus').velocity('fadeIn', 0);
        }

      , hide: function () {

        }

      , fadeIn: function (duration) {
            return $('#boom-grid-focus').velocity('fadeIn', duration);
        }

      , fadeOut: function (duration) {
             return $('#boom-grid-focus').velocity('fadeOut', duration);
        }

      , isPositionValid: function () {
            return ka.state.gridLookupMatrix.length > ka.lib.getGridFocusAbsoluteY() && ka.state.gridFocusX < ka.lib.getItemsPerLineAtFocus();
        }

    }

  , occlude: function () {
        if (ka.state.gridPage > 0 || ka.state.gridPage + 1 < ka.state.gridTotalPages) {
            var items = $('.boom-movie-grid-item'), keys = $('.boom-movie-grid-key'), buffer = $();

            if (ka.state.gridPage > 0) {
                buffer = buffer.add(items.slice(0, ka.settings.gridMaxColumns * ka.settings.gridMaxRows * ka.state.gridPage));
                buffer = buffer.add(keys.slice(0, ka.settings.gridMaxRows * ka.state.gridPage));
            }

            if (ka.state.gridPage + 1 < ka.state.gridTotalPages) {
                buffer = buffer.add(items.slice(ka.settings.gridMaxColumns * ka.settings.gridMaxRows * (ka.state.gridPage + 1)));
                buffer = buffer.add(keys.slice(ka.settings.gridMaxRows * (ka.state.gridPage + 1)));
            }

            ka.state.occludedGridItems = buffer;

            buffer.css('display', 'none');
            $('#boom-movie-grid-container')
                .css('transform', 'translate(0,0)')
                .velocity({translateZ: 0, translateY: '0px'}, 0);
        }
    }

  , unocclude: function () {
        if (ka.state.occludedGridItems !== null && ka.state.occludedGridItems.length > 0) {
            ka.state.occludedGridItems.css({display: 'inline-block'});
            $('#boom-movie-grid-container')
                .css('transform', 'translate(0,-' + (ka.state.gridPage * 1080) + 'px)')
                .velocity({translateZ: 0, translateY: '-' + (ka.state.gridPage * 1080) + 'px'}, 0);
        }
    }

  , processDeferredUpdates: function () {
        ka.state.view = 'grid';

        ka.lib.updateMovieGridOnAdd(false);
    }

  , snapshotMovieLookups: function () {
        ka.state.lastGridMovieListSnapshot = ka.data.asList.concat();
        ka.state.lastGridMovieIndexSnapshot = JSON.parse(JSON.stringify(ka.data.indexById));
    }

  , getMovieListSnapshot: function () {
        return ka.state.lastGridMovieListSnapshot;
    }

  , getMovieIndexSnapshot: function () {
        return ka.state.lastGridMovieIndexSnapshot;
    }

};


ka.lib.onPosterLoaded = function () {
    if (ka.state.isProcessingInitialItems) {
        ka.state.processingInitialItemsCount -= 1;

        if (ka.state.processingInitialItemsCount == 0) {
            ka.state.isProcessingInitialItems = false;
            ka.state.processingInitialItemsCount = null;

            onPostersLoaded();
        }
    }
};


ka.lib.hideBrokenPoster = function () {
    var overlayElement = $(this).closest('.boom-movie-grid-info-overlay'),
        movieObj = ka.data.byId[$(this).closest('.boom-grid-item').data('boom.id')];

    ka.lib.activatePosterOverlay(movieObj, overlayElement);

    overlayElement.addClass('boom-blocked');

    $(this).hide();

    ka.lib.onPosterLoaded();
};


ka.lib.setPrimaryPosterColor = function () {
    var gridItem = $(this).closest('.boom-movie-grid-item'),
        id = gridItem.data('boom.id');

    if ('primaryPosterColor' in ka.data.byId[id] && !!ka.data.byId[id].primaryPosterColor) {
        /*  Weird bug:
         *  Trigger full render of grid by painting every single poster on canvas.
         */
        var image = $(this).get(0),
            context = ka.state.canvasContext;

        context.canvas.width = image.naturalWidth;
        context.canvas.height = image.naturalHeight;
        context.drawImage(image, 0, 0, image.naturalWidth, image.naturalHeight);

        gridItem.find('.boom-movie-grid-info-overlay-title').css('backgroundColor', '#' + ka.data.byId[id].primaryPosterColor);
    } else {
        var pixelArray = ka.lib.getPixelsFromImage($(this));
        pixelArray.unshift(id);
        ka.state.imagePosterPixelArrayBacklog.push(pixelArray);

        setTimeout(ka.lib.processPixelArray, 0);
    }

    gridItem.find('.boom-movie-grid-info-overlay').removeClass('active');
    ka.state.setOfKnownPosters[id] = true;
    if (id in ka.state.setOfUnknownPosters) {
        delete ka.state.setOfUnknownPosters[id];
    }

    ka.lib.onPosterLoaded();
};


ka.lib.processPixelArray = function () {
    if (!ka.state.imagePosterPixelArrayBacklog.length) return;

    var nextPixelArray = ka.state.imagePosterPixelArrayBacklog.shift(),
        id = nextPixelArray.shift(),
        primaryColors = MMCQ.quantize(nextPixelArray, 5).palette(),
        colorLuminance = [
            ka.lib.getLuminance(primaryColors[0])
          , ka.lib.getLuminance(primaryColors[1])
          , ka.lib.getLuminance(primaryColors[2])
        ],
        primaryColorRGB = primaryColors[colorLuminance.indexOf(Math.min.apply(Math, colorLuminance))],
        primaryColorHex = ((1 << 24) + (primaryColorRGB[0] << 16) + (primaryColorRGB[1] << 8) + primaryColorRGB[2]).toString(16).slice(1);

    $('#boom-movie-grid-item-' + id + ' .boom-movie-grid-info-overlay-title').css('backgroundColor', '#' + primaryColorHex);
    ka.data.byId[id].primaryPosterColor = primaryColorHex;
    ka.state.imagePosterPrimaryColorById[id] = primaryColorHex;

    $.get('/update/' + id + '/poster-color/' + primaryColorHex);
};


ka.lib.recalcMovieGrid = function () {
    var lookupMatrix = ka.state.gridLookupMatrix = [];
    ka.state.gridLookupLinesByKey = {};
    ka.state.gridLookupKeyByLine = [];
    ka.state.gridLookupCoordById = {};

    if (ka.state.gridSortCriterion == 'byBudget') {
        var keys = Object.getOwnPropertyNames(ka.data[ka.state.gridSortCriterion]).sort(ka.lib.sortExpandedKeys);
    } else {
        var keys = Object.getOwnPropertyNames(ka.data[ka.state.gridSortCriterion]).sort();
    }
    var keyCount = keys.length;
    if (ka.state.gridSortOrder == 'desc') {
        keys.reverse();
    }

    var currentScreenLine = 0, currentScreenColumn,
        currentGlobalCellCounter = 0, currentGlobalLine,
        lastCompilationName,
        movieDict;
    for (var key, keyIndex = 0; keyIndex < keyCount; keyIndex++) {
        key = keys[keyIndex];
        if (key in ka.data[ka.state.gridSortCriterion]) {
            var items = ka.data[ka.state.gridSortCriterion][key], count = items.length;
            if (count) {
                currentScreenColumn = 0;
                lastCompilationName = null;
                for (var movieIndex = 0; movieIndex < count; movieIndex++) {
                    movieDict = items[movieIndex];

                    currentGlobalLine =  Math.floor(currentGlobalCellCounter / ka.settings.gridMaxColumns);

                    if (movieIndex % ka.settings.gridMaxColumns == 0) {
                        lookupMatrix.push([]);
                    }

                    if (movieDict.isCompiled) {
                        if (ka.state.isProcessingInitialItems && lastCompilationName == movieDict.compilation) {
                            ka.state.processingInitialItemsCount -= 1;
                        }

                        lastCompilationName = movieDict.compilation;

                        var item = lookupMatrix[currentGlobalLine][currentScreenColumn];
                        if ($.isArray(item)) {
                            item.push(movieDict);
                        } else {
                            lookupMatrix[currentGlobalLine][currentScreenColumn] = [movieDict];
                        }
                    } else {
                        lastCompilationName = null;

                        lookupMatrix[currentGlobalLine][currentScreenColumn] = movieDict;
                    }

                    ka.state.gridLookupKeyByLine[currentGlobalLine] = key;
                    ka.state.gridLookupCoordById[movieDict.id] = [currentScreenColumn, currentGlobalLine];

                    if (key in ka.state.gridLookupLinesByKey) {
                        var lines = ka.state.gridLookupLinesByKey[key];
                        if (lines.indexOf(currentGlobalLine) == -1) {
                            lines.push(currentGlobalLine);
                        }
                    } else {
                        var lines = [currentGlobalLine];
                    }
                    ka.state.gridLookupLinesByKey[key] = lines;

                    if (!(movieDict.isCompiled && movieIndex < (count - 1) && items[movieIndex + 1].compilation == movieDict.compilation)) {
                        currentGlobalCellCounter++;
                        currentScreenColumn++;

                        if (currentScreenColumn == ka.settings.gridMaxColumns) {
                            currentScreenLine++;
                            currentScreenColumn = 0;
                        }

                        if (currentScreenLine == ka.settings.gridMaxRows) {
                            currentScreenLine = 0;
                        }
                    }
                }

                if (currentScreenColumn) {
                    for (; currentScreenColumn < ka.settings.gridMaxColumns; currentScreenColumn++) {
                        lookupMatrix[currentGlobalLine][currentScreenColumn] = null;
                        currentGlobalCellCounter++;
                    }
                    currentScreenLine++;

                    if (currentScreenLine == ka.settings.gridMaxRows) {
                        currentScreenLine = 0;
                    }
                }
            }
        }
    }

    /* Remove trailing empty compilations. */
    while (!lookupMatrix[lookupMatrix.length - 1].length) {
        lookupMatrix.pop();
    }

    ka.data.asList = [];
    ka.data.indexById = {};

    for (var row = 0; row < lookupMatrix.length; row++) {
        for (var column = 0; column < ka.settings.gridMaxColumns; column++) {
            var item = lookupMatrix[row][column];
            if ($.isArray(item)) {
                if (item.length == 1) {
                    lookupMatrix[row][column] = item[0];
                } else {
                    item.sort(function (a, b) {
                        if (a.releaseYear > b.releaseYear) {
                            return 1;
                        } else if (a.releaseYear < b.releaseYear) {
                            return -1;
                        } else if (a[ka.state.gridSortCriterion] > b[ka.state.gridSortCriterion]) {
                            return 1;
                        } else if (a[ka.state.gridSortCriterion] < b[ka.state.gridSortCriterion]) {
                            return -1;
                        } else {
                            return 0;
                        }
                    });
                }

                for (var index = 0, movieObj; movieObj = item[index]; index++) {
                    ka.data.indexById[movieObj.id] = ka.data.asList.length;
                    ka.data.asList.push(movieObj);
                }
            } else {
                if (item !== null) {
                    ka.data.indexById[item.id] = ka.data.asList.length;
                    ka.data.asList.push(item);
                }
            }
        }
    }

    ka.state.gridTotalPages = Math.ceil(lookupMatrix.length / ka.settings.gridMaxRows);
};


ka.lib.updateMovieGridOnChange = function () {
    var currentCellIndex = 0,
        renderedCells = $('.boom-movie-grid-item'), detachedCell,
        renderedKeyContainers = $('.boom-movie-grid-key'),
        hasCells = renderedCells.length > 0,
        lastKey = null, currentKey,
        movie;

    for (var row = 0, matrix = ka.state.gridLookupMatrix, rows = matrix.length; row < rows; row++) {
        var keyContainer = renderedKeyContainers.eq(row);
        if (!keyContainer.size()) {
            keyContainer = $('<span class="boom-movie-grid-key"></span>').appendTo('#boom-movie-grid-container');
        }

        currentKey = ka.state.gridLookupKeyByLine[row];
        if (currentKey != lastKey || row % ka.settings.gridMaxRows == 0) {
            keyContainer.css('visibility', 'visible');

            var keyLabel = keyContainer.find('.boom-movie-grid-key-label');
            if (keyLabel.size()) {
                keyLabel.text(currentKey).attr('id', 'boom-movie-grid-key-'+ currentKey);
            } else{
                $('<span class="boom-movie-grid-key-label" id="boom-movie-grid-key-' + currentKey + '">' + currentKey + '</span>').appendTo(keyContainer);
            }

            lastKey = currentKey;
        } else {
            keyContainer.css('visibility', 'hidden');
        }

        for (var column = 0, line = matrix[row], columns = line.length; column < columns; column++) {
            movie = ka.lib.getFirstMovieObjectFromCoord(column, row);

            if (movie !== null) {
                ka.state.gridLookupItemsPerLine[row] = column + 1;
            }

            if (!hasCells || currentCellIndex >= renderedCells.length) {
                ka.lib.renderMovieGridCell(movie, 'appendTo', $('#boom-movie-grid-container'));
            } else {
                if (renderedCells.eq(currentCellIndex).hasClass('empty')) {
                    ka.lib.renderMovieGridCell(movie, 'replaceWith', renderedCells.eq(currentCellIndex));
                } else {
                    if (movie === null || movie.id != renderedCells.eq(currentCellIndex).data('boom.id')) {
                        ka.lib.renderMovieGridCell(movie, 'insertAfter', renderedCells.eq(currentCellIndex));
                        detachedCell = renderedCells.eq(currentCellIndex).detach();
                        ka.state.detachedGridCells[renderedCells.eq(currentCellIndex).data('boom.id')] = detachedCell;
                        renderedCells = $('.boom-movie-grid-item').not(detachedCell);
                    }
                }
            }

            if (movie !== null) {
                var element = $('#boom-poster-' + movie.id).get(0);
                if (row >= ka.state.gridPage * ka.settings.gridMaxRows
                        && row < (ka.state.gridPage + 1) * ka.settings.gridMaxRows
                        && column < 4) {
                    if (ka.state.view == 'config') {
                        ka.state.desaturationImageCache[movie.id] = element;
                        element.style.webkitTransform = 'translate3d(0, 0, 0)';
                        element.style.webkitFilter = 'saturate(0%)';
                    }
                } else {
                    if (ka.state.view == 'config') {
                        if (movie.id in ka.state.desaturationImageCache) {
                            delete ka.state.desaturationImageCache[movie.id];
                        }
                        element.style.webkitTransform = 'none';
                        element.style.webkitFilter = 'none';
                    }
                }
            }

            currentCellIndex++;
        }
    }

    /* After changing the sort order, superfluous items might still be rendered at the tail of the grid. */
    $('.boom-movie-grid-item').slice(currentCellIndex).remove();
    $('.boom-movie-grid-key').slice(ka.state.gridLookupMatrix.length).remove();

    if (ka.state.gridLookupMatrix.length && ka.state.view == 'grid') {
        if (ka.state.shouldFocusFadeIn) {
            ka.lib.grid.focus.fadeIn(ka.settings.durationLong);
            ka.state.shouldFocusFadeIn = false;
        } else {
            ka.lib.grid.focus.show();
        }
    }
};


ka.lib.updateMovieGridOnAdd = function (isImmediateUpdate) {
    if (ka.state.view == 'limbo' && isImmediateUpdate) { /* && !ka.state.hasDeferredGridUpdate) { */
        ka.state.hasDeferredGridUpdate = true;
    } else if (ka.state.view != 'limbo' && (ka.state.hasDeferredGridUpdate || isImmediateUpdate)) {
        ka.state.hasDeferredGridUpdate = false;

        /* if (ka.state.currentCompilationPosterCount == 0 && (ka.state.view == 'detail' || ka.state.view == 'detail-browser' || ka.state.view == 'play:movie' || ka.state.view == 'play:trailer')) {
            ka.lib.updateMovieGridRefocused(true, ka.lib.unoccludeMovieGrid);

            ka.lib.occludeMovieGrid();

            var currentLeftPos = parseInt($('#boom-grid-focus').css('left'));
            if (currentLeftPos > 0 && currentLeftPos < 1920) {
                $('#boom-grid-focus').velocity({left: currentLeftPos - 1920}, {duration: 0, display: 'none'});
            }
        } else */ if (ka.state.view == 'config') {
            ka.lib.updateDesaturatedGrid();
        } else if (ka.state.view == 'grid') {
            ka.lib.recalcMovieGrid();
            ka.lib.updateMovieGridOnChange();
        }
    }
};


ka.lib.renderMovieGridCell = function (movie, operation, context) {
    if (typeof movie != 'undefined' && movie != null) {
        if (movie.id in ka.state.detachedGridCells) {
            var cell = ka.state.detachedGridCells[movie.id];
        } else {
            var cell = ka.lib.renderMovieObject(
                movie
              , 'boom-movie-grid-item-' + movie.id
              , 'boom-poster-' + movie.id
              , 200, 300
              , 'movie'
              , ka.lib.setPrimaryPosterColor
              , ka.lib.hideBrokenPoster
            );
        }
    } else {
        var cell = $('<div class="boom-movie-grid-item empty"></div>');
    }

    if (operation == 'replaceWith') {
        context.replaceWith(cell);
    } else {
        cell[operation](context);
    }

    if (typeof movie != 'undefined' &&  movie != null && movie.id in ka.state.detachedGridCells) {
        delete ka.state.detachedGridCells[movie.id];
    }
};


ka.lib.renderMovieObject = function (movieObj, movieId, posterId, posterWidth, posterHeight, infix, onLoaded, onError) {
    if (movieObj.id in ka.state.setOfUnknownPosters || !(movieObj.id in ka.state.setOfKnownPosters)) {
        var extraClass =  ' active',
            title = ka.lib.getLocalizedTitle(movieObj, true),
            additional = movieObj.releaseYear + '<br>' + movieObj.runtime;
    } else {
        var extraClass = title = additional = '';
    }

    return $(
        '<div id="' + movieId + '" class="boom-' + infix + '-grid-item boom-grid-item">'
          + '<div class="boom-movie-grid-info-overlay' + extraClass + '">'
              /* + '<div class="boom-movie-grid-info-overlay-image">' */
              + '<img class="boom-movie-grid-image" id="' + posterId + '">'
              /* + '</div>' */
              + '<div class="boom-movie-grid-info-overlay-text">'
                  + '<div class="boom-movie-grid-info-overlay-title">' + title + '</div>'
                  + '<div class="boom-movie-grid-info-overlay-text-additional">' + additional + ' minutes</div>'
              + '</div>'
          + '</div>'
      + '</div>').data('boom.id', movieObj.id)
        .find('img')
            .error(onError)
            .on('load', onLoaded)
            .attr('src', '/movie/poster/' + movieObj.keyPoster + '-' + posterWidth + '.image')
        .end();
};


ka.lib.scrollGrid = function (skipEvents) {
    var options = {duration: ka.settings.durationLong, easing: 'ease-out'};

    if (!skipEvents) {
        ka.state.view = 'limbo';
        options.complete = ka.lib.grid.processDeferredUpdates;
    }

    $('#boom-movie-grid-container').velocity({translateZ: 0, translateY: '-' + (ka.state.gridPage * 1080) + 'px'}, options);
};


ka.lib.getFirstMovieObjectFromCoord = function (x, y) {
    var obj = ka.state.gridLookupMatrix[y][x];

    if ($.isArray(obj)) {
        return obj[0];
    } else {
        return obj;
    }
};


ka.lib.moveFocusFirstItem = function () {
    if (ka.state.gridFocusX > 0) {
        var distance = 260 * ka.state.gridFocusX;
        ka.state.gridFocusX = 0;

        ka.lib.moveMovieFocusHorizontally('-=' + distance);
    }
};


ka.lib.moveFocusLastItem = function () {
    var items = ka.lib.getItemsPerLineAtFocus();
    if (ka.state.gridFocusX < items - 1) {
        var distance = 260 * (items - ka.state.gridFocusX - 1);
        ka.state.gridFocusX = items - 1;

        ka.lib.moveMovieFocusHorizontally('+=' + distance);
    }
};


ka.lib.moveFocusPageUp = function () {
    if (ka.state.gridPage > 0) {
        var transition = ka.lib.moveFocusX(-ka.settings.gridMaxRows);
        if (transition !== null) {
            ka.state.view = 'limbo'; /* leaving limbo after scrollGrid() call below */
            $('#boom-grid-focus').velocity(transition[0], transition[1]);
        }

        ka.state.gridPage -= 1;
        ka.lib.scrollGrid();
    }
};


ka.lib.moveFocusPageDown = function () {
    if (ka.state.gridPage + 1 < ka.state.gridTotalPages) {
        var transitionX = ka.lib.moveFocusX(ka.settings.gridMaxRows),
            transitionY = null;

        ka.state.gridPage += 1;

        if (ka.state.gridFocusY > 0 && ka.lib.getGridFocusAbsoluteY() >= ka.state.gridLookupMatrix.length) {
            var overshoot = ka.lib.getGridFocusAbsoluteY() - ka.state.gridLookupMatrix.length + 1,
                offsetY = overshoot * 360;
            ka.state.gridFocusY -= overshoot;

            transitionY = [{top: '-=' + offsetY}, {duration: offsetY}];
        }

        ka.state.view = 'limbo';

        if (transitionX !== null && transitionY !== null) {
            $('#boom-grid-focus').velocity(
                {translateZ: 0, left: transitionX[0].left, top: transitionY[0].top}
              , {easing: 'easeOutSine', duration: Math.max(transitionX[1].duration, transitionY[1].duration)}
            );
        } else if (transitionX !== null) {
            $('#boom-grid-focus').velocity({translateZ: 0, left: transitionX[0].left}, {easing: 'easeOutSine', duration: transitionX[1].duration});
        } else if (transitionY !== null) {
            $('#boom-grid-focus').velocity({translateZ: 0, top: transitionY[0].top}, {easing: 'ease-out', duration: transitionY[1].duration});
        }

        ka.lib.scrollGrid();
    }
};


ka.lib.moveFocusUp = function () {
    var gridFocusAbsoluteY = ka.lib.getGridFocusAbsoluteY(),
        notFirstRow = ka.state.gridFocusY > 0,
        notFirstPage = ka.state.gridPage > 0;

    if (gridFocusAbsoluteY > 0 && (notFirstRow || notFirstPage)) {
        ka.state.view = 'limbo';

        var props = {translateZ: 0}, options = {
            complete: ka.lib.grid.processDeferredUpdates
        };

        if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1] <= ka.state.gridFocusX) {
            props.left = ka.lib.repositionFocusX(gridFocusAbsoluteY - 1);

            options.easing = 'easeOutSine';
        } else {
            options.easing = 'ease-out';
        }

        if (notFirstRow) {
            props.top = '-=360';
            options.duration = ka.settings.durationNormal;

            ka.state.gridFocusY -= 1;
        } else {
            props.top = '+=720';
            options.duration = ka.settings.durationLong;

            ka.state.gridFocusY = ka.settings.gridMaxRows - 1;
            ka.state.gridPage -= 1;
            ka.lib.scrollGrid(true); /* skip limbo and deferred handling here */
        }

        $('#boom-grid-focus').velocity(props, options);
    }
};


ka.lib.moveFocusDown = function () {
    var gridFocusAbsoluteY = ka.lib.getGridFocusAbsoluteY(),
        notLastRow = ka.state.gridFocusY + 1 < ka.settings.gridMaxRows,
        notLastPage = ka.state.gridPage + 1 < ka.state.gridTotalPages;

    if (gridFocusAbsoluteY + 1 < ka.state.gridLookupMatrix.length && (notLastRow || notLastPage)) {
        var props = {translateZ: 0}, options = {
            complete: ka.lib.grid.processDeferredUpdates
        };

        if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1] <= ka.state.gridFocusX) {
            props.left = ka.lib.repositionFocusX(gridFocusAbsoluteY + 1);

            options.easing = 'easeOutSine';
        } else {
            options.easing = 'ease-out';
        }

        if (notLastRow) {
            props.top = '+=360';
            options.duration = ka.settings.durationNormal;

            ka.state.gridFocusY += 1;
        } else {
            props.top = '-=720';
            options.duration = ka.settings.durationLong;

            ka.state.gridFocusY = 0;
            ka.state.gridPage += 1;
            ka.lib.scrollGrid(true); /* skip limbo and deferred handling here */
        }

        $('#boom-grid-focus').velocity(props, options);
    }
};


ka.lib.moveMovieFocusHorizontally = function (offset) {
    ka.state.view = 'limbo';

    ka.lib.grid.focus.show().velocity({translateZ: 0, left: offset}, {duration: 260, complete: ka.lib.grid.processDeferredUpdates});
};


ka.lib.moveFocusLeft = function () {
    if (ka.state.gridFocusX > 0) {
        ka.state.gridFocusX -= 1;

        ka.lib.moveMovieFocusHorizontally('-=260');
    }
};


ka.lib.moveFocusRight = function () {
    if (ka.state.gridFocusX < ka.settings.gridMaxColumns - 1 && ka.state.gridFocusX + 1 < ka.lib.getItemsPerLineAtFocus()) {
        ka.state.gridFocusX += 1;

        ka.lib.moveMovieFocusHorizontally('+=260');
    }
};


ka.lib.moveFocusToIndex = function (index) {
    if (index < ka.lib.getItemsPerLineAtFocus() && index != ka.state.gridFocusX) {
        var distance = 260 * (index - ka.state.gridFocusX), operator = (distance < 0) ? '-' : '+';
        ka.state.gridFocusX = index;

        ka.lib.moveMovieFocusHorizontally(operator + '=' + Math.abs(distance));
    }
};


ka.lib.activatePosterOverlay = function (movieObj, element) {
    var source, additionalHtml;

    if ($.isArray(movieObj)) {
        source = movieObj[0];

        for (var movie, years = [], index = 0; movie = movieObj[index]; index++) {
            years.push(movie.releaseYear);
        }
        additionalHtml = Math.min.apply(Math, years) + ' - ' + Math.max.apply(Math, years);
    } else {
        source = movieObj;

        additionalHtml = movieObj.releaseYear + '<br>' + movieObj.runtime + ' minutes';
    }

    element
        .find('.boom-movie-grid-info-overlay-title').html(ka.lib.getLocalizedTitle(source, true)).end()
        .find('.boom-movie-grid-info-overlay-text-additional').html(additionalHtml).end()
        .addClass('active');
};


ka.lib.toggleGridFocus = function () {
    var id = ka.lib.getFirstMovieObjectFromCoord(ka.state.gridFocusX, ka.lib.getGridFocusAbsoluteY()).id,
        element = $('#boom-movie-grid-item-' + id + ' .boom-movie-grid-info-overlay');

    if (element.hasClass('boom-blocked')) {
        return;
    } else if (!element.hasClass('active')) {
        var movieObj = ka.lib.getVariantFromGridFocus();

        ka.lib.activatePosterOverlay(movieObj, element);
    } else {
        element.removeClass('active');
    }
};


ka.lib.toggleCompilationFocus = function () {
    var element = $('.boom-compilation-grid-item:nth-child(' + (ka.state.currentCompilationFocusIndex + 1) + ')'),
        movieObj = ka.lib.getVariantFromGridFocus()[ka.state.currentCompilationFocusIndex];

    element
        .find('.boom-movie-grid-info-overlay-title')
            .css('backgroundColor', '#' + movieObj.primaryPosterColor)
            .html(
                ka.lib.getLocalizedTitle(movieObj, true, true)
            ).end()
        .find('.boom-movie-grid-info-overlay-text-additional').html(
                movieObj.releaseYear + '<br>' + movieObj.runtime + ' minutes'
            ).end()
        .toggleClass('active');
};


ka.lib.moveCompilationFocusLeft = function () {
    if (ka.state.currentCompilationFocusIndex > 0) {
        ka.state.currentCompilationFocusIndex -= 1;

        ka.lib.repositionCompilationFocus();
    }
};


ka.lib.moveCompilationFocusRight = function () {
    if (ka.state.currentCompilationFocusIndex + 1 < ka.state.currentCompilationPosterCount) {
        ka.state.currentCompilationFocusIndex += 1;

        ka.lib.repositionCompilationFocus();
    }
};


ka.lib.moveCompilationFocusUp = function () {
    if (ka.state.currentCompilationFocusIndex + 1 > ka.state.currentCompilationColumnSize) {
        ka.state.currentCompilationFocusIndex -= ka.state.currentCompilationColumnSize;

        ka.lib.repositionCompilationFocus();
    }
};


ka.lib.moveCompilationFocusDown = function () {
    if (ka.state.currentCompilationFocusIndex + ka.state.currentCompilationColumnSize < ka.state.currentCompilationPosterCount) {
        ka.state.currentCompilationFocusIndex += ka.state.currentCompilationColumnSize;

        ka.lib.repositionCompilationFocus();
    }
};


ka.lib.repositionCompilationFocus = function () {
    var target = $('.boom-compilation-grid-item:nth-child(' + (ka.state.currentCompilationFocusIndex + 1) + ')').offset();
    $('#boom-compilation-focus').velocity({
        top: target.top + ka.settings.compilationPosterOffsetTop
      , left: target.left + ka.settings.compilationPosterOffsetLeft
    }, ka.settings.durationNormal);
};


ka.lib.populateCompilationGrid = function () {
    var compilation = ka.lib.getVariantFromGridFocus();
    ka.state.currentCompilationPosterCount = compilation.length;
    ka.state.currentCompilationFocusIndex = 0;

    $('#boom-compilation-grid').empty();
    for (var movieObj, index = 0; movieObj = compilation[index]; index++) {
        ka.lib.renderMovieObject(
            movieObj
          , 'boom-movie-compilation-item-' + movieObj.id
          , 'boom-movie-compilation-poster-' + movieObj.id
          , 300, 450
          , 'compilation'
          , null
          , ka.lib.hideBrokenPoster
        ).appendTo('#boom-compilation-grid');
    }
};


ka.lib.openCompilation = function (callback) {
    ka.lib.grid.focus.fadeOut(ka.settings.durationShort);

    var gridMaxColumns = ka.settings.gridMaxColumns,
        posterArray = ka.lib.getCurrentScreenPosters(gridMaxColumns),
        relativePosX = [100, 83, 66, 50, 34, 17, 0],
        relativePosY = [100, 50, 0];

    for (var index = 0; index < posterArray.length; index++) {
        if (posterArray[index] != null) {
            posterArray[index]
                .css({
                    '-webkit-transform-origin': relativePosX[index % gridMaxColumns] + '% ' + relativePosY[Math.floor(index / gridMaxColumns)] + '%'
                  , '-webkit-transform': 'scale3d(1, 1, 1)'
                })
                .velocity({scaleX: 0.75, scaleY: 0.75, scaleZ: 1, opacity: 0.15}, {duration: ka.settings.durationNormal, progress: function(elements, percentComplete) {
                    elements[0].style.webkitFilter = 'blur(' + Math.round(3 * percentComplete) + 'px)';
                }});
        }
    }

    var movieCount = ka.lib.getVariantFromGridFocus().length;
    if (movieCount < 6) {
        ka.state.currentCompilationColumnSize = movieCount;
    } else if (movieCount == 6) {
        ka.state.currentCompilationColumnSize = 3;
    } else if (movieCount < 9) {
        ka.state.currentCompilationColumnSize = 4;
    } else {
        ka.state.currentCompilationColumnSize = 5;
    }

    $('.boom-movie-grid-key').slice(ka.state.gridPage * ka.settings.gridMaxRows, (ka.state.gridPage + 1) * ka.settings.gridMaxRows)
        .velocity({opacity: 0}, ka.settings.durationShort);

    $('#boom-compilation-container')
        .css({
            width: 360 * ka.state.currentCompilationColumnSize
          , marginLeft: (1920 - (360 * ka.state.currentCompilationColumnSize) + 100) / 2
        })
        .velocity('transition.expandIn', {display: 'flex', duration: ka.settings.durationNormal, complete: function () {
            var coord = $('.boom-compilation-grid-item:first-child').offset();
            $('#boom-compilation-focus')
                .css({
                    top: coord.top + ka.settings.compilationPosterOffsetTop
                  , left: coord.left + ka.settings.compilationPosterOffsetLeft
                })
                .velocity('fadeIn', {duration: ka.settings.durationShort, complete: callback});
        }});
};


ka.lib.closeCompilation = function (callback) {
    ka.lib.grid.focus.fadeIn(ka.settings.durationNormal);

    var posterArray = ka.lib.getCurrentScreenPosters(ka.settings.gridMaxColumns);

    for (var index = 0; index < posterArray.length; index++) {
        if (posterArray[index] != null) {
            posterArray[index]
                .velocity({scaleX: 1, scaleY: 1, scaleZ: 1, opacity: 1}, {
                    duration: ka.settings.durationNormal
                  , progress: function(elements, percentComplete) {
                        elements[0].style.webkitFilter = 'blur(' + Math.round(3 - 3 * percentComplete) + 'px)'; /* TODO: optimize! */
                    }
                  , complete: function (elements) {
                        elements[0].style.webkitFilter = 'none';
                    }
                });
        }
    }

    $('.boom-movie-grid-key').slice(ka.state.gridPage * ka.settings.gridMaxRows, (ka.state.gridPage + 1) * ka.settings.gridMaxRows)
        .velocity({opacity: 1}, ka.settings.durationNormal);

    $('#boom-compilation-focus').velocity('fadeOut', ka.settings.durationShort);

    $('#boom-compilation-container').velocity('transition.expandOut', {display: 'none', duration: ka.settings.durationNormal, complete: function () {
        $('#boom-compilation-grid').empty();
        ka.state.currentCompilationPosterCount = 0;

        callback();
    }});
};


ka.lib.dissolveCompilation = function () {
    ka.state.actualScreenMode = null;
    ka.state.currentCompilationPosterCount = 0;

    $('#boom-movie-grid-container, #boom-grid-focus').velocity({left: '-=1920'}, 0);
    $('#boom-compilation-container, #boom-compilation-focus').velocity('fadeOut', {duration: 0, complete: function () {
        $('#boom-compilation-container, #boom-compilation-focus').velocity({left: '+=1920'}, 0);
    }});

    $('.boom-movie-grid-image').css('webkitFilter', '').velocity({scaleX: 1, scaleY: 1, scaleZ: 1, opacity: 1}, 0);
    $('.boom-movie-grid-key').velocity({opacity: 1}, 0);
    $('#boom-compilation-grid').empty();
};


ka.lib.getCurrentScreenPosters = function (maxColumn) {
    var elements = [], items = $('.boom-movie-grid-item'),
        start = ka.state.gridPage * ka.settings.gridMaxRows, end = (ka.state.gridPage + 1) * ka.settings.gridMaxRows,
        counter = ka.state.gridPage * ka.settings.gridMaxRows * ka.settings.gridMaxColumns;

    // TODO: OPTIMIZE!!!
    for (var row = start; row < end; row++) {
        if (row < ka.state.gridLookupMatrix.length) {
            for (var i = 0; i < maxColumn; i++) {
                elements.push(items.eq(counter).find('img'));
                counter++;
            }
            for (; i < ka.settings.gridMaxColumns; i++) {
                counter++;
            }
        }
    }

    return elements;
};


ka.lib.getGridFocusAbsoluteY = function () {
    return ka.settings.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY;
};


ka.lib.getItemsPerLineAtFocus = function () {
    return ka.state.gridLookupItemsPerLine[ka.lib.getGridFocusAbsoluteY()];
};


ka.lib.repositionFocusX = function (targetY) {
    var targetX = ka.state.gridLookupItemsPerLine[targetY] - 1,
        driftLeft = '-=' + 260 * (ka.state.gridFocusX - targetX);
    ka.state.gridFocusX = targetX;
    return driftLeft;
};


ka.lib.moveFocusX = function (offsetY) {
    var gridFocusAbsoluteY = ka.lib.getGridFocusAbsoluteY(),
        gridFocusTargetY = gridFocusAbsoluteY + offsetY;

    if (gridFocusTargetY > ka.state.gridLookupMatrix.length - 1) {
        gridFocusTargetY = ka.state.gridLookupMatrix.length - 1;
    }

    var itemsPerLineAtTarget = ka.state.gridLookupItemsPerLine[gridFocusTargetY];

    if (itemsPerLineAtTarget <= ka.state.gridFocusX) {
        return [{translateZ: 0, left: ka.lib.repositionFocusX(gridFocusTargetY)}, {duration: ka.settings.durationLong, easing: 'easeOutSine'}];
    } else {
        return null;
    }
};


ka.lib.getVariantFromGridFocus = function () {
     return ka.state.gridLookupMatrix[ka.lib.getGridFocusAbsoluteY()][ka.state.gridFocusX];
};


ka.lib.isCompilationAtFocus = function () {
  return $.isArray(ka.lib.getVariantFromGridFocus());
};


ka.lib.repositionMovieGrid = function () {
    $('#boom-movie-grid-container')
        .velocity({translateZ: 0, translateY: '-' + (ka.state.gridPage * 1080) + 'px'}, 0);
};


ka.lib.repositionMovieFocus = function (offscreen) {
    var top = 16 + 360 * ka.state.gridFocusY, left = 116 + 260 * ka.state.gridFocusX, display = 'block';
    if (offscreen) {
        left -= 1920;
        display = 'none';
    }

    $('#boom-grid-focus').velocity({top: top, left: left}, {duration: 0, display: display});
};


ka.lib.recalcPositionById = function (id) {
    var coordinates = ka.state.gridLookupCoordById[id];
    ka.state.gridPage = Math.floor(coordinates[1] / ka.settings.gridMaxRows);
    ka.state.gridFocusX = coordinates[0];
    ka.state.gridFocusY = coordinates[1] % ka.settings.gridMaxRows;
};
