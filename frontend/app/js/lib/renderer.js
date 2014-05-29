/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

ka.lib.renderMovieThumbnail = function () {
    var ITEMS_PER_LINE = 7, LINES_PER_PAGE = 3;

    var keys = ['123'].concat('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')), key;

    var filledLines = 0, lastFilledLines = null, itemsPerLine, startSection = true, tablePerKey, letterIndicator, indicatorFlipFlop = false;

    for (var index = 0; index < 27; index++) {
        key = keys[index];
        if (key in ka.data.cortex.byLetter) {
            var movies = ka.data.cortex.byLetter[key];
            if (movies.count()) {
                // console.log('processing ' + movies.count() + ' movies starting with ' + key);
                itemsPerLine = 0;
                tablePerKey = -1;
                for (var m = 0; m < movies.values().length; m++) {

                    // if (m == 0) console.log(key, lastFilledLines)

                    if (lastFilledLines !== null && (m == 0 || startSection)) {
                        // console.log($(letterIndicator.css)
                        /* Update height of letter indicator. */
                        letterIndicator.css('height', lastFilledLines * 360);

                        /* if (indicatorFlipFlop) {
                             letterIndicator.css('background-color', 'red');
                        } else {
                            letterIndicator.css('background-color', 'green');
                        }
                        indicatorFlipFlop = !indicatorFlipFlop; */
                    }

                    // console.log('    movie # ' + m);
                    if (startSection) {
                        // console.log('        creating new <section>');
                        var section = $('<section>', {
                            class: 'boom-movie-grid-page'
                        }).appendTo($('#content'));
                    }

                    if (m == 0 || startSection) {


                        tablePerKey++;
                        // console.log('        creating new <table>');
                        letterIndicator = $('<table class="boom-movie-grid-letter-indicator"><tr><td class="boom-movie-grid-letter-cell"></td></tr></table>', {
                            // class: 'boom-movie-grid-letter-indicator'
                        }).appendTo(section);

                        $('<span>', {
                            class: 'boom-movie-grid-letter-indicator-text'
                          , text: key
                        }).appendTo(letterIndicator.find('td'));

                        // console.log(letterIndicator.style)

                        var table = $('<table>', {
                            id: 'boom-movie-grid-table-' + key + '-' + tablePerKey
                          , class: 'boom-movie-grid-table'
                        }).appendTo(section);

                        lastFilledLines = 0;
                    }

                    startSection = false;

                    if (m % ITEMS_PER_LINE == 0) {
                        // console.log('        creating new <tr>');
                        var row = $('<tr>', {
                            class: 'boom-movie-grid-line'
                        }).appendTo(table);
                        lastFilledLines++;
                    }

                    // console.log('        creating new <td>');
                    var cell = $('<td>', {
                        id: 'boom-movie-grid-item-' + movies.values()[m].uuid
                      , class: 'boom-movie-grid-item'
                      // , text: movies.values()[m].titleOriginal
                    }).appendTo(row);

                    var title = movies.values()[m].titleOriginal;
                    if (title.indexOf(':') > 9) {
                        title = title.substr(0, title.indexOf(':') + 1) + '<br>' + title.substr(title.indexOf(':') + 1);
                    }

                    var hover = $('<div class="ih-item square effect6 top_to_bottom"><a href="#"><div class="img"></div><div class="info"><h3>' + title + '</h3><p>' + movies.values()[m].releaseYear + '</p></div></a></div>').appendTo(cell);

                    $('<img>', {
                        src: 'https://127.0.0.1:' + HTTP_PORT + '/movie/poster/' + movies.values()[m].uuid + '.jpg/200'
                      , width: 200
                      , height: 300
                    // }).appendTo(cell);
                    }).appendTo(hover.find('.img'));

                    /*
                    <!-- normal -->
    <div class="ih-item square effect6 top_to_bottom"><a href="#">
        <div class="img"><img src="images/assets/rect/5.jpg" alt="img"></div>
        <div class="info">
          <h3>Heading here</h3>
          <p>Description goes here</p>
        </div></a></div>
    <!-- end normal -->
                    */



                    /* $('<span>', {
                        class: 'boom-movie-grid-item-title'
                      , text: movies.values()[m].titleOriginal
                    }).appendTo(cell); */


                    itemsPerLine += 1;



                    // console.log('        items per line: ' + itemsPerLine);

                    if (itemsPerLine == ITEMS_PER_LINE) {
                        filledLines += 1;

                        // console.log('        lines filled: ' + filledLines);

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
                }


                if (itemsPerLine) {
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

    $('#content').onepage_scroll({
       sectionContainer: "section",     // sectionContainer accepts any kind of selector in case you don't want to use section
       // easing: "cubic-bezier(0.445, 0.050, 0.550, 0.950)",                  // Easing options accepts the CSS3 easing animation such "ease", "linear", "ease-in",
                                        // "ease-out", "ease-in-out", or even cubic bezier value such as "cubic-bezier(0.175, 0.885, 0.420, 1.310)"
       easing: 'ease',
       animationTime: 750,             // AnimationTime let you define how long each section takes to animate
       pagination: false,                // You can either show or hide the pagination. Toggle true for show, false for hide.
       updateURL: false,                // Toggle this true if you want the URL to be updated automatically when the user scroll to each page.
       // beforeMove: function(index) {},  // This option accepts a callback function. The function will be called before the page moves.
       // afterMove: function(index) {},   // This option accepts a callback function. The function will be called after the page moves.
       loop: false,                     // You can have the page loop back to the top/bottom when the user navigates at up/down on the first/last page.
       keyboard: true,                  // You can activate the keyboard controls
       responsiveFallback: false        // You can fallback to normal page scroll by defining the width of the browser in which
                                        // you want the responsive fallback to be triggered. For example, set this to 600 and whenever
                                        // the browser's width is less than 600, the fallback will kick in.
    });

};
