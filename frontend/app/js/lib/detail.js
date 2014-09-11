/**
 *  Render movie detail page items.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.updateDetailPage = function (movie, callback) {
    if (movie) {
        $('#boom-movie-detail .boom-button').data('boom.select-color', movie.primaryPosterColor);

        $('#boom-detail-release span').text(movie.releaseYear);
        $('#boom-detail-runtime span').text(movie.runtime);
        $('#boom-detail-rating span').text((movie.rating) ? (movie.rating / 10) : '?');
        $('#boom-movie-detail-title').text(ka.lib.getLocalizedTitle(movie, false));
        $('#boom-movie-detail-description').text(movie.storyline);

        $('#boom-movie-detail-play-button').css('display', (movie.streamless) ? 'none' : 'inline-block');
        $('#boom-movie-detail-trailer-button').css('display', (movie.trailer) ? 'inline-block' : 'none');

        $('#boom-movie-detail').css('backgroundImage', 'none');

        if (callback) {
            setTimeout(callback, 80);
        }

        $('#boom-movie-detail-top img')
            .css('visibility', 'hidden')
            .data({'boom.isLoading': true, 'boom.loadUuid': movie.uuid})
            .on('load', function () {
                if ($(this).data('boom.isLoading')) {
                    $(this).data('boom.isLoading', false).css('visibility', 'visible').off();
                    $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + $(this).data('boom.loadUuid') + '.jpg)');
                }
            })
            .attr('src', '/movie/poster/' + movie.uuid + '-300.image');
    }
};


ka.lib.updateDetailButtonSelection = function () {
    $('#boom-detail-button-group .boom-active').removeClass('boom-active')
        .css('backgroundColor', 'transparent');

    var button = $('#boom-movie-detail-' + ka.state.currentDetailButton + '-button');
    button.addClass('boom-active')
        .css('backgroundColor', '#' + button.data('boom.select-color'));

    if (ka.state.currentDetailButton == 'details') {
        $('#boom-movie-detail-shade').velocity({opacity: 0.75}, {duration: ka.settings.durationNormal});
        $('#boom-movie-detail-description').velocity('transition.expandIn', {duration: ka.settings.durationNormal, display: 'flex'});
    } else {
        $('#boom-movie-detail-shade').velocity({opacity: 0}, ka.settings.durationNormal);
        $('#boom-movie-detail-description').velocity('transition.expandOut', ka.settings.durationNormal);
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
    var element = $('<img>', {
        src: '/movie/poster/' + ka.data.asList[index].uuid + '-150.image'
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

    var index = ka.data.indexByUuid[ka.state.currentGridMovieUuid],
        start = index - 2;
    for (var counter = 0; counter < 5; counter++) {
        ka.lib.addBrowserGridImage(start + counter, counter != 2, 150);
    }

    /* Pre-cache previous/next posters. */
    var lookBehindIndex = index - 3, lookAheadIndex = index + 3;
    if (lookBehindIndex > -1) {
        new Image().src = '/movie/poster/' + ka.data.asList[lookBehindIndex].uuid + '-150.image';
    }
    if (lookAheadIndex < ka.data.asList.length) {
        new Image().src = '/movie/poster/' + ka.data.asList[lookAheadIndex].uuid + '-150.image';
    }
};


ka.lib.updateDetailBrowserInfo = function (movieObj, fade) {
    if (fade) {
        /* $('#boom-movie-detail-browser-info').velocity({backgroundColor: '#' + movieObj.primaryPosterColor}, ka.settings.durationNormal); */

        setTimeout(function () { ka.lib._updateDetailBrowserInfo(movieObj); }, ka.settings.durationShort);
        /* $('#boom-movie-detail-browser-info').velocity('fadeOut', {duration: ka.settings.durationShort, complete: function () {
            ka.lib._updateDetailBrowserInfo(movieObj);

            $(this).velocity('fadeIn', ka.settings.durationShort);
        }}); */
    } else {
        ka.lib._updateDetailBrowserInfo(movieObj);
    }
};


ka.lib._updateDetailBrowserInfo = function (movieObj) {
    var title = (ka.state.gridSortDisplayLanguage == 'localized') ? movieObj.titleLocalized : movieObj.titleOriginal;
    $('#boom-movie-detail-browser-title').text(title);

    if (movieObj.isCompiled) {
        $('#boom-movie-detail-browser-collection').text(movieObj.compilation + ' Collection');
    } else {
        $('#boom-movie-detail-browser-collection').text('');
    }

    var additionalInfo = $('#boom-movie-detail-browser-additional span');
    additionalInfo.eq(0).text(movieObj.releaseYear);
    additionalInfo.eq(1).text(movieObj.runtime);
    additionalInfo.eq(2).text((movieObj.rating) ? (movieObj.rating / 10) : '?');
};


