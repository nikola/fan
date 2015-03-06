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
 *  @copyright Copyright (C) 2013-2015 Nikola Klaric.
 */

; var ka = ka || {}; if (!('transition' in ka)) ka.transition = {};


ka.transition.menu = {to: {

    grid: function () {
        ka.state.view = 'limbo';

        ka.lib.grid.occlude();

        $('#boom-menu, #boom-movie-grid-container, #boom-grid-focus').velocity(
            {translateZ: 0, left: '-=780'}
          , {
                duration: ka.settings.durationNormal
              , progress: function (elements, percentComplete) {
                    elements[1].style.opacity = 0.5 + percentComplete / 2;
                    elements[2].style.opacity = percentComplete;

                    $.each(ka.state.desaturationImageCache, function (key, value) {
                        value.style.webkitFilter = 'saturate(' + Math.round(100 * percentComplete) + '%)';
                    });
                }
              , complete: function () {
                    ka.lib.grid.unocclude();

                    $.each(ka.state.desaturationImageCache, function (key, value) {
                        value.style.webkitFilter = 'none';
                        value.style.webkitTransform = 'none';
                    });
                    ka.state.desaturationImageCache = {};

                    $('#boom-menu').css('display', 'none');

                    ka.state.view = 'grid';
                }
            }
        );
    }
}};


ka.transition.grid = {to: {

    menu: function () {
        ka.state.view = 'limbo';

        $('#boom-menu').css('display', 'block');
        ka.lib.updatePendingObjects(true);

        ka.lib.grid.occlude();

        ka.state.desaturationImageCache = {};

        var start = ka.state.gridPage * ka.settings.gridMaxRows, end = (ka.state.gridPage + 1) * ka.settings.gridMaxRows,
            item;
        for (var row = start; row < end; row++) {
            if (row < ka.state.gridLookupMatrix.length) {
                for (var column = 0; column < 4; column++) {
                    item = ka.lib.getFirstMovieObjectFromCoord(column, row);
                    if (item !== null) {
                        ka.state.desaturationImageCache[item.id] = $('#boom-poster-' + item.id)
                            .css('-webkit-transform', 'translate3d(0, 0, 0)')
                            .get(0);
                    }
                }
            }
        }

        $('#boom-menu, #boom-movie-grid-container, #boom-grid-focus').velocity(
            {translateZ: 0, left: '+=780'}
          , {
                duration: ka.settings.durationNormal
              , progress: function (elements, percentComplete) {
                    elements[1].style.opacity = 1 - percentComplete / 2;    /* #boom-movie-grid-container   */
                    elements[2].style.opacity = 1 - percentComplete;        /* #boom-grid-focus           */

                    $.each(ka.state.desaturationImageCache, function (key, value) {
                        value.style.webkitFilter = 'saturate(' + Math.round(100 - 100 * percentComplete) + '%)';
                    });
                }
              , complete: function () {
                    ka.lib.grid.unocclude();

                    ka.state.view = 'config';
                }
            }
        );
    }

  , detail: function (movieObj, isCompilationSelected) {
        ka.state.view = 'limbo';

        $('#boom-movie-detail').css('display', 'block');

        ka.lib.grid.snapshotMovieLookups();

        ka.state.lastGridMovieId = movieObj.id;

        ka.lib.updateDetailBrowserInfo(movieObj, false);

        if (!isCompilationSelected) {
            ka.lib.grid.occlude();
        }

        if (ka.lib.browser.isExpanded()) {
            ka.lib.browser.poster.setSource(movieObj);
        }

        var targetElements = (isCompilationSelected) ? $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail') : $('#boom-movie-grid-container, #boom-grid-focus, #boom-movie-detail');
        targetElements.velocity({translateZ: 0, left: '-=1920'}, {
            duration: ka.settings.durationLong
          , complete: function () {
                if (!isCompilationSelected) {
                    ka.lib.grid.unocclude();
                }

                ka.lib.browser.backdrop.fadeIn(movieObj);

                if (ka.lib.browser.isExpanded()) {
                    ka.lib.browser.posters.hide();
                } else {
                    ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

                    ka.lib.browser.focus.reposition();
                    ka.lib.browser.posters.show();
                }
                ka.state.view = 'detail';
            }
        });
    }

  , compilation: function () {
        ka.state.view = 'limbo';

        ka.lib.grid.occlude();

        ka.lib.populateCompilationGrid();

        $('.boom-movie-grid-info-overlay').removeClass('active');
        ka.lib.openCompilation(function () {
            ka.state.view = 'grid-compilation';
        });
    }
}};


