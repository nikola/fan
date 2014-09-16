/**
 *  Render movie detail page items.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.updateDetailPage = function (movie, skipBackdropUpdate) {
    if (!movie) {
        return;
    }

    $('#boom-movie-detail').data('boom.uuid', movie.uuid);

    if (!movie.streamless) {
        ka.state.currentDetailButton = 'play';
    } else if (movie.trailer) {
        ka.state.currentDetailButton = 'trailer';
    } else {
        ka.state.currentDetailButton = 'details';
    }

    $('#boom-movie-detail .boom-button').data('boom.select-color', movie.primaryPosterColor);

    $('#boom-detail-release span').text(movie.releaseYear);
    $('#boom-detail-runtime span').text(movie.runtime);
    $('#boom-detail-rating span').text((movie.rating) ? (movie.rating / 10) : '?');
    $('#boom-movie-detail-title').text(ka.lib.getLocalizedTitle(movie, false));
    $('#boom-movie-detail-description').text(movie.storyline);

    $('#boom-movie-detail-play-button').css('display', (movie.streamless) ? 'none' : 'inline-block');
    $('#boom-movie-detail-trailer-button').css('display', (movie.trailer) ? 'inline-block' : 'none');

    var poster = $('#boom-movie-detail-top img')
    if (poster.data('boom.loadUuid') != movie.uuid) {
        if (!skipBackdropUpdate) {
            $('#boom-movie-detail').css('backgroundImage', 'none');
        }

        poster.css('visibility', 'hidden').data({'boom.isLoading': true, 'boom.loadUuid': movie.uuid})
            .on('load', function () {
                if (poster.data('boom.isLoading')) {
                    poster.data('boom.isLoading', false).css('visibility', 'visible').off();
                    if (!skipBackdropUpdate) {
                        $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + poster.data('boom.loadUuid') + '.jpg)');
                    }
                }
            })
            .attr('src', '/movie/poster/' + movie.uuid + '-300.image');
    }


};


ka.lib.updateDetailButtonSelection = function (skipAnimation) {
    $('#boom-detail-button-group .boom-active').removeClass('boom-active')
        .css('backgroundColor', 'transparent');

    var button = $('#boom-movie-detail-' + ka.state.currentDetailButton + '-button');
    button.addClass('boom-active')
        .css('backgroundColor', '#' + button.data('boom.select-color'));

    if (!skipAnimation) {
        if (ka.state.currentDetailButton == 'details') {
            $('#boom-movie-detail-shade').velocity({opacity: 0.75}, {duration: ka.settings.durationNormal});
            $('#boom-movie-detail-description').velocity('transition.expandIn', {duration: ka.settings.durationNormal, display: 'flex'});
        } else {
            $('#boom-movie-detail-shade').velocity({opacity: 0}, ka.settings.durationNormal);
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


ka.lib.addBrowserGridImage = function (index, unselected, width) {
    var snapshot = ka.lib.grid.getMovieListSnapshot(),
        element = $('<img>', {
        src: '/movie/poster/' + snapshot[index].uuid + '-150.image'
      , width: width
      , height: 225
      , data: {
            'boom.index': index
        }
      , css: {
            webkitTransform: 'translate3d(0, 0, 0)'
        }
    }).appendTo('#boom-movie-detail-poster-browser');

    if (unselected) {
        var style = element.get(0).style;
        style.opacity = 0.5;
        style.webkitFilter = 'grayscale(100%)';
    }

    return element;
};


ka.lib.populateDetailBrowserGrid = function () {
    $('#boom-movie-detail-poster-browser').empty();
    $('<img>', {
          width: 150
        , height: 225
        , css: {
            webkitFilter: 'grayscale(100%)'
          , webkitTransform: 'translate3d(0, 0, 0)'
          , opacity: 0.5
        }
    }).appendTo('#boom-movie-detail-poster-browser');

    var current = ka.data.indexByUuid[$('#boom-movie-detail').data('boom.uuid')],
        index, end, focused,
        snapshot = ka.lib.grid.getMovieListSnapshot();

    if (snapshot.length < 6) {
        index = 0;
        end = snapshot.length;
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
        if (end > snapshot.length) {
            if (focused == 2 && snapshot.length > 5) {
                focused = 2 + end - snapshot.length;
                index -= end - snapshot.length;
            }
            end = snapshot.length;
        }
    }

    do {
        ka.lib.addBrowserGridImage(index, index != current, 150);
    } while (++index < end);

    /* Pre-cache previous/next posters. */
    var lookBehindIndex = index - 3, lookAheadIndex = index + 3;
    if (lookBehindIndex > -1) {
        new Image().src = '/movie/poster/' + snapshot[lookBehindIndex].uuid + '-150.image';
    }
    if (lookAheadIndex < snapshot.length) {
        new Image().src = '/movie/poster/' + snapshot[lookAheadIndex].uuid + '-150.image';
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
    var title = (ka.state.gridSortDisplayLanguage == 'localized') ? movieObj.titleLocalized : movieObj.titleOriginal;
    $('#boom-movie-detail-browser-title').html(title + '&nbsp;(' + movieObj.releaseYear + ')');

    if (movieObj.isCompiled) {
        $('#boom-movie-detail-browser-collection').text(movieObj.compilation + ' Collection');
    } else {
        $('#boom-movie-detail-browser-collection').text('');
    }

    var additionalInfo = $('#boom-movie-detail-browser-additional span');
    additionalInfo.eq(0).text(movieObj.runtime);
    additionalInfo.eq(1).text((movieObj.rating) ? (movieObj.rating / 10) : '?');
};


