/**
 *  Transitions between GUI screens.
 *
 *  @author Nikola Klaric (nikola@klaric.org)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('transition' in ka)) ka.transition = {};


ka.transition.menu = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.view = 'limbo';

        /* ka.lib.occludeMovieGrid(); */
        ka.lib.grid.occlude();

        $('#boom-menu, #boom-movie-grid-container, #boom-grid-focus').velocity(
            {translateZ: 0, left: '-=780'}
          , {
                duration: ka.settings.durationNormal
              , progress: function (elements, percentComplete) {
                    elements[1].style.opacity = 0.5 + percentComplete / 2;
                    elements[2].style.opacity = percentComplete;

                    $.each(ka.state.desaturationImageCache, function (key, value) {
                        value.style.webkitFilter = 'grayscale(' + Math.round(100 - 100 * percentComplete) + '%)';
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

    menu: function () {     /* screen state transition: OK */
        ka.state.view = 'limbo';

        $('#boom-menu').css('display', 'block');

        /* ka.lib.occludeMovieGrid(); */
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
                        value.style.webkitFilter = 'grayscale(' + Math.round(100 * percentComplete) + '%)';
                    });
                }
              , complete: function () {
                    /* ka.lib.unoccludeMovieGrid(); */
                    ka.lib.grid.unocclude();

                    ka.state.view = 'config';
                }
            }
        );
    }

  , detail: function (movieObj, isCompilationSelected) {   /* screen state transition: OK */
        ka.state.view = 'limbo';

        /* var movieObj = ka.lib.getVariantFromGridFocus(); */
        ka.state.lastGridMovieId = movieObj.id;

        ka.lib.updateDetailBrowserInfo(movieObj, false);

        ka.lib.browser.backdrop.init();
        if (movieObj.isBackdropCached) {
            ka.lib.browser.backdrop.setImmediate(movieObj);
        } else {
            ka.lib.browser.backdrop.clear();
        }

        /* ka.lib.updateDetailButtonSelection(); */

        if (!isCompilationSelected) {
            /* ka.lib.occludeMovieGrid(); */
            ka.lib.grid.occlude();
        }

        ka.lib.browser.show();

        var targetElements = (isCompilationSelected) ? $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail') : $('#boom-movie-grid-container, #boom-grid-focus, #boom-movie-detail');
        targetElements.velocity({translateZ: 0, left: '-=1920'}, {
            duration: ka.settings.durationLong
          , complete: function () {
                if (isCompilationSelected) {

                } else {
                    ka.lib.grid.focus.hide();
                }

                ka.lib.grid.snapshotMovieLookups();

                if (ka.lib.browser.isExpanded()) {
                    ka.lib.browser.poster.setSource(movieObj.keyPoster);
                    if (!movieObj.isBackdropCached) {
                            ka.lib.browser.backdrop.loadOptimistic(movieObj);
                        }
                    ka.lib.browser.posters.fadeUp();

                    ka.state.view = 'detail';
                } else {
                    ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

                    ka.lib.browser.focus.reposition();
                    ka.lib.browser.posters.show(function () {
                        if (!movieObj.isBackdropCached) {
                            ka.lib.browser.backdrop.loadOptimistic(movieObj);
                        }

                        ka.state.view = 'detail';
                    });
                }
            }
        });
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.view = 'limbo';

        /* ka.state.mustUndoCompilationChanges = true; */

        /* ka.lib.occludeMovieGrid(); */
        ka.lib.grid.occlude();

        ka.lib.populateCompilationGrid();

        $('.boom-movie-grid-info-overlay').removeClass('active');
        ka.lib.openCompilation(function () {
            ka.state.view = 'grid-compilation';
        });
    }
}};


ka.transition.compilation = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.view = 'limbo';

        ka.lib.closeCompilation(function () {
             var id = ka.lib.getFirstMovieObjectFromCoord(ka.state.gridFocusX, ka.lib.getGridFocusAbsoluteY()).id;

            ka.lib.recalcMovieGrid();
            ka.lib.recalcPositionById(id);

            ka.lib.grid.unocclude();
            ka.lib.updateMovieGridOnChange();

            ka.lib.repositionMovieGrid();
            ka.lib.repositionMovieFocus();

            ka.state.view = 'grid';
        });
    }

  , detail: function () {   /* screen state transition: OK */
        ka.state.actualScreenMode = 'grid-compilation';
        ka.state.view = 'limbo';

        ka.lib.grid.snapshotMovieLookups();

        var movieObj = ka.lib.getVariantFromGridFocus()[ka.state.currentCompilationFocusIndex];

        ka.state.lastGridMovieId = movieObj.id;
        /* ka.state.actualScreenMode = null; */

        ka.lib.updateDetailPage(movieObj, false, true); /* refresh backdrop, too, and use the non-collection title */
        ka.lib.updateDetailButtonSelection();

        ka.state.actualScreenMode = null;

        $('#boom-movie-detail').velocity('fadeIn', {
            duration: 0
          , complete: function () {
                $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, {
                    duration: ka.settings.durationLong
                  /* , delay: ka.settings.durationVeryShort */
                  , complete: function () {
                        ka.state.view = 'detail';
                    }
                });
            }
        });
    }

}};


