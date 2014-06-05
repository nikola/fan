/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};


ka.lib.updateDetailPage = function () {
    var uuid = ka.state.gridLookupMatrix[ka.config.gridMaxRows * ka.state.gridPage + ka.state.gridFocusY][ka.state.gridFocusX].uuid;
    $('#boom-movie-detail').css('backgroundImage', 'url(/movie/backdrop/' + uuid + '.jpg)')
};
