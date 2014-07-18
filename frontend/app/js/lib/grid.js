/**
 *  Calculate and render movie grid.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.setPrimaryPosterColor = function () {
    var gridItem = $(this).closest('.boom-movie-grid-item'),
        uuid = gridItem.data('boom.uuid');
    if ('primaryPosterColor' in ka.data.cortex.byUuid[uuid]) {
        /*  Weird bug:
         *  Trigger full render of grid by painting every single poster on canvas.
         */
        var image = $(this).get(0),
            context = ka.state.canvasContext;

        context.canvas.width = image.width;
        context.canvas.height = image.height;
        context.drawImage(image, 0, 0, image.width, image.height);

        /* TODO: call callback here to remove loading spinner */

        gridItem.find('.boom-movie-grid-info-overlay-title').css('backgroundColor', '#' + ka.data.cortex.byUuid[uuid].primaryPosterColor);
    } else {
        var pixelArray = ka.lib.getPixelsFromImage($(this));
        pixelArray.unshift(uuid);
        ka.state.imagePosterPixelArrayBacklog.push(pixelArray);

        setTimeout(ka.lib.processPixelArray, 0);
    }
};


ka.lib.processPixelArray = function () {
    if (!ka.state.imagePosterPixelArrayBacklog.length) return;

    var nextPixelArray = ka.state.imagePosterPixelArrayBacklog.shift(),
        uuid = nextPixelArray.shift(),
        primaryColors = MMCQ.quantize(nextPixelArray, 5).palette(),
        colorLuminance = [
            ka.lib.getLuminance(primaryColors[0])
          , ka.lib.getLuminance(primaryColors[1])
          , ka.lib.getLuminance(primaryColors[2])
        ],
        primaryColorRGB = primaryColors[colorLuminance.indexOf(Math.min.apply(Math, colorLuminance))],
        primaryColorHex = ((1 << 24) + (primaryColorRGB[0] << 16) + (primaryColorRGB[1] << 8) + primaryColorRGB[2]).toString(16).slice(1);

    $('#boom-movie-grid-item-' + uuid + ' .boom-movie-grid-info-overlay-title').css('backgroundColor', '#' + primaryColorHex);
    ka.data.cortex.byUuid[uuid].primaryPosterColor = primaryColorHex;
    ka.state.imagePosterPrimaryColorByUuid[uuid] = primaryColorHex;

    $.get('/update/' + uuid + '/poster-color/' + primaryColorHex);
};


ka.lib.recalcMovieGrid = function () {
    ka.state.gridLookupMatrix = [];
    ka.state.gridLookupLinesByKey = {};
    ka.state.gridLookupKeyByLine = [];

    var keys = Object.getOwnPropertyNames(ka.data.cortex[ka.state.gridSortCriterion]).sort(), keyCount = keys.length;
    if (ka.state.gridSortOrder == 'desc') {
        keys.reverse();
    }

    var currentRowIndex = 0, currentColumnIndex, currentCellIndex = 0, currentLineIndex;
    for (var key, keyIndex = 0; keyIndex < keyCount; keyIndex++) {
        key = keys[keyIndex];
        if (key in ka.data.cortex[ka.state.gridSortCriterion]) {
            var items = ka.data.cortex[ka.state.gridSortCriterion][key], count = items.count();
            if (count) {
                currentColumnIndex = 0;
                for (var movieIndex = 0; movieIndex < count; movieIndex++) {
                    if (movieIndex % ka.settings.gridMaxColumns == 0) {
                        ka.state.gridLookupMatrix.push([]);
                    }

                    currentLineIndex =  ka.state.gridLookupMatrix.length - 1;
                    ka.state.gridLookupMatrix[currentLineIndex][currentColumnIndex] = items.values()[movieIndex];
                    ka.state.gridLookupKeyByLine[currentLineIndex] = key;

                    var currentLine = Math.floor(currentCellIndex / ka.settings.gridMaxColumns);
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

                    if (currentColumnIndex == ka.settings.gridMaxColumns) {
                        currentRowIndex++;
                        currentColumnIndex = 0;
                    }

                    if (currentRowIndex == ka.settings.gridMaxRows) {
                        currentRowIndex = 0;
                    }
                }

                if (currentColumnIndex) {
                    for (; currentColumnIndex < ka.settings.gridMaxColumns; currentColumnIndex++) {
                        ka.state.gridLookupMatrix[ka.state.gridLookupMatrix.length - 1][currentColumnIndex] = null;
                        currentCellIndex++;
                    }
                    currentRowIndex++;

                    if (currentRowIndex == ka.settings.gridMaxRows) {
                        currentRowIndex = 0;
                    }
                }
            }
        }
    }

    ka.state.gridTotalPages = Math.ceil(ka.state.gridLookupMatrix.length / ka.settings.gridMaxRows);
};


