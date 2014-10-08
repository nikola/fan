/**
 *  Render movie detail page items.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.browser = {

    isHidden: function () {
        return $('#boom-detail-panel').data('boom.isHidden');
    }

  , isExpanded: function () {
        return $('#boom-detail-panel').data('boom.isExpanded');
    }

  , setExpanded: function () {
        $('#boom-detail-panel').data('boom.isExpanded', true);
    }

  , setContracted: function () {
        $('#boom-detail-panel').data('boom.isExpanded', false);
    }

  , setupExpansion: function () {
        if (!ka.lib.browser.isExpanded() && !ka.lib.browser.isHidden()) {
            var selectedPoster = $('#boom-detail-browser :nth-child(' + (ka.state.currentDetailBrowserPosterColumn + 2) + ')'),
                snapshot = ka.lib.grid.getMovieListSnapshot(),
                movieObj = snapshot[selectedPoster.data('boom.index')];
            ka.lib.browser.poster.setSource(movieObj.keyPoster);
            ka.lib.browser.expandUp();
            /* $('#boom-detail-large-poster').css('right', 1920 - selectedPoster.offset().left - 150).attr('src', selectedPoster.attr('src').replace('-150.image', '-300.image')); */
        }
    }

  , expandUp: function () {
        ka.state.currentPageMode = 'limbo';

        $('#boom-detail-title').velocity({translateZ: 0, width: 1580, height: '-=100'}, ka.settings.durationNormal);
        $('#boom-detail-collection').velocity({translateZ: 0, bottom: '+=100', opacity: 0}, {duration: ka.settings.durationNormal, display: 'none'});

        $('#boom-detail-storyline').velocity({translateZ: 0, top: '-=120'}, ka.settings.durationNormal);

        $('#boom-detail-browser, #boom-detail-focus').velocity({translateZ: 0, bottom: '+=247px', opacity: 0}, {display: 'none', duration: ka.settings.durationNormal});

        $('#boom-detail-panel').velocity({translateZ: 0, bottom: 0}, {duration: ka.settings.durationNormal, complete: function () {
            ka.lib.browser.setExpanded();
            ka.state.currentPageMode = 'detail';
        }});
    }

  , contractDown: function () {
        if (ka.lib.browser.isExpanded()) {
            ka.state.currentPageMode = 'limbo';

            ka.lib.browser.poster.slideDown();

            $('#boom-detail-title').velocity({translateZ: 0, width: 1049, height: '+=100'}, ka.settings.durationNormal);
            $('#boom-detail-collection').css('display', 'inline-block').velocity({translateZ: 0, bottom: '-=100', opacity: 1}, ka.settings.durationNormal);

            $('#boom-detail-storyline').velocity({translateZ: 0, top: '+=120'}, ka.settings.durationNormal);

            $('#boom-detail-browser').css('display', 'inline-block').velocity({translateZ: 0, bottom: '-=247px', opacity: 1}, ka.settings.durationNormal);
            $('#boom-detail-focus').css('display', 'inline-block').velocity({translateZ: 0, bottom: [226, 473], opacity: 1}, ka.settings.durationNormal);

            $('#boom-detail-panel').velocity({translateZ: 0, bottom: -223}, {duration: ka.settings.durationNormal, complete: function () {
                ka.lib.browser.setContracted();
                ka.state.currentPageMode = 'detail';
            }});
        }
    }

  , show: function () {
        $('#boom-movie-detail').css('display', 'block');
    }

  , toggle: function () {
        var isHidden = $('#boom-detail-panel').data('boom.isHidden'),
            direction = isHidden ? '+' : '-',
            distance = ka.lib.browser.isExpanded() ? 470 : 247;

        $('#boom-detail-panel').data('boom.isHidden', !isHidden);

        ka.state.currentPageMode = 'limbo';
        var toggleElements = '#boom-detail-panel';
        if (!ka.lib.browser.isExpanded()) {
            /* toggleElements += ', #boom-detail-focus'; */
        }
        $(toggleElements).velocity({translateZ: 0, bottom: direction + '=' + distance}, {duration: ka.settings.durationNormal, complete: function () {
            ka.state.currentPageMode = 'detail';
        }});
    }

  , focus: {

        reposition: function () {
            $('#boom-detail-focus').velocity({left: 1110 + 2 + 160 * ka.state.currentDetailBrowserPosterColumn}, 0);
        }

    }

  , poster: {

        setSource: function (key) {
            $('#boom-detail-large-poster').attr('src', '/movie/poster/' + key + '-300.image');
        }

      , onLoaded: function () {
            /* if (ka.lib.browser.isExpanded()) {
                ka.lib.browser.poster.slideUp();
            } else {
                ka.lib.browser.expandUp();
            } */
            ka.lib.browser.poster.slideUp();
        }

      , hide: function () {
            $('#boom-detail-large-poster').attr('src', '').velocity({bottom: '-=490'}, {duration: 0, display: 'none'});
        }

      , slideUp: function () {
            $('#boom-detail-large-poster').css('display', 'block').velocity({bottom: '+=490'}, ka.settings.durationNormal);
        }

      , slideDown: function () {
            $('#boom-detail-large-poster').velocity({bottom: '-=490'}, {duration: ka.settings.durationNormal, display: 'none', complete: function () {
                $(this).attr('src', '');
            }});
        }

    }

  , backdrop: {

        init: function () {
            return $('.boom-movie-detail-poster-loader').css('opacity', 0);
        }

      , clear: function () {
            $('#boom-movie-detail').css('backgroundImage', 'none');
        }

      , setImmediate: function (movieObj) {
            $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + movieObj.keyBackdrop + '.jpg)');
        }

      , loadOptimistic: function (movieObj) {
            $('#boom-movie-detail-poster-foreground')
                .css('opacity', 0)
                .data({
                    'boom.isCached': movieObj.isBackdropCached
                  , 'boom.uuid': movieObj.uuid
                })
                .attr('src', '/movie/backdrop/' + movieObj.keyBackdrop +  '.jpg');
        }

      , loadPessimistic: function (movieObj) {
            if (movieObj.isBackdropCached) {
                ka.lib.browser.backdrop.loadOptimistic(movieObj);
            } else {
                if (!$('#boom-movie-detail-poster-background').data('boom.isDefocused')) {
                    ka.state.uncachedBackdropDelayTimer = setTimeout(function () {
                        $('#boom-movie-detail-poster-foreground').css('opacity', 0);
                        $('#boom-movie-detail-poster-background').css('opacity', 1).data('boom.isDefocused', true);
                        ka.lib.browser.backdrop.clear();
                        ka.lib._focusOutImage($('#boom-movie-detail-poster-background'));
                    }, ka.settings.durationShort);
                }

                ka.lib.browser.backdrop.loadOptimistic(movieObj);
            }
        }

      , onLoaded: function () {
            clearTimeout(ka.state.uncachedBackdropDelayTimer);
            $('#boom-movie-detail-poster-background').velocity('stop');

            $('#boom-movie-detail-poster-foreground').velocity({translateZ: 0, opacity: 1}, {duration: 360, complete: function () {
                $('#boom-movie-detail').css('backgroundImage', 'url(' + $(this).attr('src') + ')');

                $('#boom-movie-detail-poster-background')
                    .attr('src', $('#boom-movie-detail-poster-foreground').attr('src'))
                    .data('boom.isDefocused', false)
                    .get(0).style.webkitFilter = null;

                if (!$(this).data('boom.isCached')) {
                    var uuid = $(this).data('boom.uuid');
                    ka.data.byUuid[uuid].isBackdropCached = true;
                    $.get('/movie/' + uuid + '/set-backdrop-cached');
                }
            }});
        }

    }

  , posters: {

        show: function (callback) {
            $('#boom-detail-focus').velocity({bottom: -21}, {duration: 0, complete: function () {
                $('#boom-detail-focus').css('display', 'block').velocity({bottom: 226}, ka.settings.durationNormal);
                $('#boom-detail-browser').css('display', 'inline-block').velocity({bottom: '+=247'}, {
                    duration: ka.settings.durationNormal
                  , complete: callback
                });
            }});
        }

      , fadeUp: function () {
            $('#boom-detail-browser').velocity({bottom: '+=' + 247, opacity: 0}, 0);
            $('#boom-detail-focus').velocity({bottom: 473, opacity: 0}, 0);

            ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

            ka.lib.browser.focus.reposition();
        }

    }

};