ka.lib.moveDetailBrowserLeft = function () {
    var firstPosterIndex = $('#boom-movie-detail-poster-browser :nth-child(2)').data('boom.index'),
        snapshot = ka.lib.grid.getMovieListSnapshot();

    if (ka.state.currentDetailBrowserPosterColumn > 2 || (firstPosterIndex == 0 && ka.state.currentDetailBrowserPosterColumn > 0)) {
        ka.lib._moveDetailBrowserFocus('prev', '-=160');
        ka.state.currentDetailBrowserPosterColumn -= 1;
    } else if (firstPosterIndex > 0) {
        ka.state.currentPageMode = 'limbo';

        var images = $('#boom-movie-detail-poster-browser img'),
            previouslyFocusedImage = images.eq(3).get(0),
            upcomingFocusedImage = images.eq(2).get(0),
            firstImageIndex = images.eq(1).data('boom.index');

        images.eq(0)
            .attr('src', '/movie/poster/' + snapshot[firstImageIndex - 1].uuid + '-150.image')
            .data('boom.index', firstImageIndex - 1);

        $('<img>', {
            width: 0
          , height: 225
          , css: {
                webkitFilter: 'grayscale(100%)'
              , webkitTransform: 'translate3d(0, 0, 0)'
              , opacity: 0.5
              , marginLeft: 0
            }
        }).prependTo('#boom-movie-detail-poster-browser').velocity({width: 150, marginLeft: 10}, ka.settings.durationNormal);

        ka.lib._animatePosterVisibility(
            snapshot[firstImageIndex + 1]
          , $('#boom-movie-detail-poster-browser img').eq(6)
          , previouslyFocusedImage
          , upcomingFocusedImage
        );
    }
};


ka.lib.moveDetailBrowserRight = function () {
    var column = ka.state.currentDetailBrowserPosterColumn,
        posters = $('#boom-movie-detail-poster-browser img'),
        currentPosterIndex = posters.eq(column + 1).data('boom.index'),
        lastPosterIndex = posters.last().data('boom.index'),
        snapshot = ka.lib.grid.getMovieListSnapshot();

    if ((column < 2 && snapshot.length > 2) || (lastPosterIndex == snapshot.length - 1 && lastPosterIndex - currentPosterIndex > 0)) {
        ka.lib._moveDetailBrowserFocus('next', '+=160');
        ka.state.currentDetailBrowserPosterColumn += 1;
    } else if (posters.length == 6 && lastPosterIndex + 1 < snapshot.length) {
        ka.state.currentPageMode = 'limbo';

        var images = $('#boom-movie-detail-poster-browser img'),
            dummyImage = images.eq(0),
            previouslyFocusedImage = images.eq(3).get(0),
            upcomingFocusedImage = images.eq(4).get(0),
            lastImageIndex = images.eq(5).data('boom.index');

        ka.lib.addBrowserGridImage(lastImageIndex + 1, true, 0).velocity({width: 150}, ka.settings.durationNormal);

        ka.lib._animatePosterVisibility(
            snapshot[lastImageIndex - 1]
          , dummyImage
          , previouslyFocusedImage
          , upcomingFocusedImage
        );
    }
};


