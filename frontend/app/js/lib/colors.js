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


ka.lib.getPixelsFromImage = function (element) {
    var image = element.get(0),
        context = ka.state.canvasContext;

    context.canvas.width = image.width;
    context.canvas.height = image.height;
    context.drawImage(image, 0, 0, image.width, image.height);

    var pixels = context.getImageData(0, 0, image.width, image.height).data,
        pixelCount = image.width * image.height, pixelArray = [],
        block = 0, index = 0, r, g, b;
    while (block < pixelCount) {
        r = pixels[index++];
        g = pixels[index++];
        b = pixels[index];
        index += 38;
        block += 10;
        if (!(r > 250 && g > 250 && b > 250)) {
            pixelArray.push([r, g, b]);
        }
    }
    return pixelArray;
};