ka.lib.updateDetailPage = function (movie, skipBackdropUpdate, noCollection) {
    if (!movie) {
        return;
    }

    $('#boom-movie-detail').data('boom.uuid', movie.uuid);

    /*
    if (!movie.streamless) {
        ka.state.currentDetailButton = 'play';
    } else if (movie.trailer) {
        ka.state.currentDetailButton = 'trailer';
    } else {
        ka.state.currentDetailButton = 'details';
    }

    $('#boom-movie-detail .boom-button').data('boom.select-color', movie.primaryPosterColor || '000000');

    $('#boom-detail-release span').text(movie.releaseYear);
    $('#boom-detail-runtime span').text(movie.runtime);
    $('#boom-detail-rating span').text((movie.rating) ? (movie.rating / 10) : '?');
    $('#boom-movie-detail-title').text(ka.lib.getLocalizedTitle(movie, false, noCollection));
    $('#boom-movie-detail-description').text(movie.storyline);

    $('#boom-movie-detail-play-button').css('display', (movie.streamless) ? 'none' : 'inline-block');
    $('#boom-movie-detail-trailer-button').css('display', (movie.trailer) ? 'inline-block' : 'none');

    var poster = $('#boom-movie-detail-top img')
    if (poster.data('boom.ikeyBackdrop') != movie.uuid) {
        if (!skipBackdropUpdate) {
            $('#boom-movie-detail').css('backgroundImage', 'none');
        }

        poster.css('visibility', 'hidden').data({'boom.isLoading': true, 'boom.keyBackdrop': movie.keyBackdrop})
            .on('load', function () {
                if (poster.data('boom.isLoading')) {
                    poster.data('boom.isLoading', false).css('visibility', 'visible').off();
                    if (!skipBackdropUpdate) {
                        $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + poster.data('boom.keyBackdrop') + '.jpg)');
                    }
                }
            })
            .attr('src', '/movie/poster/' + movie.keyPoster + '-300.image');
    }
    */

};


