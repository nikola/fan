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

        ka.lib.occludeMovieGrid();

        var obj = ka.lib.getVariantFromGridFocus();
        ka.state.currentGridMovieUuid = obj.uuid;
        if (!obj.streamless) {
            ka.state.currentDetailButton = 'play';
        } else if (obj.trailer) {
            ka.state.currentDetailButton = 'trailer';
        } else {
            ka.state.currentDetailButton = 'details';
        }

        ka.lib.updateDetailPage(obj, function () {
            ka.lib.updateDetailButtonSelection();

            $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, {duration: ka.settings.durationLong, complete: function () {
                ka.state.currentPageMode = 'detail';
                ka.state.actualScreenMode = null;
            }});
        });

    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        ka.lib.occludeMovieGrid();

        ka.lib.populateCompilationGrid();

        $('.boom-movie-grid-info-overlay').removeClass('active');
        ka.lib.zoomOutGridPage(function () {
            ka.state.currentPageMode = 'grid-compilation';
        });
    }
}};


ka.transition.compilation = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        ka.lib.zoomInGridPage(function () {
            ka.lib.unoccludeMovieGrid();

            ka.lib.updateMovieGridRefocused();

            /* ka.lib.updateMovieGridOnReturn(); */
            ka.state.currentPageMode = 'grid';
        });
    }

  , detail: function () {   /* screen state transition: OK */
        ka.state.actualScreenMode = 'grid-compilation';
        ka.state.currentPageMode = 'limbo';

        var movieObj = ka.lib.getVariantFromGridFocus()[ka.state.currentCompilationFocusIndex];

        ka.state.currentGridMovieUuid = movieObj.uuid;

        if (!movieObj.streamless) {
            ka.state.currentDetailButton = 'play';
        } else if (movieObj.trailer) {
            ka.state.currentDetailButton = 'trailer';
        } else {
            ka.state.currentDetailButton = 'details';
        }

        ka.lib.updateDetailPage(movieObj, function () {
            ka.state.actualScreenMode = 'null';

            ka.lib.updateDetailButtonSelection();

            $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, {duration: ka.settings.durationLong, complete: function () {
                ka.state.currentPageMode = 'detail';
            }});
        });
    }

}};


ka.transition.detail = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: ka.settings.durationLong, complete: function () {
                /* No refocus necessary here, as ka.lib.updateMovieGridOnAdd() has been called previously. */
                ka.lib.updateMovieGridOnReturn();
                ka.state.currentPageMode = 'grid';
            }});
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: ka.settings.durationLong, complete: function () {
                ka.state.currentPageMode = 'grid-compilation';
            }});
    }

  , browser: function () {
        ka.state.currentPageMode = 'limbo';

        ka.state.currentDetailBrowserPosterColumn = ka.lib.populateDetailBrowserGrid();

        ka.lib.updateDetailBrowserInfo(ka.data.byUuid[ka.state.currentGridMovieUuid], false);

        var leftPos = 3 + 160 * ka.state.currentDetailBrowserPosterColumn;
        $('#boom-movie-detail-browser-focus').velocity({left: leftPos}, 0);

        $('#boom-movie-detail-head').velocity('fadeIn', {duration: 0, complete: function () {
            $('#boom-movie-detail-left').velocity({left: '-=360'}, ka.settings.durationNormal);
            $('#boom-movie-detail-head, #boom-movie-detail-browser-focus').velocity({top: '-=245'}, {
                duration: ka.settings.durationNormal
              , complete: function () {
                    ka.state.currentPageMode = 'detail-browser';
                }
            });
        }});
        $('#boom-movie-detail-right').velocity({marginLeft: '+=40'}, ka.settings.durationNormal);
    }

}};


ka.transition.browser = {to: {

    detail: function () {
        ka.state.currentPageMode = 'limbo';

        $('#boom-movie-detail-left').velocity({left: '+=360'}, ka.settings.durationNormal);
        $('#boom-movie-detail-head, #boom-movie-detail-browser-focus').velocity({top: '+=245'}, {duration: ka.settings.durationNormal, complete: function () {
            $('#boom-movie-detail-head').velocity('fadeOut', {duration: 0, complete: function () {
                $('#boom-movie-detail-poster-browser').empty();

                ka.state.currentPageMode = 'detail';
            }});
        }});
        $('#boom-movie-detail-right').velocity({marginLeft: '-=40'}, ka.settings.durationNormal);
    }

}};
