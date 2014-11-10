/**
 *  fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
 *  Copyright (C) 2013-2014 Nikola Klaric.
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.

 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *
 *  @author Nikola Klaric (nikola@klaric.org)
 *  @copyright Copyright (C) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.localizeButtons = function () {
    $('.boom-localizable-adjective').text(ka.lib.getLocalizationAdjective());
};


ka.lib.getLocalizedTitle = function (movieObj, insertHardBreak, noCollection) {
    var title;

    if (!noCollection && movieObj.isCompiled && ka.lib.isCompilationAtFocus() && ka.state.actualScreenMode != 'grid-compilation') {
        title = movieObj.compilation;
        if (ka.config.language == 'en') {
            title += ' Collection';
        } else if (ka.config.language == 'de') {
            title = 'Filmreihe: ' + title;
        }
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