ka.lib.updateMovieGrid = function () {
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
                keyLabel.text(currentKey).attr('id', currentKey);
            } else{
                $('<span class="boom-movie-grid-key-label" id="boom-movie-grid-key-' + currentKey + '">' + currentKey + '</span>').appendTo(keyContainer);
            }

            lastKey = currentKey;
        } else {
            keyContainer.css('visibility', 'hidden');
        }

        for (var column = 0, line = matrix[row], columns = line.length; column < columns; column++) {
            movie = ka.state.gridLookupMatrix[row][column];
            if (movie !== null) {
                ka.state.gridLookupItemsPerLine[row] = column + 1;
            }
            if (!hasCells || currentCellIndex >= renderedCells.length) {
                ka.lib.renderMovieGridCell(movie, 'appendTo', $('#boom-movie-grid-container'));
            } else {
                if (renderedCells.eq(currentCellIndex).hasClass('empty')) {
                    ka.lib.renderMovieGridCell(movie, 'replaceWith', renderedCells.eq(currentCellIndex));
                } else {
                    if (movie === null || movie.uuid != renderedCells.eq(currentCellIndex).data('boom.uuid')) {
                        ka.lib.renderMovieGridCell(movie, 'insertAfter', renderedCells.eq(currentCellIndex));
                        detachedCell = renderedCells.eq(currentCellIndex).detach();
                        ka.state.detachedGridCells[renderedCells.eq(currentCellIndex).data('boom.uuid')] = detachedCell;
                        renderedCells = $('.boom-movie-grid-item').not(detachedCell);
                    }
                }
            }
            currentCellIndex++;
        }
    }

    /* After changing the sort order, superfluous items might still be rendered at the tail of the grid. */
    $('.boom-movie-grid-item').slice(currentCellIndex).remove();
    $('.boom-movie-grid-key').slice(ka.state.gridLookupMatrix.length).remove();

    if (ka.state.gridLookupMatrix.length) {
        if (ka.state.currentPageMode != 'detail') {
            ka.lib.updateDetailPage(); // TODO: prevent this from happening by repositioning focus
        }
        if (ka.state.currentPageMode == 'grid') {
            if (ka.state.shouldFocusFadeIn) {
                $('#boom-poster-focus').velocity('fadeIn', 720);
                ka.state.shouldFocusFadeIn = false;
            } else {
                $('#boom-poster-focus').css('display', 'block');
            }
        }
    }
};


ka.lib.renderMovieGridCell = function (movie, operation, context) {
    if (movie !== null) {
        if (movie.uuid in ka.state.detachedGridCells) {
            var cell = ka.state.detachedGridCells[movie.uuid];
        } else {
            var movieTitle = movie.titleOriginal;
            if (movieTitle.indexOf(':') > 9) {
                movieTitle = movieTitle.substr(0, movieTitle.indexOf(':') + 1) + '<br>' + movieTitle.substr(movieTitle.indexOf(':') + 1);
            }
            var cell = $(
                '<div class="boom-movie-grid-item">'
                  + '<div id="boom-movie-grid-item-' + movie.uuid + '" class="boom-movie-grid-info-overlay">'
                      + '<div class="boom-movie-grid-info-overlay-image">'
                          + '<img id="boom-poster-' + movie.uuid + '" src="/movie/poster/' + movie.uuid + '-200.image" width="200" height="300">'
                      + '</div>'
                      + '<div class="boom-movie-grid-info-overlay-text">'
                          + '<div class="boom-movie-grid-info-overlay-title">' + movieTitle + '</div>'
                          + '<div class="boom-movie-grid-info-overlay-text-additional">' + movie.releaseYear + '<br>' + movie.runtime + ' minutes</div>'
                      + '</div>'
                  + '</div>'
              + '</div>'
            ).data('boom.uuid', movie.uuid);

            cell.find('img').on('load', ka.lib.setPrimaryPosterColor);
        }
    } else {
        var cell = $('<div class="boom-movie-grid-item empty"></div>');
    }

    if (operation == 'replaceWith') {
        context.replaceWith(cell);
    } else {
        cell[operation](context);
    }

    if (movie !== null && movie.uuid in ka.state.detachedGridCells) {
        delete ka.state.detachedGridCells[movie.uuid];
    }
};


ka.lib.scrollGrid = function () {
    $('#boom-movie-grid-container').velocity({translateZ: 0, translateY: '-' + (ka.state.gridPage * 1080) + 'px'}, {duration: 720, easing: 'ease-out'});
};


ka.lib.moveFocusFirstItem = function () {
    if (ka.state.gridFocusX > 0) {
        var distance = 260 * ka.state.gridFocusX;
        ka.state.gridFocusX = 0;

        $('#boom-poster-focus').css('display', 'block').velocity({left: '-=' + distance}, 260);
    }
};


ka.lib.moveFocusLastItem = function () {
    var items = ka.lib.getItemsPerLineAtFocus();
    if (ka.state.gridFocusX < items - 1) {
        var distance = 260 * (items - ka.state.gridFocusX - 1);
        ka.state.gridFocusX = items - 1;

        $('#boom-poster-focus').css('display', 'block').velocity({left: '+=' + distance}, 260);
    }
};