ka.transition.detail = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.view = 'limbo';

        var currentDetailMovieId = $('#boom-movie-detail').data('boom.id'),
            hasOpenCompilation = ka.state.currentCompilationPosterCount > 0;

        if (currentDetailMovieId != ka.state.lastGridMovieId) {
            ka.state.lastGridMovieId = currentDetailMovieId;

            if (hasOpenCompilation) {
                hasOpenCompilation = false;

                ka.lib.dissolveCompilation();
            }

            ka.lib.grid.unocclude();

            ka.lib.recalcMovieGrid();
            ka.lib.updateMovieGridOnChange();

            ka.lib.recalcPositionById(currentDetailMovieId);
            ka.lib.repositionMovieGrid();
            ka.lib.repositionMovieFocus(true); /* offscreen */

            ka.lib.grid.occlude();
        }

        if (!hasOpenCompilation) {
            ka.lib.grid.focus.show();
        }

        var targetElements = (hasOpenCompilation) ? $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail') : $('#boom-movie-grid-container, #boom-grid-focus, #boom-movie-detail');
        targetElements.velocity({translateZ: 0, left: '+=1920'}, {
            duration: ka.settings.durationLong
          , complete: function () {
                ka.lib.grid.unocclude();

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
                    $('#boom-detail-browser img').each(ka.lib._detachBrowserPoster);
                }});

                if (ka.lib.browser.isExpanded()) {
                    ka.lib.browser.poster.hide();
                }

                if (hasOpenCompilation) {
                    ka.state.view = 'grid-compilation';
                } else {
                    ka.state.view = 'grid';
                }
            }});
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.view = 'limbo';

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: ka.settings.durationLong, complete: function () {
                $('#boom-movie-detail').velocity('fadeOut', 0);

                ka.state.view = 'grid-compilation';
            }});
    }

  , browser: function () {
        ka.state.view = 'limbo';

        ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

        ka.lib.updateDetailBrowserInfo(ka.data.byId[$('#boom-movie-detail').data('boom.id')], false);

        var leftPos = 1110 + 2 + 160 * ka.state.currentDetailBrowserPosterColumn;
        $('#boom-detail-focus').velocity({left: leftPos}, 0);

        $('#boom-detail-panel').velocity('fadeIn', {duration: 0, display: 'block', complete: function () {
            if (ka.state.currentDetailButton == 'details') {
                $('#boom-movie-detail-shade').velocity({opacity: 0}, ka.settings.durationNormal);
                $('#boom-movie-detail-description').velocity('transition.expandOut', ka.settings.durationNormal);
            }

            $('#boom-movie-detail-right').velocity({translateZ: 0, marginLeft: '+=40'}, {duration: ka.settings.durationNormal, easing: 'linear'});
            $('#boom-movie-detail-left').velocity({translateZ: 0, left: '-=360'}, ka.settings.durationNormal);
            $('#boom-detail-panel, #boom-detail-focus').velocity({translateZ: 0, bottom: '+=247'}, {
                duration: ka.settings.durationNormal
              , complete: function () {
                    ka.state.view = 'detail-browser';
                }
            });
        }});

    }

}};


ka.transition.browser = {to: {

    detail: function () {
        ka.state.view = 'limbo';

        var snapshot = ka.lib.grid.getMovieListSnapshot(),
            movieObj = snapshot[$('#boom-detail-browser :nth-child('
                        + (ka.state.currentDetailBrowserPosterColumn + 2) + ')').data('boom.index')];

        if (movieObj.id != $('#boom-movie-detail').data('boom.id')) {
            $('#boom-movie-detail').data('boom.id', movieObj.id);

            ka.lib.updateDetailPage(movieObj, true); // don't refresh backdrop
            ka.lib.updateDetailButtonSelection(true); // don't animate backdrop shade
        }

        $('#boom-movie-detail-poster-fade-in').velocity('fadeOut', 0);

        $('#boom-movie-detail-right').velocity({translateZ: 0, marginLeft: '-=40'}, {duration: ka.settings.durationNormal, easing: 'linear'});
        $('#boom-movie-detail-left').velocity({translateZ: 0, left: '+=360'}, ka.settings.durationNormal);
        $('#boom-detail-panel, #boom-detail-focus').velocity({translateZ: 0, bottom: '-=247'}, {
            duration: ka.settings.durationNormal
          , complete: function () {
                $('#boom-detail-panel').velocity('fadeOut', {duration: 0, display: 'none', complete: function () {
                    /* $('#boom-detail-browser').empty(); */
                    $('#boom-detail-browser img').each(ka.lib._detachBrowserPoster);

                    ka.state.view = 'detail';
                }});
            }
        });

    }

}};
