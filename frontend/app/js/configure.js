/**
 *  Configurator screen.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {};

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

            $('#boom-button-selection-floater').velocity({top: '-=50'}, {duration: 120});
        }
    }
}


function handleKeypressDown() {
    if (ka.state.currentChoice === null) {
        demandInitialChoice();
    } else if (ka.state.currentChoice == 'left') {
        if (ka.state.currentDriveIndex + 1 < ka.data.drives.length) {
            ka.state.currentDriveIndex += 1;

            $('#boom-button-selection-floater').velocity({top: '+=50'}, {duration: 120});
        } else if (ka.state.currentDriveIndex + 1 == ka.data.drives.length && ka.state.hasDrivesSelected) {
            ka.state.isStartButtonSelected = true;

            $('#boom-button-selection-floater').css('opacity', 0);
            $('#boom-button-start-floater').css({
                opacity: 1
              , backgroundColor: 'rgb(0, 116, 217)'
            });
            $('#boom-choice-confirm .boom-button').css('display', 'inline-block');
        }
    }
}


function handleKeypressLeft() {
    if (ka.state.currentChoice == 'left') {
        return;
    } else if (ka.state.currentChoice === null) {
        ka.state.currentDriveIndex = 0;
        ka.state.initialChoiceMade = true;

        $('#boom-choice-right, #boom-choice-splitter').velocity('fadeOut', {display: null, duration: ka.settings.durationNormal});
        $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: ka.settings.durationNormal, complete: function (elements) {
            $('#boom-button-selection-floater').css('opacity', 1);
        }});

        if (ka.state.hasDrivesSelected) {
            $('#boom-choice-confirm .boom-button').velocity('fadeIn', {display: 'inline-block', duration: ka.settings.durationNormal});
        }
    } else {
        if (!ka.state.isStartButtonSelected) {
            $('#boom-button-start-floater').velocity({opacity: 0, backgroundColorGreen: 0, backgroundColorBlue: 0}, ka.settings.durationLong);
        }

        $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: ka.settings.durationNormal, easing: 'ease-in'});
        $('#boom-choice-left, #boom-choice-splitter').velocity('fadeIn', {display: null, duration: ka.settings.durationNormal});
        $('#boom-choice-right').velocity('fadeOut', {display: null, duration: ka.settings.durationNormal, complete: function (elements) {
            if (!ka.state.hasDrivesSelected) {
                $('#boom-choice-confirm .boom-button').velocity('fadeOut', {display: 'inline-block', duration: ka.settings.durationNormal});
            }

            $('#boom-choice-splitter').velocity('fadeOut', {display: null, duration: ka.settings.durationNormal});
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

        /* TODO: 'null' correct? */
        $('#boom-choice-left, #boom-choice-splitter').velocity('fadeOut', {display: null, duration: ka.settings.durationNormal});
        $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: ka.settings.durationNormal});
        $('#boom-choice-confirm .boom-button').velocity('fadeIn', {display: 'inline-block', duration: ka.settings.durationNormal});
    } else {
        $('#boom-button-selection-floater').css('opacity', 0);
        $('#boom-button-start-floater').velocity({opacity: 1, backgroundColorGreen: 116, backgroundColorBlue: 217}, ka.settings.durationLong);

        $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: ka.settings.durationNormal, easing: 'ease-in'});
        $('#boom-choice-right, #boom-choice-splitter').velocity('fadeIn', {display: null, duration: ka.settings.durationNormal});
        $('#boom-choice-left').velocity('fadeOut', {display: null, duration: ka.settings.durationNormal, complete: function (elements) {
            $('#boom-choice-splitter').velocity('fadeOut', {display: null, duration: ka.settings.durationNormal});
            $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: ka.settings.durationNormal, easing: 'ease-out'});

            if (!ka.state.hasDrivesSelected) {
                $('#boom-choice-confirm .boom-button').velocity('fadeIn', {display: 'inline-block', duration: ka.settings.durationNormal});
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
                $('#boom-choice-confirm .boom-button').velocity('fadeIn', {display: 'inline-block', duration: ka.settings.durationNormal});
            } else if (!ka.state.hasDrivesSelected && previouslySelected) {
                $('#boom-choice-confirm .boom-button').velocity('fadeOut', {display: 'none', duration: ka.settings.durationNormal});
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
        ka.state.socketDispatcher.push('loopback:command', 'shutdown');
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
            $('<div id="spinner"><div><img src="/loader.gif"></div></div>').appendTo('body');
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


/* Prevent all input events. */
document.oncontextmenu = document.onmousedown = function (event) { event.preventDefault(); };


$(document).ready(function () {
    registerListener();
    registerHotkeys();

    /* Preload spinner. */
    var image = new Image();
    image.src = '/loader.gif';

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

                    $('#boom-panel').velocity('fadeIn', ka.settings.durationNormal);
                }
            });
        }
    });
});
