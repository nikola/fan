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


ka.lib.updateMenuButtonSelection = function () {
    $('#boom-menu .boom-active').removeClass('boom-active').css('backgroundColor', 'transparent');
    var selected = $('#boom-menu .boom-button').eq(ka.state.currentConfigButton);
    selected.addClass('boom-active').css('backgroundColor', selected.data('selectColor'));
};


ka.lib.executeMenuSelection = function () {
    var id = $('#boom-menu .boom-button').eq(ka.state.currentConfigButton).attr('id');

    if (id == 'boom-config-button-exit') {
        ka.state.hotkeyListener.reset();

        $('#boom-menu, #boom-movie-grid-container').velocity('fadeOut', {duration: ka.settings.durationNormal, complete: function () {
            console.exitApplication();
        }});
    } else if (id == 'boom-config-button-change-import') {
        ka.state.hotkeyListener.reset();

        $('#boom-menu, #boom-movie-grid-container').velocity('fadeOut', {duration: ka.settings.durationNormal, complete: function () {
            window.top.location.href = '/configure.html#return';
        }});
    } else if (id == 'boom-config-button-show-credits') {
        if (ka.state.view != 'credits') {
            ka.lib.showLicenseTexts();
        }
    } else {
        var lastCriterion = ka.state.gridSortCriterion, lastOrder = ka.state.gridSortOrder;

        if (id == 'boom-config-button-sort-title-original-asc') {
            ka.state.gridSortCriterion = 'byTitleOriginal';
            ka.state.gridSortDisplayLanguage = 'original';
            ka.state.gridSortOrder = 'asc';
        } else if (id == 'boom-config-button-sort-title-localized-asc') {
            ka.state.gridSortCriterion = 'byTitleLocalized';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'asc';
        } else if (id == 'boom-config-button-sort-year-desc') {
            ka.state.gridSortCriterion = 'byYear';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'desc';
        } else if (id == 'boom-config-button-sort-year-asc') {
            ka.state.gridSortCriterion = 'byYear';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'asc';
        } else if (id == 'boom-config-button-sort-rating-desc') {
            ka.state.gridSortCriterion = 'byRating';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'desc';
        } else if (id == 'boom-config-button-sort-budget-desc') {
            ka.state.gridSortCriterion = 'byBudget';
            ka.state.gridSortDisplayLanguage = 'localized';
            ka.state.gridSortOrder = 'desc';
        }

        if (ka.state.gridSortCriterion != lastCriterion || ka.state.gridSortOrder != lastOrder) {
            ka.lib.updateDesaturatedGrid();
        }
    }
};


ka.lib.updateDesaturatedGrid = function () {
    var id = ka.lib.getFirstMovieObjectFromCoord(ka.state.gridFocusX, ka.lib.getGridFocusAbsoluteY()).id;

    ka.lib.recalcMovieGrid();
    ka.lib.recalcPositionById(id);

    ka.state.desaturationImageCache = {};
    ka.lib.updateMovieGridOnChange();

    ka.lib.repositionMovieGrid();
    ka.lib.repositionMovieFocus();

    $('#boom-grid-focus').velocity({translateZ: 0, left: '+=780'}, 0);
};
