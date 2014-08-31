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

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({translateZ: 0, left: '-=780', opacity: '+=0.5'}, 360);
        $('#boom-poster-focus').velocity({translateZ: 0, left: '-=780', opacity: '+=1'}, 360);
        $('#boom-movie-config').velocity({translateZ: 0, left: '-=780'}, {duration: 360, complete: function () {
            ka.state.currentPageMode = 'grid';
        }});

        ka.lib.undesaturateVisiblePosters();
    }

}};


ka.transition.grid = {to: {

    menu: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({translateZ: 0, left: '+=780', opacity: '-=0.5'}, 360);
        $('#boom-poster-focus').velocity({translateZ: 0, left: '+=780', opacity: '-=1'}, 360);
        $('#boom-movie-config').velocity({translateZ: 0, left: '+=780'}, {duration: 360, complete: function () {
            ka.state.currentPageMode = 'config';
        }});

        ka.lib.desaturateVisiblePosters();
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

            $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, {duration: 720, complete: function () {
                ka.state.currentPageMode = 'detail';
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
            ka.lib.updateMovieGridOnReturn();
            ka.state.currentPageMode = 'grid';
        });
    }

  , detail: function () {   /* screen state transition: OK */
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
            ka.lib.updateDetailButtonSelection();

            $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, {duration: 720, complete: function () {
                ka.state.currentPageMode = 'detail';
            }});
        });
    }

}};


ka.transition.detail = {to: {

    grid: function () {     /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: 720, complete: function () {
                ka.lib.updateMovieGridOnReturn();
                ka.state.currentPageMode = 'grid';
            }});
    }

  , compilation: function () {  /* screen state transition: OK */
        ka.state.currentPageMode = 'limbo';

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: 720, complete: function () {
                ka.state.currentPageMode = 'grid-compilation';
            }});
    }

}};
