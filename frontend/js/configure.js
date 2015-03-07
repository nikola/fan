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

/*! LAB.js (LABjs :: Loading And Blocking JavaScript)
    v2.0.3 (c) Kyle Simpson
    MIT License
*/
; (function(o){var K=o.$LAB,y="UseLocalXHR",z="AlwaysPreserveOrder",u="AllowDuplicates",A="CacheBust",B="BasePath",C=/^[^?#]*\//.exec(location.href)[0],D=/^\w+\:\/\/\/?[^\/]+/.exec(C)[0],i=document.head||document.getElementsByTagName("head"),L=(o.opera&&Object.prototype.toString.call(o.opera)=="[object Opera]")||("MozAppearance"in document.documentElement.style),q=document.createElement("script"),E=typeof q.preload=="boolean",r=E||(q.readyState&&q.readyState=="uninitialized"),F=!r&&q.async===true,M=!r&&!F&&!L;function G(a){return Object.prototype.toString.call(a)=="[object Function]"}function H(a){return Object.prototype.toString.call(a)=="[object Array]"}function N(a,c){var b=/^\w+\:\/\//;if(/^\/\/\/?/.test(a)){a=location.protocol+a}else if(!b.test(a)&&a.charAt(0)!="/"){a=(c||"")+a}return b.test(a)?a:((a.charAt(0)=="/"?D:C)+a)}function s(a,c){for(var b in a){if(a.hasOwnProperty(b)){c[b]=a[b]}}return c}function O(a){var c=false;for(var b=0;b<a.scripts.length;b++){if(a.scripts[b].ready&&a.scripts[b].exec_trigger){c=true;a.scripts[b].exec_trigger();a.scripts[b].exec_trigger=null}}return c}function t(a,c,b,d){a.onload=a.onreadystatechange=function(){if((a.readyState&&a.readyState!="complete"&&a.readyState!="loaded")||c[b])return;a.onload=a.onreadystatechange=null;d()}}function I(a){a.ready=a.finished=true;for(var c=0;c<a.finished_listeners.length;c++){a.finished_listeners[c]()}a.ready_listeners=[];a.finished_listeners=[]}function P(d,f,e,g,h){setTimeout(function(){var a,c=f.real_src,b;if("item"in i){if(!i[0]){setTimeout(arguments.callee,25);return}i=i[0]}a=document.createElement("script");if(f.type)a.type=f.type;if(f.charset)a.charset=f.charset;if(h){if(r){e.elem=a;if(E){a.preload=true;a.onpreload=g}else{a.onreadystatechange=function(){if(a.readyState=="loaded")g()}}a.src=c}else if(h&&c.indexOf(D)==0&&d[y]){b=new XMLHttpRequest();b.onreadystatechange=function(){if(b.readyState==4){b.onreadystatechange=function(){};e.text=b.responseText+"\n//@ sourceURL="+c;g()}};b.open("GET",c);b.send()}else{a.type="text/cache-script";t(a,e,"ready",function(){i.removeChild(a);g()});a.src=c;i.insertBefore(a,i.firstChild)}}else if(F){a.async=false;t(a,e,"finished",g);a.src=c;i.insertBefore(a,i.firstChild)}else{t(a,e,"finished",g);a.src=c;i.insertBefore(a,i.firstChild)}},0)}function J(){var l={},Q=r||M,n=[],p={},m;l[y]=true;l[z]=false;l[u]=false;l[A]=false;l[B]="";function R(a,c,b){var d;function f(){if(d!=null){d=null;I(b)}}if(p[c.src].finished)return;if(!a[u])p[c.src].finished=true;d=b.elem||document.createElement("script");if(c.type)d.type=c.type;if(c.charset)d.charset=c.charset;t(d,b,"finished",f);if(b.elem){b.elem=null}else if(b.text){d.onload=d.onreadystatechange=null;d.text=b.text}else{d.src=c.real_src}i.insertBefore(d,i.firstChild);if(b.text){f()}}function S(c,b,d,f){var e,g,h=function(){b.ready_cb(b,function(){R(c,b,e)})},j=function(){b.finished_cb(b,d)};b.src=N(b.src,c[B]);b.real_src=b.src+(c[A]?((/\?.*$/.test(b.src)?"&_":"?_")+~~(Math.random()*1E9)+"="):"");if(!p[b.src])p[b.src]={items:[],finished:false};g=p[b.src].items;if(c[u]||g.length==0){e=g[g.length]={ready:false,finished:false,ready_listeners:[h],finished_listeners:[j]};P(c,b,e,((f)?function(){e.ready=true;for(var a=0;a<e.ready_listeners.length;a++){e.ready_listeners[a]()}e.ready_listeners=[]}:function(){I(e)}),f)}else{e=g[0];if(e.finished){j()}else{e.finished_listeners.push(j)}}}function v(){var e,g=s(l,{}),h=[],j=0,w=false,k;function T(a,c){a.ready=true;a.exec_trigger=c;x()}function U(a,c){a.ready=a.finished=true;a.exec_trigger=null;for(var b=0;b<c.scripts.length;b++){if(!c.scripts[b].finished)return}c.finished=true;x()}function x(){while(j<h.length){if(G(h[j])){try{h[j++]()}catch(err){}continue}else if(!h[j].finished){if(O(h[j]))continue;break}j++}if(j==h.length){w=false;k=false}}function V(){if(!k||!k.scripts){h.push(k={scripts:[],finished:true})}}e={script:function(){for(var f=0;f<arguments.length;f++){(function(a,c){var b;if(!H(a)){c=[a]}for(var d=0;d<c.length;d++){V();a=c[d];if(G(a))a=a();if(!a)continue;if(H(a)){b=[].slice.call(a);b.unshift(d,1);[].splice.apply(c,b);d--;continue}if(typeof a=="string")a={src:a};a=s(a,{ready:false,ready_cb:T,finished:false,finished_cb:U});k.finished=false;k.scripts.push(a);S(g,a,k,(Q&&w));w=true;if(g[z])e.wait()}})(arguments[f],arguments[f])}return e},wait:function(){if(arguments.length>0){for(var a=0;a<arguments.length;a++){h.push(arguments[a])}k=h[h.length-1]}else k=false;x();return e}};return{script:e.script,wait:e.wait,setOptions:function(a){s(a,g);return e}}}m={setGlobalDefaults:function(a){s(a,l);return m},setOptions:function(){return v().setOptions.apply(null,arguments)},script:function(){return v().script.apply(null,arguments)},wait:function(){return v().wait.apply(null,arguments)},queueScript:function(){n[n.length]={type:"script",args:[].slice.call(arguments)};return m},queueWait:function(){n[n.length]={type:"wait",args:[].slice.call(arguments)};return m},runQueue:function(){var a=m,c=n.length,b=c,d;for(;--b>=0;){d=n.shift();a=a[d.type].apply(null,d.args)}return a},noConflict:function(){o.$LAB=K;return m},sandbox:function(){return J()}};return m}o.$LAB=J();(function(a,c,b){if(document.readyState==null&&document[a]){document.readyState="loading";document[a](c,b=function(){document.removeEventListener(c,b,false);document.readyState="complete"},false)}})("addEventListener","DOMContentLoaded")})(this);


var ka = ka || {};

ka.data = {
    drives: null
  , sourceByPathname: {}
};

ka.settings = {
    durationVeryShort: 90
  , durationShort: 180
  , durationNormal: 360
  , durationLong: 720
};

ka.state = {
    initialChoiceMade: false
  , currentChoice: null
  , hasDrivesSelected: false
  , currentDriveIndex: null
  , isStartButtonSelected: false
};


function demandInitialChoice() {
    $('#boom-demand-choice').velocity('callout.flash');
}


function handleKeypressUp() {
    if (ka.state.currentChoice === null) {
        demandInitialChoice();
    } else if (ka.state.currentChoice == 'left') {
        if (ka.state.isStartButtonSelected) {
            ka.state.isStartButtonSelected = false;

            $('#boom-button-selection-floater').css('opacity', 1);
            $('#boom-button-start-floater').css({
                opacity: 0
              , backgroundColor: 'rgb(0, 0, 0)'
            });
        } else if (ka.state.currentDriveIndex > 0) {
            ka.state.currentDriveIndex -= 1;

            $('#boom-button-selection-floater').velocity({top: '-=50'}, ka.settings.durationShort);
        }
    }
}


function handleKeypressDown() {
    if (ka.state.currentChoice === null) {
        demandInitialChoice();
    } else if (ka.state.currentChoice == 'left') {
        if (ka.state.currentDriveIndex + 1 < ka.data.drives.length) {
            ka.state.currentDriveIndex += 1;

            $('#boom-button-selection-floater').velocity({top: '+=50'}, ka.settings.durationShort);
        } else if (ka.state.currentDriveIndex + 1 == ka.data.drives.length && ka.state.hasDrivesSelected) {
            ka.state.isStartButtonSelected = true;

            $('#boom-button-selection-floater').css('opacity', 0);
            $('#boom-button-start-floater').css({
                opacity: 1
              , backgroundColor: 'rgb(0, 116, 217)'
            });
        }
    }
}


function handleKeypressLeft() {
    if (ka.state.currentChoice == 'left') {
        return;
    } else if (ka.state.currentChoice === null) {
        ka.state.currentDriveIndex = 0;
        ka.state.initialChoiceMade = true;

        $('#boom-choice-right, #boom-choice-splitter').velocity({opacity: 0}, ka.settings.durationNormal);
        $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: ka.settings.durationNormal, complete: function () {
            $('#boom-button-selection-floater').css('opacity', 1);
        }});

        if (ka.state.hasDrivesSelected) {
            $('#boom-choice-confirm .boom-button').velocity({opacity: 1}, ka.settings.durationNormal);
        }
    } else {
        if (!ka.state.isStartButtonSelected) {
            $('#boom-button-start-floater').velocity({opacity: 0, backgroundColorGreen: 0, backgroundColorBlue: 0}, ka.settings.durationLong);
        }

        $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: ka.settings.durationNormal, easing: 'ease-in'});
        $('#boom-choice-left, #boom-choice-splitter').velocity({opacity: 1}, ka.settings.durationNormal);
        $('#boom-choice-right').velocity({opacity: 0}, {duration: ka.settings.durationNormal, complete: function () {
            if (!ka.state.hasDrivesSelected) {
                $('#boom-choice-confirm .boom-button').velocity({opacity: 0}, ka.settings.durationNormal);
            }

            $('#boom-choice-splitter').velocity({opacity: 0}, ka.settings.durationNormal);
            $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: ka.settings.durationNormal, easing: 'ease-out', complete: function () {
                if (!ka.state.isStartButtonSelected) {
                    $('#boom-button-selection-floater').css('opacity', 1);
                }


            }});
        }});
    }

    ka.state.currentChoice = 'left';
}