ka.lib.updateDetailButtonSelection = function (skipAnimation) {
    $('#boom-detail-button-group .boom-active').removeClass('boom-active')
        .css('backgroundColor', 'transparent');

    var button = $('#boom-movie-detail-' + ka.state.currentDetailButton + '-button');
    button.addClass('boom-active')
        .css('backgroundColor', '#' + button.data('boom.select-color'));

    if (!skipAnimation) {
        if (ka.state.currentDetailButton == 'details') {
            $('#boom-movie-detail-shade').velocity({translateZ: 0, opacity: 0.75}, {duration: ka.settings.durationNormal});
            $('#boom-movie-detail-description').velocity('transition.expandIn', {duration: ka.settings.durationNormal, display: 'flex'});
        } else {
            $('#boom-movie-detail-shade').velocity({translateZ: 0, opacity: 0}, ka.settings.durationNormal);
            $('#boom-movie-detail-description').velocity('transition.expandOut', ka.settings.durationNormal);
        }
    }
};


ka.lib.startTrailerPlayer = function (id) {
    ka.state.movieTrailerPlayer.loadVideoById({
        videoId: id
      , suggestedQuality: 'hd1080'
    });
    ka.state.movieTrailerPlayer.playVideo();
    ka.state.movieTrailerPlayer.setPlaybackQuality('hd1080');
};


