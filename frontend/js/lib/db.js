/**
 *  fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
 *  Copyright (C) 2013-2015 Nikola Klaric.
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
 *  @copyright Copyright (C) 2013-2015 Nikola Klaric
 */

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.sortExpandedKeys = function (a, b) {
    a = a.replace('m', '000000');
    b = b.replace('m', '000000');
    a = a.replace('k', '000');
    b = b.replace('k', '000');
    if (a.indexOf('.') != -1) {
        a = parseInt(a.replace('.', ''));
        a = a / 10;
    } else {
        a = parseInt(a);
    }
    if (b.indexOf('.') != -1) {
        b = parseInt(b.replace('.', ''));
        b = b / 10;
    } else {
        b = parseInt(b);
    }

    if (isNaN(a)) {
        a = 0;
    }

    if (isNaN(b)) {
        b = 0;
    }

    if (a > b) {
        return 1;
    } else if (a < b) {
        return -1;
    } else {
        return 0;
    }
};


ka.lib.addMovie = function (movieDict) {
    if (movieDict.id in ka.data.byId) {
        if (ka.state.isProcessingInitialItems) {
            ka.state.processingInitialItemsCount -= 1;
        }
        return;
    }

    var title, key, sortCriterionKey, sortedList;

    for (var orders = ['titleOriginal', 'titleLocalized', 'year', 'rating', 'budget'], order, o = 0; order = orders[o]; o++) {
        if (movieDict.isCompiled) {
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
        } else if (order == 'budget') {
            key = ka.lib._keyByBudget(movieDict.budget);
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

    ka.data.byId[movieDict.id] = movieDict;
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


ka.lib._keyByBudget = function (budget) {
    if (!budget) {
        return '?';
    } else if (budget >= 250000000) {
        return '250m';
    } else if (budget >= 200000000) {
        return '200m';
    } else if (budget >= 175000000) {
        return '175m';
    } else if (budget >= 150000000) {
        return '150m';
    } else if (budget >= 125000000) {
        return '125m';
    } else if (budget >= 100000000) {
        return '100m';
    } else if (budget >=  75000000) {
        return '75m';
    } else if (budget >=  50000000) {
        return '50m';
    } else if (budget >=  25000000) {
        return '25m';
    } else if (budget >=  10000000) {
        return '10m';
    } else if (budget >=   5000000) {
        return '5m';
    } else if (budget >=   2500000) {
        return '2.5m';
    } else if (budget >=   1000000) {
        return '1m';
    } else if (budget >=    500000) {
        return '500k';
    } else if (budget >=    250000) {
        return '250k';
    } else if (budget >=    100000) {
        return '100k';
    } else if (budget >=     50000) {
        return '50k';
    } else if (budget >=     10000) {
        return '10k';
    } else if (budget >=      1000) {
        return '1k';
    } else {
        return '< 1k';
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