function handleKeypressRight() {
    if (ka.state.currentChoice == 'right') return;

    if (ka.state.currentChoice === null) {
        ka.state.initialChoiceMade = true;

        $('#boom-button-start-floater').velocity({opacity: 1, backgroundColorGreen: 116, backgroundColorBlue: 217}, ka.settings.durationNormal);

        $('#boom-choice-left, #boom-choice-splitter').velocity({opacity: 0}, ka.settings.durationNormal);
        $("#boom-split-choices").velocity({marginLeft: '-=420'}, ka.settings.durationNormal);
        $('#boom-choice-confirm .boom-button').velocity({opacity: 1}, ka.settings.durationNormal);
    } else {
        $('#boom-button-selection-floater').css('opacity', 0);
        $('#boom-button-start-floater').velocity({opacity: 1, backgroundColorGreen: 116, backgroundColorBlue: 217}, ka.settings.durationLong);

        $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: ka.settings.durationNormal, easing: 'ease-in'});
        $('#boom-choice-right, #boom-choice-splitter').velocity({opacity: 1}, ka.settings.durationNormal);
        $('#boom-choice-left').velocity({opacity: 0}, {duration: ka.settings.durationNormal, complete: function () {
            $('#boom-choice-splitter').velocity({opacity: 0}, ka.settings.durationNormal);
            $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: ka.settings.durationNormal, easing: 'ease-out'});

            if (!ka.state.hasDrivesSelected) {
                $('#boom-choice-confirm .boom-button').velocity({opacity: 1}, ka.settings.durationNormal);
            }
        }});
    }

    ka.state.currentChoice = 'right';
}


