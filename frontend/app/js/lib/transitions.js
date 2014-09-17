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

        ka.lib.occludeMovieGrid();

        $('#boom-movie-config, #boom-movie-grid-container, #boom-poster-focus').velocity(
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
                    ka.lib.unoccludeMovieGrid();

                    ka.state.currentPageMode = 'grid';

                    $.each(ka.state.desaturationImageCache, function (key, value) {
                        value.style.webkitFilter = null;
                        value.style.webkitTransform = 'none';
                    });
                    ka.state.desaturationImageCache = {};

                    $('#boom-movie-detail').css('display', 'block');
                }
            }
        );
    }

}};


ka.transition.grid = {to: {

    menu: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-movie-detail').css('display', 'none');

        ka.lib.occludeMovieGrid();

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

        $('#boom-movie-config, #boom-movie-grid-container, #boom-poster-focus').velocity(
            {translateZ: 0, left: '+=780'}
          , {
                duration: 360
              , progress: function (elements, percentComplete) {
                    elements[1].style.opacity = 1 - percentComplete / 2;
                    elements[2].style.opacity = 1 - percentComplete;

                    $.each(ka.state.desaturationImageCache, function (key, value) {
                        value.style.webkitFilter = 'grayscale(' + Math.round(100 * percentComplete) + '%)';
                    });
                }
              , complete: function () {
                    ka.lib.unoccludeMovieGrid();

                    ka.state.currentPageMode = 'config';
                }
            }
        );
    }

  , detail: function () {   /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        var movieObj = ka.lib.getVariantFromGridFocus();
        ka.state.lastGridMovieUuid = movieObj.uuid;

        ka.lib.updateDetailPage(movieObj); /* refresh backdrop, too */
        ka.lib.updateDetailButtonSelection();

        ka.lib.occludeMovieGrid();

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, {
            duration: ka.settings.durationLong
          /* , delay: ka.settings.durationVeryShort */
          , complete: function () {
                ka.state.currentPageMode = 'detail';
                ka.state.actualScreenMode = null;

                ka.lib.grid.snapshotMovieLookups();

                ka.lib.grid.focus.hide();
            }
        });
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        /* ka.state.mustUndoCompilationChanges = true; */

        ka.lib.occludeMovieGrid();

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
            ka.lib.unoccludeMovieGrid();

            ka.lib.updateMovieGridRefocused(false);

            /* ka.lib.updateMovieGridOnReturn(); */
            ka.state.currentPageMode = 'grid';
        });
    }

  , detail: function () {   /* screen state transition: OK */
        ka.state.actualScreenMode = 'grid-compilation';
        ka.state.currentPageMode = 'limbo';

        ka.lib.grid.snapshotMovieLookups();

        var movieObj = ka.lib.getVariantFromGridFocus()[ka.state.currentCompilationFocusIndex];

        ka.state.lastGridMovieUuid = movieObj.uuid;
        ka.state.actualScreenMode = null;

        ka.lib.updateDetailPage(movieObj); /* refresh backdrop, too */
        ka.lib.updateDetailButtonSelection();

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, {
            duration: ka.settings.durationLong
          /* , delay: ka.settings.durationVeryShort */
          , complete: function () {
                ka.state.currentPageMode = 'detail';
            }
        });
    }

}};


ka.transition.detail = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        ka.lib.grid.focus.show();

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: ka.settings.durationLong, complete: function () {
                /* No refocus necessary here, as updateMovieGridOnAdd has been called previously. */
                /* ka.lib.updateMovieGridOnReturn(); */
                ka.lib.unoccludeMovieGrid();

                ka.lib.recalcMovieGrid();
                ka.lib.updateMovieGridOnChange();

                ka.state.currentPageMode = 'grid';
                /* ka.state.mustUndoCompilationChanges = false; */
            }});
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: ka.settings.durationLong, complete: function () {
                ka.state.currentPageMode = 'grid-compilation';
                /* ka.state.mustUndoCompilationChanges = false; */
            }});
    }

  , browser: function () {
        ka.state.currentPageMode = 'limbo';

        ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

        /* ka.lib.updateDetailBrowserInfo(ka.data.byUuid[ka.state.currentGridMovieUuid], false); */
        ka.lib.updateDetailBrowserInfo(ka.data.byUuid[$('#boom-movie-detail').data('boom.uuid')], false);

        var leftPos = 3 + 160 * ka.state.currentDetailBrowserPosterColumn;
        $('#boom-movie-detail-browser-focus').velocity({left: leftPos}, 0);

        $('#boom-movie-detail-head').velocity('fadeIn', {duration: 0, complete: function () {
            if (ka.state.currentDetailButton == 'details') {
                $('#boom-movie-detail-shade').velocity({opacity: 0}, ka.settings.durationNormal);
                $('#boom-movie-detail-description').velocity('transition.expandOut', ka.settings.durationNormal);
            }

            $('#boom-movie-detail-left').velocity({left: '-=360'}, ka.settings.durationNormal);
            $('#boom-movie-detail-head, #boom-movie-detail-browser-focus').velocity({top: '-=245'}, {
                duration: ka.settings.durationNormal
              , complete: function () {
                    ka.state.currentPageMode = 'detail-browser';
                }
            });
        }});
        $('#boom-movie-detail-right').velocity({marginLeft: '+=40'}, {duration: ka.settings.durationNormal, easing: 'linear'});
    }

}};


ka.transition.browser = {to: {

    detail: function () {
        ka.state.currentPageMode = 'limbo';

        var snapshot = ka.lib.grid.getMovieListSnapshot(),
            movieObj = snapshot[$('#boom-movie-detail-poster-browser :nth-child('
                        + (ka.state.currentDetailBrowserPosterColumn + 2) + ')').data('boom.index')];

        if (movieObj.uuid != $('#boom-movie-detail').data('boom.uuid')) {
            $('#boom-movie-detail').data('boom.uuid', movieObj.uuid);

            ka.lib.updateDetailPage(movieObj, true); /* don't refresh backdrop */
            ka.lib.updateDetailButtonSelection(true); /* don't animate backdrop shade */
        }

        $('#boom-movie-detail-left').velocity({left: '+=360'}, ka.settings.durationNormal);
        $('#boom-movie-detail-head, #boom-movie-detail-browser-focus').velocity({top: '+=245'}, {duration: ka.settings.durationNormal, complete: function () {
            $('#boom-movie-detail-head').velocity('fadeOut', {duration: 0, complete: function () {
                $('#boom-movie-detail-poster-browser').empty();

                ka.state.currentPageMode = 'detail';
            }});
        }});
        $('#boom-movie-detail-right').velocity({marginLeft: '-=40'}, {duration: ka.settings.durationNormal, easing: 'linear'});
    }

}};