ka.lib._moveDetailBrowserFocus = function (accessor, offset) {
    ka.state.currentPageMode = 'limbo';

    var currentElement = $('#boom-movie-detail-poster-browser :nth-child(' + (ka.state.currentDetailBrowserPosterColumn + 2) + ')'),
        targetElement = currentElement[accessor](),
        snapshot = ka.lib.grid.getMovieListSnapshot();

    ka.lib._triggerBrowserUpdate(snapshot[targetElement.data('boom.index')]);
    ka.lib._focusInPoster(targetElement);
    ka.lib._focusOutPoster(currentElement);

    $('#boom-movie-detail-browser-focus').velocity({left: offset}, {duration: ka.settings.durationNormal, complete: function () {
        ka.state.currentPageMode = 'detail-browser';
    }});
};


ka.lib._animatePosterVisibility = function (movieObj, targetElement, previouslyFocusedPoster, upcomingFocusedPoster) {
    ka.lib._triggerBrowserUpdate(movieObj);

    targetElement.velocity({width: 0, marginLeft: 0}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            if (percentComplete < 1) {
                previouslyFocusedPoster.style.webkitFilter = 'grayscale(' + Math.round(percentComplete * 100) + '%)';
                previouslyFocusedPoster.style.opacity = Math.round(100 - 50 * percentComplete) / 100;
                upcomingFocusedPoster.style.webkitFilter = 'grayscale(' + (100 - Math.round(percentComplete * 100)) + '%)';
                upcomingFocusedPoster.style.opacity = Math.round(50 + 50 * percentComplete) / 100;
            }
        }
      , complete: function () {
            previouslyFocusedPoster.style.webkitFilter = 'grayscale(100%)';
            previouslyFocusedPoster.style.opacity = 0.5;
            upcomingFocusedPoster.style.webkitFilter = null;
            upcomingFocusedPoster.style.opacity = 1;

            targetElement.remove();

            ka.state.currentPageMode = 'detail-browser';
    }});
};


ka.lib._triggerBrowserUpdate = function (movieObj) {
    ka.lib.updateDetailBrowserInfo(movieObj, true);

    clearTimeout(ka.state.backdropDownloadTimer);
    ka.state.backdropDownloadTimer = null;

    $('#boom-movie-detail-poster-fade-in').attr('src', '/movie/backdrop/' + movieObj.uuid +  '.jpg');
};


ka.lib._focusInPoster = function (targetElement) {
    targetElement.velocity({opacity: 1}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            elements[0].style.webkitFilter = 'grayscale(' + (100 - Math.round(percentComplete * 100)) + '%)';
        }
      , complete: function (elements) {
            elements[0].style.webkitFilter = null;
        }
    });
};


ka.lib._focusOutPoster = function (targetElement) {
    targetElement.velocity({opacity: 0.5}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            elements[0].style.webkitFilter = 'grayscale(' + Math.round(percentComplete * 100) + '%)';
        }
    });
};


ka.lib.onBackdropLoaded = function () {
    $('#boom-movie-detail-poster-fade-in').velocity('fadeIn', {duration: ka.settings.durationNormal, complete: function () {
        $('#boom-movie-detail').css('backgroundImage', 'url(' + $(this).attr('src') + ')');
        ka.state.backdropDownloadTimer = setTimeout(function () {
            $('#boom-movie-detail-poster-fade-in').velocity('fadeOut', {duration: 0, complete: function () {
                ka.state.backdropDownloadTimer = null;
            }});
        }, ka.settings.durationShort);
    }});
};


ka.lib.transitionBackFromDetailScreen = function () {
    var currentDetailMovieUuid = $('#boom-movie-detail').data('boom.uuid'),
        hasOpenCompilation = ka.state.currentCompilationPosterCount > 0;
    if (currentDetailMovieUuid != ka.state.currentGridMovieUuid) {
        ka.state.currentGridMovieUuid = currentDetailMovieUuid;

        ka.lib.unoccludeMovieGrid();

        if (hasOpenCompilation) {
            ka.lib.dissolveCompilation();
        }

        ka.lib.recalcPositionByUuid(currentDetailMovieUuid);
        ka.lib.repositionMovieGrid();
        ka.lib.repositionMovieFocus(true); /* offscreen */

        ka.lib.occludeMovieGrid();

        ka.transition.detail.to.grid();
    } else if (hasOpenCompilation) {
        ka.transition.detail.to.compilation();
    } else {
        ka.transition.detail.to.grid();
    }
};
