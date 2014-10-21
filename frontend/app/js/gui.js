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

/*! LAB.js (LABjs :: Loading And Blocking JavaScript)
    v2.0.3 (c) Kyle Simpson
    MIT License
*/
; (function(o){var K=o.$LAB,y="UseLocalXHR",z="AlwaysPreserveOrder",u="AllowDuplicates",A="CacheBust",B="BasePath",C=/^[^?#]*\//.exec(location.href)[0],D=/^\w+\:\/\/\/?[^\/]+/.exec(C)[0],i=document.head||document.getElementsByTagName("head"),L=(o.opera&&Object.prototype.toString.call(o.opera)=="[object Opera]")||("MozAppearance"in document.documentElement.style),q=document.createElement("script"),E=typeof q.preload=="boolean",r=E||(q.readyState&&q.readyState=="uninitialized"),F=!r&&q.async===true,M=!r&&!F&&!L;function G(a){return Object.prototype.toString.call(a)=="[object Function]"}function H(a){return Object.prototype.toString.call(a)=="[object Array]"}function N(a,c){var b=/^\w+\:\/\//;if(/^\/\/\/?/.test(a)){a=location.protocol+a}else if(!b.test(a)&&a.charAt(0)!="/"){a=(c||"")+a}return b.test(a)?a:((a.charAt(0)=="/"?D:C)+a)}function s(a,c){for(var b in a){if(a.hasOwnProperty(b)){c[b]=a[b]}}return c}function O(a){var c=false;for(var b=0;b<a.scripts.length;b++){if(a.scripts[b].ready&&a.scripts[b].exec_trigger){c=true;a.scripts[b].exec_trigger();a.scripts[b].exec_trigger=null}}return c}function t(a,c,b,d){a.onload=a.onreadystatechange=function(){if((a.readyState&&a.readyState!="complete"&&a.readyState!="loaded")||c[b])return;a.onload=a.onreadystatechange=null;d()}}function I(a){a.ready=a.finished=true;for(var c=0;c<a.finished_listeners.length;c++){a.finished_listeners[c]()}a.ready_listeners=[];a.finished_listeners=[]}function P(d,f,e,g,h){setTimeout(function(){var a,c=f.real_src,b;if("item"in i){if(!i[0]){setTimeout(arguments.callee,25);return}i=i[0]}a=document.createElement("script");if(f.type)a.type=f.type;if(f.charset)a.charset=f.charset;if(h){if(r){e.elem=a;if(E){a.preload=true;a.onpreload=g}else{a.onreadystatechange=function(){if(a.readyState=="loaded")g()}}a.src=c}else if(h&&c.indexOf(D)==0&&d[y]){b=new XMLHttpRequest();b.onreadystatechange=function(){if(b.readyState==4){b.onreadystatechange=function(){};e.text=b.responseText+"\n//@ sourceURL="+c;g()}};b.open("GET",c);b.send()}else{a.type="text/cache-script";t(a,e,"ready",function(){i.removeChild(a);g()});a.src=c;i.insertBefore(a,i.firstChild)}}else if(F){a.async=false;t(a,e,"finished",g);a.src=c;i.insertBefore(a,i.firstChild)}else{t(a,e,"finished",g);a.src=c;i.insertBefore(a,i.firstChild)}},0)}function J(){var l={},Q=r||M,n=[],p={},m;l[y]=true;l[z]=false;l[u]=false;l[A]=false;l[B]="";function R(a,c,b){var d;function f(){if(d!=null){d=null;I(b)}}if(p[c.src].finished)return;if(!a[u])p[c.src].finished=true;d=b.elem||document.createElement("script");if(c.type)d.type=c.type;if(c.charset)d.charset=c.charset;t(d,b,"finished",f);if(b.elem){b.elem=null}else if(b.text){d.onload=d.onreadystatechange=null;d.text=b.text}else{d.src=c.real_src}i.insertBefore(d,i.firstChild);if(b.text){f()}}function S(c,b,d,f){var e,g,h=function(){b.ready_cb(b,function(){R(c,b,e)})},j=function(){b.finished_cb(b,d)};b.src=N(b.src,c[B]);b.real_src=b.src+(c[A]?((/\?.*$/.test(b.src)?"&_":"?_")+~~(Math.random()*1E9)+"="):"");if(!p[b.src])p[b.src]={items:[],finished:false};g=p[b.src].items;if(c[u]||g.length==0){e=g[g.length]={ready:false,finished:false,ready_listeners:[h],finished_listeners:[j]};P(c,b,e,((f)?function(){e.ready=true;for(var a=0;a<e.ready_listeners.length;a++){e.ready_listeners[a]()}e.ready_listeners=[]}:function(){I(e)}),f)}else{e=g[0];if(e.finished){j()}else{e.finished_listeners.push(j)}}}function v(){var e,g=s(l,{}),h=[],j=0,w=false,k;function T(a,c){a.ready=true;a.exec_trigger=c;x()}function U(a,c){a.ready=a.finished=true;a.exec_trigger=null;for(var b=0;b<c.scripts.length;b++){if(!c.scripts[b].finished)return}c.finished=true;x()}function x(){while(j<h.length){if(G(h[j])){try{h[j++]()}catch(err){}continue}else if(!h[j].finished){if(O(h[j]))continue;break}j++}if(j==h.length){w=false;k=false}}function V(){if(!k||!k.scripts){h.push(k={scripts:[],finished:true})}}e={script:function(){for(var f=0;f<arguments.length;f++){(function(a,c){var b;if(!H(a)){c=[a]}for(var d=0;d<c.length;d++){V();a=c[d];if(G(a))a=a();if(!a)continue;if(H(a)){b=[].slice.call(a);b.unshift(d,1);[].splice.apply(c,b);d--;continue}if(typeof a=="string")a={src:a};a=s(a,{ready:false,ready_cb:T,finished:false,finished_cb:U});k.finished=false;k.scripts.push(a);S(g,a,k,(Q&&w));w=true;if(g[z])e.wait()}})(arguments[f],arguments[f])}return e},wait:function(){if(arguments.length>0){for(var a=0;a<arguments.length;a++){h.push(arguments[a])}k=h[h.length-1]}else k=false;x();return e}};return{script:e.script,wait:e.wait,setOptions:function(a){s(a,g);return e}}}m={setGlobalDefaults:function(a){s(a,l);return m},setOptions:function(){return v().setOptions.apply(null,arguments)},script:function(){return v().script.apply(null,arguments)},wait:function(){return v().wait.apply(null,arguments)},queueScript:function(){n[n.length]={type:"script",args:[].slice.call(arguments)};return m},queueWait:function(){n[n.length]={type:"wait",args:[].slice.call(arguments)};return m},runQueue:function(){var a=m,c=n.length,b=c,d;for(;--b>=0;){d=n.shift();a=a[d.type].apply(null,d.args)}return a},noConflict:function(){o.$LAB=K;return m},sandbox:function(){return J()}};return m}o.$LAB=J();(function(a,c,b){if(document.readyState==null&&document[a]){document.readyState="loading";document[a](c,b=function(){document.removeEventListener(c,b,false);document.readyState="complete"},false)}})("addEventListener","DOMContentLoaded")})(this);


var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

ka.data = {
    byId: {}
  , byYear: {}
  , byTitleOriginal: {}
  , byTitleLocalized: {}
  , byRating: {}
  , byBudget: {}
  , asList: []
  , indexById: {}
};

ka.cache = {
    smallBrowserPosterByKey: {}
  , largeBrowserPosterByKey: {}
};

ka.settings = {
    gridMaxRows: 3
  , gridMaxColumns: 7
  , compilationPosterOffsetTop: -18
  , compilationPosterOffsetLeft: 12

  , durationUltraShort: 45
  , durationVeryShort: 90
  , durationShort: 180
  , durationNormal: 360
  , durationLong: 720
};

ka.state = {
    view: 'grid'
  , actualScreenMode: null

  , currentConfigButton: 1

  , lastGridMovieId: null
  , lastGridMovieListSnapshot: null
  , lastGridMovieIndexSnapshot: null

  , currentCompilationFocusIndex: null
  , currentCompilationPosterCount: 0
  , currentCompilationColumnSize: null

  , hasDeferredGridUpdate: false

  , gridSortCriterion: 'byTitleLocalized'
  , gridSortDisplayLanguage: 'localized'
  , gridSortOrder: 'asc'
  , gridFocusX: 0
  , gridFocusY: 0
  , gridPage: 0
  , gridTotalPages: 0
  , detachedGridCells: {}
  , gridLookupMatrix: {}
  , gridLookupItemsPerLine: []
  , gridLookupLinesByKey: {}
  , gridLookupKeyByLine: []
  , gridLookupCoordById: {}
  , shouldFocusFadeIn: true
  , imagePosterPrimaryColorById: {}
  , imagePosterPixelArrayBacklog: []
  , desaturationImageCache: {}
  , isProcessingInitialItems: false
  , processingInitialItemsCount: null
  , isPlayerUpdated: false
  , occludedGridItems: null

  , currentDetailBrowserPosterColumn: null
  , uncachedBackdropDelayTimer: null

  , setOfKnownPosters: {}
  , setOfUnknownPosters: {}
};


function onPageLoaded() {
    var script = window.top.document.getElementsByTagName('script')[0];
    script.parentNode.removeChild(script);

    var url = (location.protocol == 'https:' ? 'wss' : 'ws') + '://' + location.host + '/';
    ka.state.socketDispatcher = new ka.lib.WebSocketDispatcher(url);

    ka.state.socketDispatcher.bind('receive:movie:item', function (movie) {
        ka.state.setOfUnknownPosters[movie.id] = true;

        ka.lib.addMovie(movie);

        ka.lib.updateMovieGridOnAdd(true); /* immediate mode */
    });

    ka.state.socketDispatcher.bind('player:update:complete', function () {
        $('#boom-playback-wait').css('display', 'none');
        ka.state.isPlayerUpdated = true;
    });

    ka.state.socketDispatcher.bind('resume:detail:screen', function () {
        $('#boom-movie-detail').velocity('fadeIn', {duration: ka.settings.durationNormal, complete: function () {
            ka.state.view = 'select-stream';
        }});
    });

    ka.state.socketDispatcher.bind('movie:poster:refresh', function (id) {
        $(".boom-movie-grid-image[src^='/movie/poster/" + id + "']").each(function () {
            $(this).attr('src', $(this).attr('src') + '#' + new Date().getTime());
        });
    });
}


function onBackendReady() {
    var listener = ka.state.hotkeyListener = new keypress.Listener(document.body, {prevent_repeat: true}),
        _hotkeys = ka.config.hotkeys;

     listener.register_many([
        {keys: _hotkeys['firstItem'],       on_keydown: ka.lib.handleKeypressFirstItem}
      , {keys: _hotkeys['lastItem'],        on_keydown: ka.lib.handleKeypressLastItem}
      , {keys: _hotkeys['previousPage'],    on_keydown: ka.lib.handleKeypressPreviousPage}
      , {keys: _hotkeys['nextPage'],        on_keydown: ka.lib.handleKeypressNextPage}
      , {keys: _hotkeys['up'],              on_keydown: ka.lib.handleKeypressUp}
      , {keys: _hotkeys['down'],            on_keydown: ka.lib.handleKeypressDown}
      , {keys: _hotkeys['left'],            on_keydown: ka.lib.handleKeypressLeft}
      , {keys: _hotkeys['right'],           on_keydown: ka.lib.handleKeypressRight}
      , {keys: _hotkeys['toggle'],          on_keydown: ka.lib.handleKeypressToggle}
      , {keys: _hotkeys['select'],          on_keydown: ka.lib.handleKeypressSelect}
      , {keys: _hotkeys['back'],            on_keydown: ka.lib.handleKeypressBack}
    ]);

    listener.sequence_combo('up up down down left right left right b a', function() {
        /* TODO */
    }, true);

    document.body.addEventListener('keypress', ka.lib.handleKeypressAny);

    ka.lib.setupCollator();

    ka.lib.localizeButtons();

    /* Reset config button selection to default. */
    ka.lib.updateMenuButtonSelection();

    $.ajax({
        url: '/movies/all',
        success: function (list) {
            var index = list.length, movie;
            if (index) {
                ka.state.shouldFocusFadeIn = false;
                ka.state.isProcessingInitialItems = true;
                ka.state.processingInitialItemsCount = index;

                while (index--) {
                    movie = list[index];
                    ka.state.setOfKnownPosters[movie.id] = true;
                    ka.lib.addMovie(movie);
                }
                ka.lib.recalcMovieGrid();
                ka.lib.updateMovieGridOnChange();
            } else {
                onPostersLoaded();
            }
        }
    });
}


function onPostersLoaded() {
    window.top.postMessage('', location.protocol + '//' + location.host);
}


document.oncontextmenu = document.onmousedown = document.onselectstart = function (evt) {
    evt.preventDefault();
};


window.onerror = function (message, filename, lineno, colno, error) {
    console.error(message);
};


window.history.pushState(null, null, 'c7b4165ce062400e90f943066564582a');
window.onpopstate = function () {
    window.history.pushState(null, null, 'c7b4165ce062400e90f943066564582a');
};


$LAB.setGlobalDefaults({
    UseLocalXHR: true
  , AlwaysPreserveOrder: true
  , AllowDuplicates: false
  , CacheBust: true
  , BasePath: '/static/js/'
});

$LAB
    .script('thirdparty/mmcq.js')
    .script('thirdparty/jquery.min.js')
    .script('thirdparty/keypress.min.js')
    .script('thirdparty/velocity.min.js')
    .script('thirdparty/velocity.ui.min.js')
    .script('lib/sockets.js')
    .script('lib/colors.js')
    .script('lib/l10n.js')
    .script('lib/db.js')
    .script('lib/hotkeys.js')
    .script('lib/lang.js')
    .script('lib/menu.js')
    .script('lib/grid.js')
    .script('lib/detail.js')
    .script('lib/transitions.js')
    .script('lib/youtube.js')
    .script('lib/credits.js').wait(function () {
        ka.state.maxConfigButton = $('#boom-menu .boom-button').length;
        ka.state.canvasContext = $('#boom-image-sampler-canvas').get(0).getContext('2d');

        $('#boom-movie-detail-poster-foreground').on('load', ka.lib.browser.backdrop.onLoaded);
        $('#boom-detail-large-poster').data('boom.isHidden', true).find('img').on('load', ka.lib.browser.poster.onLoaded);
        $('#boom-detail-watch-trailer').data('boom.type', 'trailer');

        $.get(
            'https://www.youtube.com/iframe_api'
          , null
          , function () {

            }
          , 'script'
        );

        $.ajax({url: '/ready', type: 'PATCH', success: onBackendReady});
    });

/*
console.log(ka.state.canvasContext.webkitBackingStorePixelRatio == 1);
console.log(window.devicePixelRatio == 1);
*/
