/**
 *  Receive movie details over WebSockets.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

// ka.data.cortex.all.forEach(function (item, index) { console.log(item.titleOriginal.getValue(), '->', item.criterion.getValue())})

ka.lib.addMovie = function (movieDict) {
    if (movieDict.uuid in ka.data.byUuid) {
        if (ka.state.isProcessingInitialItems) {
            ka.state.processingInitialItemsCount -= 1;
        }
        return;
    }

    var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''), compare = ka.state.collator.compare,
        localizedArticles = ka.lib.getLocalizedArticles();

    for (var orders = ['titleOriginal', 'titleLocalized', 'year', 'rating'], order, o = 0; order = orders[o]; o++) {
        var field = 'by' + order[0].toUpperCase() + order.slice(1);

        if (order == 'titleOriginal' || order == 'titleLocalized') {
            var title = movieDict[order],
                criterion = title.replace(new RegExp('^' + localizedArticles + ' ', 'i'), '').replace('.', '').toLocaleLowerCase(),
                key = new RegExp('^(?:' + localizedArticles + ' )?([\\S])', 'i').exec(title)[1].toLocaleUpperCase().replace(/[0-9]/, '123');

            /* Fix keys that are not Latin. */
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
        } else if (order == 'year') {
            var criterion = movieDict.titleLocalized.replace(/^the /i, '').replace('.', '').toLowerCase(),
                key = movieDict.releaseYear;
        } else if (order == 'rating') {
            var criterion = movieDict.titleLocalized.replace(/^the /i, '').replace('.', '').toLowerCase(),
                rating = movieDict.rating / 10, key;
            if (!rating) {
                key = '?';
            } else if (rating < 2) {
                key = '< 2';
            } else if (rating < 3) {
                key = '> 2';
            } else if (rating < 4) {
                key = '> 3';
            } else if (rating < 5) {
                key = '> 4';
            } else if (rating < 6) {
                key = '> 5';
            } else if (rating < 6.5) {
                key = '> 6';
            } else if (rating > 9) {
                key = '> 9';
            } else if (rating > 8.5) {
                key = '> 8.5';
            } else if (rating > 8) {
                key = '> 8';
            } else if (rating > 7.5) {
                key = '> 7.5';
            } else if (rating > 7) {
                key = '> 7';
            } else if (rating >= 6.5) {
                key = '> 6.5';
            }
        }

        if (key in ka.data[field]) {
            var sortedList = ka.data[field][key];
        } else {
            var sortedList = new Cortex([]);
        }

        ka.lib._insertSorted(sortedList, movieDict, criterion, field);
        ka.data[field][key] = sortedList;
    }

    ka.data.byUuid[movieDict.uuid] = movieDict;
    ka.data.all.push(movieDict);
};


ka.lib._insertSorted  = function (sortedListRef, item, primaryCriterion, field) {
    item[field] = primaryCriterion;

    var compare = ka.state.collator.compare;

    if (sortedListRef.count() == 0) {
        sortedListRef.push(item);
    } else if (sortedListRef.count() == 1) {
        if (compare(sortedListRef[0][field].getValue(), primaryCriterion) < 0) {
            sortedListRef.push(item);
        } else {
            sortedListRef.unshift(item);
        }
    } else {
        var index = sortedListRef.findIndex(function (wrapperElement, index) {
            if (index == 0 || index == sortedListRef.count() - 1) {
                return compare(primaryCriterion, sortedListRef[index][field].getValue()) < 0;
            } else {
                return compare(primaryCriterion, sortedListRef[index][field].getValue()) < 0 && compare(primaryCriterion, sortedListRef[index -1][field].getValue()) > 0;
            }
        });
        if (index == -1) {
            sortedListRef.push(item);
        } else {
            sortedListRef.insertAt(index, item);
        }
    }    
};