ka.lib.closeTrailerPlayer = function () {
    ka.state.movieTrailerPlayer.stopVideo();
    ka.state.movieTrailerPlayer.clearVideo();

    ka.state.currentPageMode = 'detail';

    $('#boom-movie-trailer').css('display', 'none');

    $('#boom-movie-grid-container').css('display', 'block');

    $('#boom-movie-detail').velocity('fadeIn', ka.settings.durationNormal);

    window.focus();
};


ka.lib._addBrowserGridImage = function (keyPoster, index, unselected) {
    var css = {webkitTransform: 'translate3d(0, 0, 0)'};
    if (unselected) {
        /* css.webkitFilter = 'grayscale(100%) opacity(0.5)'; */
        css.webkitFilter = 'saturate(0%) opacity(0.5)';
    }

    if (keyPoster in ka.state.detachedBrowserPosterByKey) {
        return ka.state.detachedBrowserPosterByKey[keyPoster].appendTo('#boom-detail-browser').data('boom.index', index);
    } else {
        return $('<img>', {
            src: '/movie/poster/' + keyPoster + '-150.image'
          , width: 150
          , height: 225
          , data: {'boom.index': index}
          , css: css
        }).appendTo('#boom-detail-browser');
    }
};

ka.lib._addBrowserGridDummy = function () {
    return $('<img>', {
        width: 0
      , height: 225
      , css: {
            /* webkitFilter: 'grayscale(100%) opacity(0.5)' */
            webkitFilter: 'saturate(0%) opacity(0.5)'
          , webkitTransform: 'translate3d(0, 0, 0)', marginLeft: 0
        }
    }).prependTo('#boom-detail-browser');
};


ka.lib.populateDetailBrowserGrid = function () {
    $('#boom-detail-browser').empty();
    $('<img>', {
          width: 150
        , height: 225
        , css: {
            /* webkitFilter: 'grayscale(100%) opacity(0.5)' */
            webkitFilter: 'saturate(0%) opacity(0.5)'
          , webkitTransform: 'translate3d(0, 0, 0)'
        }
    }).appendTo('#boom-detail-browser');

    var current = ka.lib.grid.getMovieIndexSnapshot()[$('#boom-movie-detail').data('boom.uuid')],
        index, end, focused,
        movieList = ka.lib.grid.getMovieListSnapshot();

    if (movieList.length < 6) {
        index = 0;
        end = movieList.length;
        focused = current;
    } else {
        index = current - 2;
        if (index < 0) {
            focused = 2 + index;
            index = 0;
        } else {
            focused = 2;
        }
        end = index + 5;
        if (end > movieList.length) {
            if (focused == 2 && movieList.length > 5) {
                focused = 2 + end - movieList.length;
                index -= end - movieList.length;
            }
            end = movieList.length;
        }
    }

    do {
        ka.lib._addBrowserGridImage(movieList[index].keyPoster, index, index != current);
    } while (++index < end);

    /* Pre-cache previous/next posters. */
    var lookBehindIndex = index - 3, lookAheadIndex = index + 3;
    if (lookBehindIndex > -1) {
        new Image().src = '/movie/poster/' + movieList[lookBehindIndex].keyPoster + '-150.image';
    }
    if (lookAheadIndex < movieList.length) {
        new Image().src = '/movie/poster/' + movieList[lookAheadIndex].keyPoster + '-150.image';
    }

    return focused;
};


ka.lib.updateDetailBrowserInfo = function (movieObj, fade) {
    if (fade) {
        setTimeout(function () {
            ka.lib._updateDetailBrowserInfo(movieObj);
        }, ka.settings.durationShort);
    } else {
        ka.lib._updateDetailBrowserInfo(movieObj);
    }
};


