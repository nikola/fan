/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};


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


ka.lib.setPrimaryPosterColor = function () {
    var colorThief = new ColorThief(),
        primaryColors = colorThief.getPalette($(this).get(0), 5),
        colorLuminance = [
            ka.lib.getLuminance(primaryColors[0])
          , ka.lib.getLuminance(primaryColors[1])
          , ka.lib.getLuminance(primaryColors[2])
        ],
        primaryColorRGB = primaryColors[colorLuminance.indexOf(Math.min.apply(Math, colorLuminance))];

    $(this).closest('.boom-movie-grid-info-overlay').find('.boom-movie-grid-info-overlay-title').css('backgroundColor', '#' + ((1 << 24) + (primaryColorRGB[0] << 16) + (primaryColorRGB[1] << 8) + primaryColorRGB[2]).toString(16).slice(1));
};


ka.lib.scrollToPage = function (page) {
    $('#content').css('-webkit-transform', 'translate3d(0, -' + page + '00%, 0)');
};
