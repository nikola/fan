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
            .attr('src', '/movie/poster/' + movie.uuid + '-300.image')
            .on('load', function () {
                if ($(this).data('boom.isLoading')) {
                    $(this).data('boom.isLoading', false).css('visibility', 'visible');
                    $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + $(this).data('boom.loadUuid') + '.jpg)');
                }
            });
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


ka.lib.moveDetailBrowserFocusLeft = function () {

};


ka.lib.moveDetailBrowserFocusRight = function () {
    var dummyImage = $('#boom-movie-detail-poster-browser img').eq(0),
        previouslyFocusedImage = $('#boom-movie-detail-poster-browser img').eq(3).get(0),
        upcomingFocusedImage = $('#boom-movie-detail-poster-browser img').eq(4).get(0);

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
