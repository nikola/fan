/**
 *  Color-related utility functions.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.getLuminance = function (color) {
    var red = color[0], green = color[1], blue = color[2],
        channelRed = red / 255,
        luminanceRed = (channelRed <= 0.03928) ? channelRed / 12.92 : Math.pow(((channelRed + 0.055) / 1.055), 2.4),
        channelGreen = green / 255,
        luminanceGreen = (channelGreen <= 0.03928) ? channelGreen / 12.92 : Math.pow(((channelGreen + 0.055) / 1.055), 2.4),
        channelBlue = blue / 255,
        luminanceBlue = (channelBlue <= 0.03928) ? channelBlue / 12.92 : Math.pow(((channelBlue + 0.055) / 1.055), 2.4);
    return 0.2126 * luminanceRed + 0.7152 * luminanceGreen + 0.0722 * luminanceBlue;
};

ka.lib.desaturateVisiblePosters = function () {
    ka.state.desaturationImageCache = [];

    var start = ka.state.gridPage * ka.config.gridMaxRows, end = (ka.state.gridPage + 1) * ka.config.gridMaxRows;
    for (var row = start; row < end; row++) {
        for (var item, i = 0; item = ka.state.gridLookupMatrix[row][i]; i++) {
            var element = $('#boom-poster-' + item.uuid);
            ka.state.desaturationImageCache.push(element);
            element.removeClass('undesaturate').addClass('desaturate');
            // TODO: use same logic to display: none posters when scrolling to details page
        }
    }
};

ka.lib.undesaturateVisiblePosters = function () {
    for (var element, e = 0; element = ka.state.desaturationImageCache[e]; e++) {
        element.removeClass('desaturate').addClass('undesaturate');
    }
};
