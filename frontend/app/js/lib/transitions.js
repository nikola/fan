/**
 *  Transitions between GUI screens.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('transition' in ka)) ka.transition = {};


ka.transition.menu = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        /* ka.lib.occludeMovieGrid(); */
        ka.lib.grid.occlude();

        $('#boom-movie-config, #boom-movie-grid-container, #boom-grid-focus').velocity(
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

                    $('#boom-movie-config').css('display', 'none');

                    ka.state.currentPageMode = 'grid';
                }
            }
        );
    }

}};


ka.transition.grid = {to: {

    menu: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-movie-config').css('display', 'block');

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
                        ka.state.desaturationImageCache[item.uuid] = $('#boom-poster-' + item.uuid)
                            .css('-webkit-transform', 'translate3d(0, 0, 0)')
                            .get(0);
                    }
                }
            }
        }

        $('#boom-movie-config, #boom-movie-grid-container, #boom-grid-focus').velocity(
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

                    ka.state.currentPageMode = 'config';
                }
            }
        );
    }

  , detail: function (movieObj, isCompilationSelected) {   /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        /* var movieObj = ka.lib.getVariantFromGridFocus(); */
        ka.state.lastGridMovieUuid = movieObj.uuid;

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

                    ka.state.currentPageMode = 'detail';
                } else {
                    ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

                    ka.lib.browser.focus.reposition();
                    ka.lib.browser.posters.show(function () {
                        if (!movieObj.isBackdropCached) {
                            ka.lib.browser.backdrop.loadOptimistic(movieObj);
                        }

                        ka.state.currentPageMode = 'detail';
                    });
                }
            }
        });
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        /* ka.state.mustUndoCompilationChanges = true; */

        /* ka.lib.occludeMovieGrid(); */
        ka.lib.grid.occlude();

        ka.lib.populateCompilationGrid();

        $('.boom-movie-grid-info-overlay').removeClass('active');
        ka.lib.openCompilation(function () {
            ka.state.currentPageMode = 'grid-compilation';
        });
    }
}};


ka.transition.compilation = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        ka.lib.closeCompilation(function () {
             var uuid = ka.lib.getFirstMovieObjectFromCoord(ka.state.gridFocusX, ka.lib.getGridFocusAbsoluteY()).uuid;

            ka.lib.recalcMovieGrid();
            ka.lib.recalcPositionByUuid(uuid);

            ka.lib.grid.unocclude();
            ka.lib.updateMovieGridOnChange();

            ka.lib.repositionMovieGrid();
            ka.lib.repositionMovieFocus();

            ka.state.currentPageMode = 'grid';
        });
    }

  , detail: function () {   /* screen state transition: OK */
        ka.state.actualScreenMode = 'grid-compilation';
        ka.state.currentPageMode = 'limbo';

        ka.lib.grid.snapshotMovieLookups();

        var movieObj = ka.lib.getVariantFromGridFocus()[ka.state.currentCompilationFocusIndex];

        ka.state.lastGridMovieUuid = movieObj.uuid;
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
                        ka.state.currentPageMode = 'detail';
                    }
                });
            }
        });
    }

}};


ka.transition.detail = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        var currentDetailMovieUuid = $('#boom-movie-detail').data('boom.uuid'),
            hasOpenCompilation = ka.state.currentCompilationPosterCount > 0;

        if (currentDetailMovieUuid != ka.state.lastGridMovieUuid) {
            ka.state.lastGridMovieUuid = currentDetailMovieUuid;

            if (hasOpenCompilation) {
                hasOpenCompilation = false;

                ka.lib.dissolveCompilation();
            }

            ka.lib.grid.unocclude();

            ka.lib.recalcMovieGrid();
            ka.lib.updateMovieGridOnChange();

            ka.lib.recalcPositionByUuid(currentDetailMovieUuid);
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
                    $('#boom-detail-browser').empty();
                }});

                if (ka.lib.browser.isExpanded()) {
                    ka.lib.browser.poster.hide();
                }

                if (hasOpenCompilation) {
                    ka.state.currentPageMode = 'grid-compilation';
                } else {
                    ka.state.currentPageMode = 'grid';
                }
            }});
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: ka.settings.durationLong, complete: function () {
                $('#boom-movie-detail').velocity('fadeOut', 0);

                ka.state.currentPageMode = 'grid-compilation';
            }});
    }

  , browser: function () {
        ka.state.currentPageMode = 'limbo';

        ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

        ka.lib.updateDetailBrowserInfo(ka.data.byUuid[$('#boom-movie-detail').data('boom.uuid')], false);

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
                    ka.state.currentPageMode = 'detail-browser';
                }
            });
        }});

    }

}};


ka.transition.browser = {to: {

    detail: function () {
        ka.state.currentPageMode = 'limbo';

        var snapshot = ka.lib.grid.getMovieListSnapshot(),
            movieObj = snapshot[$('#boom-detail-browser :nth-child('
                        + (ka.state.currentDetailBrowserPosterColumn + 2) + ')').data('boom.index')];

        if (movieObj.uuid != $('#boom-movie-detail').data('boom.uuid')) {
            $('#boom-movie-detail').data('boom.uuid', movieObj.uuid);

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
                    $('#boom-detail-browser').empty();

                    ka.state.currentPageMode = 'detail';
                }});
            }
        });

    }

}};
