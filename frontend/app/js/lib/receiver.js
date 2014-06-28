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

    var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''), compare = ka.state.collator.compare,
        localizedArticles = ka.lib.getLocalizedArticles();

    for (var orders = ['titleOriginal', 'titleLocalized', 'year'], order, o = 0; order = orders[o]; o++) {
        var field = 'by' + order[0].toUpperCase() + order.slice(1);

        if (order == 'titleOriginal' || order == 'titleLocalized') {
            var criterion = movieDict[order].replace(new RegExp('^' + localizedArticles + ' ', 'i'), '').replace('.', '').toLocaleLowerCase(),
                key = new RegExp('^(?:' + localizedArticles + ' )?([\\S])', 'i').exec(movieDict[order])[1].toLocaleUpperCase().replace(/[0-9]/, '123');

            /* Fix keys that are not Latin. */
            if (key !== '123' && /^[^A-Z]$/.test(key)) {
                for (var index = 0; index < 26; index++) {
                    if (compare(key, alphabet[index]) >= 0) { // TODO: fix comparison for e.g. die ueblichen verdaechtigen
                        key = alphabet[index];
                        break;
                    }
                }
            }
        } else if (order == 'year') {
            var criterion = movieDict.titleLocalized.replace(/^the /i, '').replace('.', '').toLowerCase(),
                key = movieDict.releaseYear;
        }

        if (key in ka.data.cortex[field]) {
            var sortedList = ka.data.cortex[field][key];
        } else {
            var sortedList = new Cortex([]);
        }

        ka.lib._insertSorted(sortedList, movieDict, criterion, field);
        ka.data.cortex[field][key] = sortedList;
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
