/**
 *  Utility functions for localization.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.localizeButtons = function () {
    $('.boom-localizable-adjective').text(ka.lib.getLocalizationAdjective());
};


ka.lib.getLocalizedTitleByUuid = function (uuid) {
    var movie = ka.data.cortex.byUuid[uuid],
        title = (ka.state.gridSortDisplayLanguage == 'localized') ? movie.titleLocalized : movie.titleOriginal;
    return title;
};


ka.lib.getLocalizedArticles = function () {
    return {
        'en': 'the'
      , 'de': '(?:der|die|das)'
    }[ka.config.language];
};


ka.lib.getLocalizationAdjective = function () {
    return {
        'en': 'English'
      , 'de': 'German'
      , 'fr': 'French'
      , 'it': 'Italian'
    }[ka.config.language];
};