ka.transition.compilation = {to: {

    grid: function () {
        ka.state.view = 'limbo';

        ka.lib.closeCompilation(function () {
             var id = ka.lib.getFirstMovieObjectFromCoord(ka.state.gridFocusX, ka.lib.getGridFocusAbsoluteY()).id;

            ka.lib.recalcMovieGrid();
            ka.lib.recalcPositionById(id);

            ka.lib.grid.unocclude();
            ka.lib.updateMovieGridOnChange();

            ka.lib.repositionGrid();

            ka.state.view = 'grid';
        });
    }

}};


ka.transition.detail = {to: {

    grid: function () {
        ka.state.view = 'limbo';

        var currentDetailMovieId = $('#boom-movie-detail').data('boom.id'),
            hasOpenCompilation = ka.state.currentCompilationPosterCount > 0;

        if (currentDetailMovieId != ka.state.lastGridMovieId) {
            ka.state.lastGridMovieId = currentDetailMovieId;

            if (hasOpenCompilation) {
                hasOpenCompilation = false;

                ka.lib.dissolveCompilation();

                ka.lib.grid.unocclude();
            }

            ka.lib.recalcPositionById(currentDetailMovieId);
            ka.lib.repositionGrid(true);  /* offscreen */
        }

        if (!hasOpenCompilation) {
            ka.lib.grid.focus.show();

            ka.lib.grid.occlude();
        }

        var targetElements = (hasOpenCompilation) ? $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail') : $('#boom-movie-grid-container, #boom-grid-focus, #boom-movie-detail');
        targetElements.velocity({translateZ: 0, left: '+=1920'}, {
            duration: ka.settings.durationLong
          , complete: function () {
                if (!hasOpenCompilation) {
                    ka.lib.grid.unocclude();
                }

                var restoreElements = '#boom-detail-browser';
                if (ka.lib.browser.isHidden()) {
                    if (ka.lib.browser.isExpanded()) {
                        $('#boom-detail-panel').data('boom.isHidden', false).velocity({bottom: '+=470'}, 0);
                    } else {
                        $('#boom-detail-panel').data('boom.isHidden', false).velocity({bottom: '+=247'}, 0);
                    }
                } else {
                    if (!ka.lib.browser.isExpanded()) {
                        restoreElements += ', #boom-detail-focus';
                    }
                }

                $(restoreElements).velocity({bottom: '-=247'}, {duration: 0, complete: function () {
                    $('#boom-movie-detail, #boom-detail-browser, #boom-detail-focus').css('display', 'none');
                    $('#boom-detail-browser img').each(ka.lib._detachSmallBrowserPoster);
                }});

                $('#boom-movie-detail').css('display', 'none');

                ka.lib.browser.backdrop.removeAll();

                if (hasOpenCompilation) {
                    ka.state.view = 'grid-compilation';
                } else {
                    ka.state.view = 'grid';
                }
            }
        });
    }

  , compilation: function () {
        ka.state.view = 'limbo';

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail').velocity(
            {translateZ: 0, left: '+=1920'}, {
                duration: ka.settings.durationLong
              , complete: function () {
                    $('#boom-movie-detail').css('display', 'none');

                    ka.state.view = 'grid-compilation';
                }
            }
        );
    }

}};