ka.lib._updateDetailBrowserInfo = function (movieObj) {
    $('#boom-movie-detail').data('boom.uuid', movieObj.uuid);

    var title = (ka.state.gridSortDisplayLanguage == 'localized') ? movieObj.titleLocalized : movieObj.titleOriginal,
        rating = ((movieObj.rating) ? (movieObj.rating / 10) : '?') + '/10',
        collectionName = (movieObj.isCompiled) ? (movieObj.compilation + ' Collection') : '';

    $('#boom-detail-title').text(title);
    $('#boom-detail-collection').html(collectionName || '&nbsp;');

    if (rating.length == 4) {
        rating = rating.replace('/', '.0/');
    }
    $('#boom-detail-release').text(movieObj.releaseYear);
    $('#boom-detail-rating').text(rating);
    $('#boom-detail-runtime').text(movieObj.runtime + ' min');
    $('#boom-detail-genres').text(movieObj.genres || '');

    /*
    if (ka.lib.browser.isExpanded() && !collectionName) {
        $('#boom-detail-collection').text(movieObj.genres || '');
        $('#boom-detail-genres').text('');
    } else {
        $('#boom-detail-collection').text(collectionName);
        $('#boom-detail-genres').text(movieObj.genres || '');
    }
    */


    $('#boom-detail-storyline').text(movieObj.storyline);
};


ka.lib.moveDetailBrowserLeft = function () {
    var column = ka.state.currentDetailBrowserPosterColumn,
        posters = $('#boom-detail-browser img'),
        currentPosterIndex = posters.eq(column + 1).data('boom.index'),
        firstPosterIndex = posters.eq(1).data('boom.index'),
        snapshot = ka.lib.grid.getMovieListSnapshot();

    if (column > 2 || (firstPosterIndex == 0 && column > 0)) {
        ka.state.currentPageMode = 'limbo';

        ka.lib.browser.backdrop.loadPessimistic(snapshot[currentPosterIndex - 1]);
        setTimeout(function () {
            ka.lib._triggerBrowserUpdate(snapshot[currentPosterIndex - 1]);
            ka.lib._moveDetailBrowserFocus(posters.eq(column + 1), posters.eq(column), '-=160');
            ka.state.currentDetailBrowserPosterColumn -= 1;
        }, ka.settings.durationUltraShort);
    } else if (firstPosterIndex > 0) {
        ka.state.currentPageMode = 'limbo';

        var keyPoster = snapshot[firstPosterIndex - 1].keyPoster;
        if (keyPoster in ka.state.detachedBrowserPosterByKey) {
            posters.eq(0).replaceWith(ka.state.detachedBrowserPosterByKey[keyPoster].data('boom.index', firstPosterIndex - 1));
        } else {
            posters.eq(0).attr('src', '/movie/poster/' + keyPoster + '-150.image').data('boom.index', firstPosterIndex - 1);
        }

        ka.lib.browser.backdrop.loadPessimistic(snapshot[currentPosterIndex - 1]);
        setTimeout(function () {
            ka.lib._triggerBrowserUpdate(snapshot[firstPosterIndex + 1]);
            ka.lib._animatePosterMove(
                 ka.lib._addBrowserGridDummy()
              , {translateZ: 0, width: 150, marginLeft: 10}
              , $('#boom-detail-browser img').eq(6)
              , posters.eq(3).get(0)
              , posters.eq(2).get(0)
            );
        }, ka.settings.durationUltraShort);
    }
};