ka.lib.moveDetailBrowserFocusLeft = function () {
    var images = $('#boom-movie-detail-poster-browser img'),
        previouslyFocusedImage = images.eq(3).get(0),
        upcomingFocusedImage = images.eq(2).get(0),
        firstImageIndex = images.eq(1).data('boom.index');

    images.eq(0)
        .attr('src', '/movie/poster/' + ka.data.asList[firstImageIndex - 1].uuid + '-150.image')
        .data('boom.index', firstImageIndex - 1);

    var dummyImage = $('<img>', {
        width: 0
      , height: 225
      , css: {
            webkitFilter: 'grayscale(100%)'
          , webkitTransform: 'translate3d(0, 0, 0)'
          , opacity: 0.5
          , marginLeft: 0
        }
    }).prependTo('#boom-movie-detail-poster-browser');
    dummyImage.velocity({width: 150, marginLeft: 10}, ka.settings.durationNormal);

    ka.lib.updateDetailBrowserInfo(ka.data.asList[firstImageIndex + 1], true);

    $('#boom-movie-detail-poster-fade-in').attr('src', '/movie/backdrop/' + ka.data.asList[firstImageIndex + 1].uuid +  '.jpg');

    $('#boom-movie-detail-poster-browser img').eq(6).velocity({width: 0, marginLeft: 0}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            if (percentComplete < 1) {
                previouslyFocusedImage.style.webkitFilter = 'grayscale(' + Math.round(percentComplete * 100) + '%)';
                previouslyFocusedImage.style.opacity = Math.round(100 - 50 * percentComplete) / 100;
                upcomingFocusedImage.style.webkitFilter = 'grayscale(' + (100 - Math.round(percentComplete * 100)) + '%)';
                upcomingFocusedImage.style.opacity = Math.round(50 + 50 * percentComplete) / 100;
            }
        }
      , complete: function () {
            previouslyFocusedImage.style.webkitFilter = 'grayscale(100%)';
            previouslyFocusedImage.style.opacity = 0.5;
            upcomingFocusedImage.style.webkitFilter = null;
            upcomingFocusedImage.style.opacity = 1;

            $('#boom-movie-detail-poster-browser img').eq(6).remove();
    }});
};


ka.lib.moveDetailBrowserFocusRight = function () {
    var images = $('#boom-movie-detail-poster-browser img'),
        dummyImage = images.eq(0),
        previouslyFocusedImage = images.eq(3).get(0),
        upcomingFocusedImage = images.eq(4).get(0),
        lastImageIndex = images.eq(5).data('boom.index');

    var addedImage = ka.lib.addBrowserGridImage(lastImageIndex + 1, true, 0);
    addedImage.velocity({width: 150}, ka.settings.durationNormal);

    ka.lib.updateDetailBrowserInfo(ka.data.asList[lastImageIndex - 1], true);

    $('#boom-movie-detail-poster-fade-in').attr('src', '/movie/backdrop/' + ka.data.asList[lastImageIndex - 1].uuid +  '.jpg');

    dummyImage.velocity({width: 0, marginLeft: 0}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            if (percentComplete < 1) {
                previouslyFocusedImage.style.webkitFilter = 'grayscale(' + Math.round(percentComplete * 100) + '%)';
                previouslyFocusedImage.style.opacity = Math.round(100 - 50 * percentComplete) / 100;
                upcomingFocusedImage.style.webkitFilter = 'grayscale(' + (100 - Math.round(percentComplete * 100)) + '%)';
                upcomingFocusedImage.style.opacity = Math.round(50 + 50 * percentComplete) / 100;
            }
        }
      , complete: function () {
            previouslyFocusedImage.style.webkitFilter = 'grayscale(100%)';
            previouslyFocusedImage.style.opacity = 0.5;
            upcomingFocusedImage.style.webkitFilter = null;
            upcomingFocusedImage.style.opacity = 1;

            dummyImage.remove();
    }});
};


ka.lib.onBackdropLoaded = function () {
    $('#boom-movie-detail-poster-fade-in').velocity('fadeIn', {duration: ka.settings.durationNormal, complete: function () {
        $('#boom-movie-detail').css('backgroundImage', 'url(' + $(this).attr('src') + ')');
        setTimeout(function () {
            $('#boom-movie-detail-poster-fade-in').velocity('fadeOut', 0);
        }, 50);
    }});
};


/*
ka.lib.moveDetailBrowserFocus = function () {
    dummyImage.velocity({width: 0, marginLeft: 0}, {
        duration: ka.settings.durationNormal
      , progress: function (elements, percentComplete) {
            if (percentComplete < 1) {
                previouslyFocusedImage.style.webkitFilter = 'grayscale(' + Math.round(percentComplete * 100) + '%)';
                previouslyFocusedImage.style.opacity = Math.round(100 - 50 * percentComplete) / 100;
                upcomingFocusedImage.style.webkitFilter = 'grayscale(' + (100 - Math.round(percentComplete * 100)) + '%)';
                upcomingFocusedImage.style.opacity = Math.round(50 + 50 * percentComplete) / 100;
            }
        }
      , complete: function () {
            previouslyFocusedImage.style.webkitFilter = 'grayscale(100%)';
            previouslyFocusedImage.style.opacity = 0.5;
            upcomingFocusedImage.style.webkitFilter = null;
            upcomingFocusedImage.style.opacity = 1;

            dummyImage.remove();

            $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + ka.data.asList[lastImageIndex - 1].uuid +  '.jpg)');
    }});
};*/
