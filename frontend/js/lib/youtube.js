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
