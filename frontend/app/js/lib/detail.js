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
    $('#boom-movie-detail-title').text(movie.titleOriginal);
    $('#boom-movie-detail-description').text(movie.overview);
    $('#boom-movie-detail-poster img').attr('src', '');
    $('#boom-movie-detail').css('backgroundImage', 'none');
    setTimeout(function () {
        $('#boom-movie-detail-poster img')
            .attr('src', '/movie/poster/' + movie.uuid + '.jpg/200')
            .on('load', function () {
                $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + movie.uuid + '.jpg)');
            });
    }, 0);
};
