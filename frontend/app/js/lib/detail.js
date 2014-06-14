/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};


ka.lib.updateDetailPage = function () {
    var movie = ka.state.gridLookupMatrix[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY][ka.state.gridFocusX];
    $('#boom-movie-detail-title').text(movie.titleOriginal); //  + ' (' + movie.releaseYear + ')');
    $('#boom-movie-detail-description').text(movie.overview);
    $('#boom-movie-detail-poster img').attr('src', '');
    $('#boom-movie-detail').css('backgroundImage', 'none');
    setTimeout(function () {
        $('#boom-movie-detail-poster img')
            .attr('src', '/movie/poster/' + movie.uuid + '-300')
            .on('load', function () {
                $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + movie.uuid + '.jpg)');
            });
    }, 0);
};


ka.lib.updateDetailButtonSelection = function () {
    $('#boom-detail-button-group .boom-active').removeClass('boom-active');
    $('#boom-detail-button-group .boom-detail-button').eq(ka.state.currentDetailButton).addClass('boom-active');
    if (ka.state.currentDetailButton > 0) {
        $('#boom-movie-detail-shade').velocity({opacity: 0.75}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandIn', {duration: 360, display: 'flex'});
    } else {
        $('#boom-movie-detail-shade').velocity({opacity: 0}, {duration: 360});
        $('#boom-movie-detail-description').velocity('transition.expandOut', 360);
    }
};
