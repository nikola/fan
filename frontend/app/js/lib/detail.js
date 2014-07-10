/**
 *  Render movie detail page items.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.updateDetailPage = function () {
    var movie = ka.lib.getMovieFromGridFocus();
    $('#boom-detail-release span').text(movie.releaseYear);
    $('#boom-detail-runtime span').text(movie.runtime);
    $('#boom-movie-detail-title').text(ka.lib.getLocalizedTitleByUuid(movie.uuid));
    $('#boom-movie-detail-description').text(movie.storyline);

    $('#boom-movie-detail-top img').css('visibility', 'hidden');
    $('#boom-movie-detail').css('backgroundImage', 'none');

    $('#boom-movie-detail-top img')
        .attr('src', '/movie/poster/' + movie.uuid + '-300.image')
        .load(function () {
            $(this).css('visibility', 'visible');
            $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + movie.uuid + '.jpg)');
        });
};


ka.lib.updateDetailButtonSelection = function () {
    $('#boom-detail-button-group .boom-active').removeClass('boom-active');
    $('#boom-detail-button-group .boom-button').eq(ka.state.currentDetailButton).addClass('boom-active');
    if (ka.state.currentDetailButton > 0) {
        $('#boom-movie-detail-shade').velocity({opacity: 0.75}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandIn', {duration: 360, display: 'flex'});
    } else {
        $('#boom-movie-detail-shade').velocity({opacity: 0}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandOut', 360);
    }
};
