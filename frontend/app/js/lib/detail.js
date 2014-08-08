/**
 *  Render movie detail page items.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.updateDetailPage = function () {
    var movie = ka.lib.getMovieFromGridFocus();
    if (movie) {
        $('#boom-movie-detail .boom-button').data('boom.select-color', movie.primaryPosterColor);

        $('#boom-detail-release span').text(movie.releaseYear);
        $('#boom-detail-runtime span').text(movie.runtime);
        $('#boom-detail-rating span').text((movie.rating) ? (movie.rating / 10) : '?');
        $('#boom-movie-detail-title').text(ka.lib.getLocalizedTitleByUuid(movie.uuid));
        $('#boom-movie-detail-description').text(movie.storyline);

        $('#boom-movie-detail-play-button').css('display', (movie.streamless) ? 'none' : 'inline-block');
        $('#boom-movie-detail-trailer-button').css('display', (movie.trailer) ? 'inline-block' : 'none');

        $('#boom-movie-detail-top img').css('visibility', 'hidden');
        $('#boom-movie-detail').css('backgroundImage', 'none');

        $('#boom-movie-detail-top img')
            .attr('src', '/movie/poster/' + movie.uuid + '-300.image')
            .load(function () {
                $(this).css('visibility', 'visible');
                $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + movie.uuid + '.jpg)');
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
        $('#boom-movie-detail-shade').velocity({opacity: 0.75}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandIn', {duration: 360, display: 'flex'});
    } else {
        $('#boom-movie-detail-shade').velocity({opacity: 0}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandOut', 360);
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

    $('#boom-movie-detail').velocity('fadeIn', 360);

    window.focus();
}
