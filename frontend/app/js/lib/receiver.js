/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};
if (!('lib' in ka)) ka.lib = {};


ka.lib.addMovieToCortex = function (movieDict) {
    if (ka.data.cortex.byUuid.hasKey(movieDict.uuid)) return;

    var uuid = movieDict.uuid,
        titleOriginal = movieDict.titleOriginal,
        titleSortable = titleOriginal.replace(/^the /i, '').replace('.', '').toLowerCase(),
        firstLetter = /^(?:the )?([\w])/i.exec(titleOriginal)[1].toUpperCase(),
        firstLetterCode = firstLetter.charCodeAt(0),
        releaseYear = movieDict.releaseYear;

    movieDict.titleSortable = titleSortable;

    if (/[0-9]/.test(firstLetter)) {
        firstLetter = '123';
    }

    if (firstLetter in ka.data.cortex.byLetter) {
        var byLetterList = ka.data.cortex.byLetter[firstLetter];
    } else {
        var byLetterList = new Cortex([]);
    }

    if (byLetterList.count() == 0) {
        byLetterList.push(movieDict);
    } else if (byLetterList.count() == 1) {
        if (byLetterList[0].titleSortable.getValue() < titleSortable) {
            byLetterList.push(movieDict);
        } else {
            byLetterList.unshift(movieDict);
        }
    } else {
        var index = byLetterList.findIndex(function (wrapperElement, index, wrapperArray) {
            if (index == 0 || index == byLetterList.count() - 1) {
                return titleSortable < byLetterList[index].titleSortable.getValue();
            } else {
                return titleSortable < byLetterList[index].titleSortable.getValue() && titleSortable > byLetterList[index -1].titleSortable.getValue();
            }
        });
        if (index == -1) {
            byLetterList.push(movieDict);
        } else {
            byLetterList.insertAt(index, movieDict);
        }

    }
    ka.data.cortex.byLetter[firstLetter] = byLetterList;
    ka.data.cortex.byUuid.add(uuid, movieDict);
    ka.data.cortex.all.push(movieDict);
};
