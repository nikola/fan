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


ka.lib.getLocalizedTitleByUuid = function (uuid, insertHardBreak) {
    var movie = ka.data.byUuid[uuid], title;

    if (movie.isCompiled) {
        title = movie.compilation + ' Collection';
    } else if (ka.state.gridSortDisplayLanguage == 'localized') {
        title = movie.titleLocalized;
    } else {
        title = movie.titleOriginal;
    }

    if (insertHardBreak && title.indexOf(':') > 9) {
        title = title.substr(0, title.indexOf(':') + 1) + '<br>' + title.substr(title.indexOf(':') + 1);
    }

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
