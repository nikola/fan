/**
 *  YouTube Player API functions.
 *
 *  @author Nikola Klaric (nikola@klaric.org)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('state' in ka)) ka.state = {};

ka.state.youtubePlayerInitialized = false;


function onYouTubeIframeAPIReady() {
    ka.state.movieTrailerPlayer = new YT.Player('boom-movie-trailer', {
        width: '1920', height: '1080', playerVars: {
            autoplay: 1
          , autohide: 1
          , controls: 0
          , enablejsapi: 1
          , hl: 'en'
          , fs: 0
          , disablekb: 1
          , iv_load_policy: 3
          , modestbranding: 1
          , origin: location.protocol + '//' + location.host
          , rel: 0
          , showinfo: 0
        }, events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}


function onPlayerReady(evt) {
    ka.state.movieTrailerPlayer.stopVideo();
    ka.state.movieTrailerPlayer.clearVideo();

    ka.state.youtubePlayerInitialized = true;
}


function onPlayerStateChange(evt) {
    if (ka.state.youtubePlayerInitialized && evt.data == YT.PlayerState.PLAYING) {
        $('#boom-movie-trailer').css('display', 'block');
    } else if (evt.data == YT.PlayerState.ENDED) {
        ka.lib.closeTrailerPlayer();
    }
}