function handleKeypressSelect() {
    if (ka.state.currentChoice === null) {
        demandInitialChoice();
    } else if (ka.state.currentChoice == 'left') {
        if (ka.state.isStartButtonSelected) {
            saveAndProceed();
        } else {
            var checkbox = $('#boom-drives-list li').eq(ka.state.currentDriveIndex).find('i');
            if (checkbox.hasClass('fa-square')) {
                checkbox.removeClass('fa-square').addClass('fa-check-square');
            } else {
                checkbox.removeClass('fa-check-square').addClass('fa-square');
            }

            var previouslySelected = ka.state.hasDrivesSelected;
            ka.state.hasDrivesSelected = $('#boom-drives-list li .fa-check-square').size() > 0;
            if (ka.state.hasDrivesSelected && !previouslySelected) {
                $('#boom-choice-confirm .boom-button').velocity({opacity: 1}, ka.settings.durationNormal);
            } else if (!ka.state.hasDrivesSelected && previouslySelected) {
                $('#boom-choice-confirm .boom-button').velocity({opacity: 0}, ka.settings.durationNormal);
            }
        }
    } else if (ka.state.currentChoice == 'right') {
        saveAndProceed();
    }
}


function handleKeypressQuit() {
    if (window.location.hash == '#return') {
        ka.state.socketDispatcher.push('loopback:redirect', 'return');
    } else {
        console.exitApplication();
    }
}


