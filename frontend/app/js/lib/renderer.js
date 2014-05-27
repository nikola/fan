/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

ka.lib.renderMovieThumbnail = function () {
    var keys = ['123'].concat('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')), key;

    var filledLines = 0, itemsPerLine, startSection = true, tablePerKey;

    for (var index = 0; index < 27; index++) {
        key = keys[index];
        if (key in ka.data.cortex.byLetter) {
            var movies = ka.data.cortex.byLetter[key];
            if (movies.count()) {
                // console.log('processing ' + movies.count() + ' movies starting with ' + key);
                itemsPerLine = 0;
                tablePerKey = -1;
                for (var m = 0; m < movies.values().length; m++) {
                    // console.log('    movie # ' + m);
                    if (startSection) {

                        // console.log('        creating new <section>');
                        var section = $('<section>', {
                            class: 'boom-movie-grid-page'
                        }).appendTo($('body'));
                    }

                    if (m == 0 || startSection) {
                        tablePerKey++;
                        // console.log('        creating new <table>');
                        var table = $('<table>', {
                            id: 'boom-movie-grid-table-' + key + '-' + tablePerKey
                          , class: 'boom-movie-grid-table'
                        }).appendTo(section);
                    }

                    startSection = false;

                    if (m % 6 == 0) {
                        // console.log('        creating new <tr>');
                        var row = $('<tr>', {
                            class: 'boom-movie-grid-line'
                        }).appendTo(table);
                    }

                    // console.log('        creating new <td>');
                    var cell = $('<td>', {
                        id: 'boom-movie-grid-item-' + movies.values()[m].uuid
                      , class: 'boom-movie-grid-item'
                      // , text: movies.values()[m].titleOriginal
                    }).appendTo(row);

                    $('<img>', {
                        src: 'https://127.0.0.1:' + HTTP_PORT + '/movie/poster/' + movies.values()[m].uuid + '.jpg/150'
                    }).appendTo(cell);


                    itemsPerLine += 1;

                    // console.log('        items per line: ' + itemsPerLine);

                    if (itemsPerLine == 6) {
                        filledLines += 1;

                        // console.log('        lines filled: ' + filledLines);

                        itemsPerLine = 0;
                    }

                    if (filledLines == 4) {
                        startSection = true;
                        filledLines = 0;
                    }

                }

                for (var c = itemsPerLine; c < 6; c++) {
                    $('<td>', {
                        class: 'boom-movie-grid-item'
                    }).appendTo(row);
                }


                filledLines += 1;

                if (filledLines == 4) {
                    startSection = true;
                    filledLines = 0;
                }
            }
        }
    }



};