ka.lib.moveDetailBrowserRight = function () {
    var column = ka.state.currentDetailBrowserPosterColumn,
        posters = $('#boom-detail-browser img'),
        currentPosterIndex = posters.eq(column + 1).data('boom.index'),
        lastPosterIndex = posters.last().data('boom.index'),
        snapshot = ka.lib.grid.getMovieListSnapshot();

    if ((column < 2 && snapshot.length > 2) || (lastPosterIndex == snapshot.length - 1 && lastPosterIndex - currentPosterIndex > 0)) {
        ka.state.currentPageMode = 'limbo';

        ka.lib.browser.backdrop.loadPessimistic(snapshot[currentPosterIndex + 1]);

        setTimeout(function () {
            ka.lib._triggerBrowserUpdate(snapshot[currentPosterIndex + 1]);
            ka.lib._moveDetailBrowserFocus(posters.eq(column + 1), posters.eq(column + 2), '+=160');
            ka.state.currentDetailBrowserPosterColumn += 1;
        }, ka.settings.durationUltraShort);
    } else if (posters.length == 6 && lastPosterIndex + 1 < snapshot.length) {
        ka.state.currentPageMode = 'limbo';

        ka.lib._addBrowserGridImage(snapshot[lastPosterIndex + 1].keyPoster, lastPosterIndex + 1, true);

        ka.lib.browser.backdrop.loadPessimistic(snapshot[lastPosterIndex - 1]);

        setTimeout(function () {
            ka.lib._triggerBrowserUpdate(snapshot[lastPosterIndex - 1]);
            ka.lib._animatePosterMove(
                posters.eq(0)
              , {translateZ: 0, width: 0, marginLeft: 0}
              , posters.eq(0)
              , posters.eq(3).get(0)
              , posters.eq(4).get(0)
            );
        }, ka.settings.durationUltraShort);
    }
};


ka.lib._moveDetailBrowserFocus = function (currentElement, targetElement, focusOffset) {
    ka.lib._focusOutImage(currentElement);
    ka.lib._focusInImage(targetElement);

    $('#boom-detail-focus').velocity({translateZ: 0, left: focusOffset}, {duration: ka.settings.durationNormal, complete: function () {
        ka.state.currentPageMode = 'detail';
    }});
};


ka.lib._animatePosterMove = function (animateElement, animateProperties, removeElement, previouslyFocusedPoster, upcomingFocusedPoster) {
    animateElement.velocity(animateProperties, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            if (percentComplete < 1) {
                previouslyFocusedPoster.style.webkitFilter = 'saturate(' + (100 - Math.round(percentComplete * 100)) + '%) opacity(' + Math.round(100 - 50 * percentComplete) / 100 + ')';
                upcomingFocusedPoster.style.webkitFilter = 'saturate(' + Math.round(percentComplete * 100) + '%) opacity(' + Math.round(50 + 50 * percentComplete) / 100 + ')';
            }
        }
      , complete: function () {
            previouslyFocusedPoster.style.webkitFilter = 'saturate(0%) opacity(0.5)';
            upcomingFocusedPoster.style.webkitFilter = null;

            var src = removeElement.attr('src');
            if (src) {
                ka.state.detachedBrowserPosterByKey[src.match(/\movie\/poster\/(.*?)-\d{2,3}\.image/)[1]] = removeElement.detach().css({
                    width: 150
                  , marginLeft: 10
                });
            } else {
                removeElement.remove();
            }

            ka.state.currentPageMode = 'detail';
    }});
};


ka.lib._triggerBrowserUpdate = function (movieObj) {
    ka.lib.updateDetailBrowserInfo(movieObj, true);

    /* $('#boom-movie-detail-browser-buttons li.boom-active').velocity({backgroundColor: '#' + (movieObj.primaryPosterColor || '000000')}, ka.settings.durationNormal); */
};


ka.lib._focusInImage = function (targetElement) {
    targetElement.velocity({translateZ: 0}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            elements[0].style.webkitFilter = 'saturate(' + Math.round(percentComplete * 100) + '%) opacity(' + Math.round(50 + 50 * percentComplete) / 100 + ')';
        }
      , complete: function (elements) {
            elements[0].style.webkitFilter = null;
        }
    });
};


ka.lib._focusOutImage = function (targetElement) {
    targetElement.velocity({translateZ: 0}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            elements[0].style.webkitFilter = 'saturate(' + (100 - Math.round(percentComplete * 100)) + '%) opacity(' + Math.round(100 - 50 * percentComplete) / 100 + ')';
        }
    });
};