function registerHotkeys() {
    var listener = new keypress.Listener(document.body, {prevent_repeat: true}),
        _hotkeys = ka.config.hotkeys || {};

     listener.register_many([
        {keys: _hotkeys['up'],              on_keydown: handleKeypressUp}
      , {keys: _hotkeys['down'],            on_keydown: handleKeypressDown}
      , {keys: _hotkeys['left'],            on_keydown: handleKeypressLeft}
      , {keys: _hotkeys['right'],           on_keydown: handleKeypressRight}
      , {keys: _hotkeys['toggle'],          on_keydown: handleKeypressSelect}
      , {keys: _hotkeys['select'],          on_keydown: handleKeypressSelect}
      , {keys: _hotkeys['back'],            on_keydown: handleKeypressQuit}
    ]);
}


function saveAndProceed() {
    var userConfig = ka.config;
    userConfig.isDemoMode = Boolean(ka.state.currentChoice == 'right');

    var sources = [];
    $('#boom-drives-list li').each(function (index) {
        if ($(this).find('i').hasClass('fa-check-square')) {
            sources.push(ka.data.drives[index]);
        }
    });
    userConfig.sources = sources;

    $.post(
        '/update/configuration'
      , JSON.stringify(userConfig)
      , function () {
            $('body div').remove();
            $('<div id="spinner"><div><img src="/static/img/loader.gif"></div></div>').appendTo('body');
        }
    );
}


function registerListener() {
    var url = (location.protocol == 'https:' ? 'wss' : 'ws') + '://' + location.host + '/';
    ka.state.socketDispatcher = new ka.lib.WebSocketDispatcher(url);

    ka.state.socketDispatcher.bind('receive:command:token', function (command) {
        eval(command);
    });

    ka.state.socketDispatcher.bind('force:redirect:url', function (target) {
        window.location.href = target;
    });
}


document.oncontextmenu = document.onmousedown = document.onselectstart = function (evt) {
    evt.preventDefault();
};


window.onerror = function (message, filename, lineno, colno, error) {
    console.error(message);
};


$LAB.setGlobalDefaults({
    UseLocalXHR: true
  , AlwaysPreserveOrder: true
  , AllowDuplicates: false
  , CacheBust: true
  , BasePath: '/static/js/'
});


$LAB
    .script('thirdparty/jquery.min.js')
    .script('thirdparty/keypress.min.js')
    .script('thirdparty/velocity.min.js')
    .script('thirdparty/velocity.ui.min.js')
    .script('lib/sockets.js')
    .script('lib/l10n.js')
    .script('lib/hotkeys.js')
    .script('lib/lang.js')
    .wait(function () {
        registerListener();
        registerHotkeys();

        /* Preload spinner. */
        var image = new Image();
        image.src = '/static/img/loader.gif';

        for (var source, index = 0; source = ka.config.sources[index]; index++) {
            ka.data.sourceByPathname[source.pathname] = source;
        }

        ka.state.hasDrivesSelected = ka.config.sources.length > 0;

        $.ajax({
            url: '/movies/top250',
            success: function (list) {
                for (var index = 0; index < 10; index++) {
                    $('<li>', {
                        text: list[index][0] + ' (' + list[index][1] + ')'
                    }).appendTo('#boom-top250-list');
                }

                $.ajax({
                    url: '/drives/mounted',
                    success: function (list) {
                        ka.data.drives = list.concat();

                        for (var index = 0, drive, className; index < list.length; index++) {
                            drive = list[index];
                            className = (drive.pathname in ka.data.sourceByPathname) ? 'fa-check-square': 'fa-square';
                            $('<li>', {
                                html: '<i class="fa ' + className + '"></i>' + list[index].label + ' (' + list[index].drive + ':)'
                            }).appendTo('#boom-drives-list');
                        }

                        $('#boom-panel').velocity({opacity: 1}, ka.settings.durationNormal);
                    }
                });
            }
        });
    });
