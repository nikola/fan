/**
 *  Store movie details received over WebSockets.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.addMovie = function (movieDict) {
    if (movieDict.uuid in ka.data.byUuid) {
        if (ka.state.isProcessingInitialItems) {
            ka.state.processingInitialItemsCount -= 1;
        }
        return;
    }

    var title, key, sortCriterionKey, sortedList;

    for (var orders = ['titleOriginal', 'titleLocalized', 'year', 'rating'], order, o = 0; order = orders[o]; o++) {
        if (movieDict.compilation && movieDict.isCompiled) {
            title = movieDict.compilation;
        } else if (order == 'titleOriginal') {
            title = movieDict.titleOriginal;
        } else {
            title = movieDict.titleLocalized;
        }

        title = ka.lib._getComparableTitle(title);

        if (order == 'titleOriginal' || order == 'titleLocalized') {
            key = ka.lib._getCollatedKey(new RegExp('^(?:' + ka.lib.getLocalizedArticles() + ' )?([\\S])', 'i').exec(title)[1].toLocaleUpperCase().replace(/[0-9]/, '123'));
        } else if (order == 'year') {
            key = movieDict.releaseYear;
        } else if (order == 'rating') {
            key = ka.lib._keyByRating(movieDict.rating / 10);
        }

        sortCriterionKey = 'by' + order[0].toUpperCase() + order.slice(1);
        if (key in ka.data[sortCriterionKey]) {
            sortedList = ka.data[sortCriterionKey][key];
        } else {
            sortedList = [];
        }
        ka.lib._insertSorted(sortedList, movieDict, title, sortCriterionKey);
        ka.data[sortCriterionKey][key] = sortedList;
    }

    ka.data.byUuid[movieDict.uuid] = movieDict;
};


ka.lib._insertSorted  = function (sortedListRef, movieDict, comparableTitle, sortCriterion) {
    movieDict[sortCriterion] = comparableTitle;

    var compare = ka.state.collator.compare;

    if (sortedListRef.length == 0) {
        sortedListRef.push(movieDict);
    } else if (sortedListRef.length == 1) {
        if (compare(sortedListRef[0][sortCriterion], comparableTitle) < 0) {
            sortedListRef.push(movieDict);
        } else {
            sortedListRef.unshift(movieDict);
        }
    } else {
        var position = -1;

        for (var index = 0; index < sortedListRef.length; index++) {
            if (compare(comparableTitle, sortedListRef[index][sortCriterion]) == 0) {
                position = index;
                break;
            } else if (index == 0 || index == sortedListRef.length - 1) {
                if (compare(comparableTitle, sortedListRef[index][sortCriterion]) < 0) {
                    position = index;
                    break;
                }
            } else {
                if (compare(comparableTitle, sortedListRef[index][sortCriterion]) < 0 && compare(comparableTitle, sortedListRef[index - 1][sortCriterion]) > 0) {
                    position = index;
                    break;
                }
            }
        }
        if (position == -1) {
            sortedListRef.push(movieDict);
        } else {
            sortedListRef.splice(position, 0, movieDict);
        }
    }
};


ka.lib._keyByRating = function (rating) {
    if (!rating) {
        return '?';
    } else if (rating < 2) {
        return '< 2';
    } else if (rating < 3) {
        return '> 2';
    } else if (rating < 4) {
        return '> 3';
    } else if (rating < 5) {
        return '> 4';
    } else if (rating < 6) {
        return '> 5';
    } else if (rating < 6.5) {
        return '> 6';
    } else if (rating > 9) {
        return '> 9';
    } else if (rating > 8.5) {
        return '> 8.5';
    } else if (rating > 8) {
        return '> 8';
    } else if (rating > 7.5) {
        return '> 7.5';
    } else if (rating > 7) {
        return '> 7';
    } else if (rating >= 6.5) {
        return '> 6.5';
    }
};


ka.lib._getCollatedKey = function (key) {
    var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''),
        compare = ka.state.collator.compare;

    if (key !== '123' && /^[^A-Z]$/.test(key)) {
        for (var index = 0; index < 26; index++) {
            if (compare(key, alphabet[index]) > 0) {
                key = alphabet[index];
                break;
            }
        }
    }

    if (key !== '123' && /^[^A-Z]$/.test(key)) {
        key = '?';
    }

    return key;
};


ka.lib._getComparableTitle = function (title) {
    return title.replace(new RegExp('^' + ka.lib.getLocalizedArticles() + ' ', 'i'), '').replace('.', '').toLocaleLowerCase();
};
