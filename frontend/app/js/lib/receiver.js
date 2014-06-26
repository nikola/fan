/**
 *  Receive movie details over WebSockets.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

// ka.data.cortex.all.forEach(function (item, index) { console.log(item.titleOriginal.getValue(), '->', item.criterion.getValue())})

ka.lib.addMovieToCortex = function (movieDict) {
    if (ka.data.cortex.byUuid.hasKey(movieDict.uuid)) return;

    var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''), compare = ka.state.collator.compare;

    for (var orders = ['byLetter', 'byYear'], order, o = 0; order = orders[o]; o++) {
        if (order == 'byLetter') {
            var criterion = movieDict.titleOriginal.replace(/^the /i, '').replace('.', '').toLowerCase(),
                key = /^(?:the )?([\S])/i.exec(movieDict.titleOriginal)[1].toUpperCase().replace(/[0-9]/, '123');

            /* Fix keys that are not Latin. */
            if (key !== '123' && /^[^A-Z]$/.test(key)) {
                for (var index = 0; index < 26; index++) {
                    if (compare(key, alphabet[index]) > -1) {
                        key = alphabet[index];
                        break;
                    }
                }
            }
        } else if (order == 'byYear') {
            var criterion = movieDict.titleOriginal.replace(/^the /i, '').replace('.', '').toLowerCase(),
                key = movieDict.releaseYear;
        }

        if (key in ka.data.cortex[order]) {
            var sortedList = ka.data.cortex[order][key];
        } else {
            var sortedList = new Cortex([]);
        }

        ka.lib._insertSorted(sortedList, movieDict, criterion, order);
        ka.data.cortex[order][key] = sortedList;
    }

    ka.data.cortex.byUuid.add(movieDict.uuid, movieDict);
    ka.data.cortex.all.push(movieDict);
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
