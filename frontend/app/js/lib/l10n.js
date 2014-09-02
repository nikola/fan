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


ka.lib.getLocalizedTitle = function (movieObj, insertHardBreak, noCollection) {
    var title;

    if (!noCollection && movieObj.isCompiled && ka.lib.isCompilationAtFocus() && ka.state.actualScreenMode != 'grid-compilation') {
        title = movieObj.compilation + ' Collection';
    } else if (ka.state.gridSortDisplayLanguage == 'localized') {
        title = movieObj.titleLocalized;
    } else {
        title = movieObj.titleOriginal;
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
