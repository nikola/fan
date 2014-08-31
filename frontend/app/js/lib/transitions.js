/**
 *  Transitions between GUI screens.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('transition' in ka)) ka.transition = {};


ka.transition.menu = {to: {

    grid: function () {
        ka.state.currentPageMode = 'grid';

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({translateZ: 0, left: '-=780', opacity: '+=0.5'}, 360);
        $('#boom-poster-focus').velocity({translateZ: 0, left: '-=780', opacity: '+=1'}, 360);
        $('#boom-movie-config').velocity({translateZ: 0, left: '-=780'}, {duration: 360});

        ka.lib.undesaturateVisiblePosters();
    }

}};


ka.transition.grid = {to: {

    menu: function () {
        ka.state.currentPageMode = 'config';

        $('#boom-movie-grid-container, #boom-movie-detail').velocity({translateZ: 0, left: '+=780', opacity: '-=0.5'}, 360);
        $('#boom-poster-focus').velocity({translateZ: 0, left: '+=780', opacity: '-=1'}, 360);
        $('#boom-movie-config').velocity({translateZ: 0, left: '+=780'}, {duration: 360});

        ka.lib.desaturateVisiblePosters();
    }

  , detail: function () {
        ka.lib.occludeMovieGrid();

        var obj = ka.lib.getVariantFromGridFocus();

        ka.state.currentPageMode = 'detail';
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

            $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, 720);
        });

    }

  , compilation: function () {
        ka.lib.occludeMovieGrid();

        ka.state.currentPageMode = 'limbo';

        ka.lib.populateCompilationGrid();

        $('.boom-movie-grid-info-overlay').removeClass('active');
        ka.lib.zoomOutGridPage(function () {
            ka.state.currentPageMode = 'grid-compilation';
        });
    }
}};


ka.transition.compilation = {to: {

    grid: function () {
        ka.state.currentPageMode = 'grid';

        ka.lib.zoomInGridPage(ka.lib.updateMovieGridOnReturn);
    }

  , detail: function () {
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
            ka.state.currentPageMode = 'detail';

            ka.lib.updateDetailButtonSelection();

            $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail').velocity({translateZ: 0, left: '-=1920'}, 720);
        });
    }

}};


ka.transition.detail = {to: {

    grid: function () {
        ka.state.currentPageMode = 'grid';

        $('#boom-movie-grid-container, #boom-poster-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, {duration: 720, complete: ka.lib.updateMovieGridOnReturn});
    }

  , compilation: function () {
        ka.state.currentPageMode = 'grid-compilation';

        $('#boom-compilation-container, #boom-compilation-focus, #boom-movie-detail')
            .velocity({translateZ: 0, left: '+=1920'}, 720);
    }

}};