ka.lib.moveFocusPageUp = function () {
    if (ka.state.gridPage > 0) {
        /* ka.lib.moveFocusX(-ka.settings.gridMaxRows); */
        var transition = ka.lib.moveFocusX(-ka.settings.gridMaxRows);
        if (transition !== null) {
            $('#boom-poster-focus').velocity(transition[0], transition[1]);
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
        ka.lib.scrollGrid();

        if (ka.state.gridFocusY > 0 && ka.lib.getGridFocusAbsoluteY() >= ka.state.gridLookupMatrix.length) {
            var overshoot = ka.lib.getGridFocusAbsoluteY() - ka.state.gridLookupMatrix.length + 1,
                offsetY = overshoot * 360;
            ka.state.gridFocusY -= overshoot;

            transitionY = [{top: '-=' + offsetY}, {duration: offsetY}];
        }

        if (transitionX !== null && transitionY !== null) {
            $('#boom-poster-focus').velocity(
                {left: transitionX[0].left, top: transitionY[0].top}
              , {easing: 'easeOutSine', duration: Math.max(transitionX[1].duration, transitionY[1].duration)}
            );
        } else if (transitionX !== null) {
            $('#boom-poster-focus').velocity({left: transitionX[0].left}, {easing: 'easeOutSine', duration: transitionX[1].duration});
        } else if (transitionY !== null) {
            $('#boom-poster-focus').velocity({top: transitionY[0].top}, {easing: 'ease-out', duration: transitionY[1].duration});
        }
    }
};


ka.lib.moveFocusUp = function () {
    var gridFocusAbsoluteY = ka.lib.getGridFocusAbsoluteY(),
        notFirstRow = ka.state.gridFocusY > 0,
        notFirstPage = ka.state.gridPage > 0;

    if (gridFocusAbsoluteY > 0 && (notFirstRow || notFirstPage)) {
        var props = {}, options = {};

        if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY - 1] <= ka.state.gridFocusX) {
            props.left = ka.lib.repositionFocusX(gridFocusAbsoluteY - 1);

            options.easing = 'easeOutSine';
        } else {
            options.easing = 'ease-out';
        }

        if (notFirstRow) {
            props.top = '-=360';
            options.duration = 360;

            ka.state.gridFocusY -= 1;
        } else {
            props.top = '+=720';
            options.duration = 720;

            ka.state.gridFocusY = ka.settings.gridMaxRows - 1;
            ka.state.gridPage -= 1;
            ka.lib.scrollGrid();
        }

        $('#boom-poster-focus').velocity(props, options);
    }
};


ka.lib.moveFocusDown = function () {
    var gridFocusAbsoluteY = ka.lib.getGridFocusAbsoluteY(),
        notLastRow = ka.state.gridFocusY + 1 < ka.settings.gridMaxRows,
        notLastPage = ka.state.gridPage + 1 < ka.state.gridTotalPages;

    if (gridFocusAbsoluteY + 1 < ka.state.gridLookupMatrix.length && (notLastRow || notLastPage)) {
        var props = {}, options = {};

        if (ka.state.gridLookupItemsPerLine[gridFocusAbsoluteY + 1] <= ka.state.gridFocusX) {
            props.left = ka.lib.repositionFocusX(gridFocusAbsoluteY + 1);

            options.easing = 'easeOutSine';
        } else {
            options.easing = 'ease-out';
        }

        if (notLastRow) {
            props.top = '+=360';
            options.duration = 360;

            ka.state.gridFocusY += 1;
        } else {
            props.top = '-=720';
            options.duration = 720;

            ka.state.gridFocusY = 0;
            ka.state.gridPage += 1;
            ka.lib.scrollGrid();
        }

        $('#boom-poster-focus').velocity(props, options);
    }
};


ka.lib.moveFocusLeft = function () {
    if (ka.state.gridFocusX > 0) {
        ka.state.gridFocusX -= 1;

        $('#boom-poster-focus').css('display', 'block').velocity({left: '-=260'}, 260);
    }
};


ka.lib.moveFocusRight = function () {
    if (ka.state.gridFocusX < ka.settings.gridMaxColumns - 1 && ka.state.gridFocusX + 1 < ka.lib.getItemsPerLineAtFocus()) {
        ka.state.gridFocusX += 1;

        $('#boom-poster-focus').css('display', 'block').velocity({left: '+=260'}, 260);
    }
};


ka.lib.toggleFocus = function () {
    var uuid = ka.state.gridLookupMatrix[ka.lib.getGridFocusAbsoluteY()][ka.state.gridFocusX].uuid;

    $('#boom-movie-grid-item-' + uuid)
        .toggleClass('active')
        .find('.boom-movie-grid-info-overlay-title').text(ka.lib.getLocalizedTitleByUuid(uuid));
};


ka.lib.selectFocus = function () {
    ka.state.currentPageMode = 'detail';
    ka.state.currentDetailButton = 0;

    ka.lib.updateDetailPage();
    ka.lib.updateDetailButtonSelection();

    $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, 720);
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
        return [{left: ka.lib.repositionFocusX(gridFocusTargetY)}, {duration: 720, easing: 'easeOutSine'}];
    } else {
        return null;
    }
};


ka.lib.getMovieFromGridFocus = function () {
    return ka.state.gridLookupMatrix[ka.lib.getGridFocusAbsoluteY()][ka.state.gridFocusX];
};
