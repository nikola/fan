/**
 *  Configurator screen.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {};

ka.state = {
    initialChoiceMade: false
  , currentChoice: null
  , hasDrivesSelected: false
  , currentDriveIndex: null
};

ka.data = {
    drives: null
};


function demandInitialChoice() {
    // console.log('demand');
}


function handleKeypressUp() {
    if (ka.state.currentChoice === null) {
        demandInitialChoice();
    } else if (ka.state.currentChoice == 'left') {
        if (ka.state.currentDriveIndex > 0) {
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
            $('#boom-button-selection-floater').css('opacity', 0);
            $('#boom-button-start-floater').css('opacity', 1);
            $('#boom-choice-confirm .boom-button').css('display', 'inline-block');
        }
    }
}


function handleKeypressLeft() {
    if (ka.state.currentChoice == 'left') return;

    ka.state.currentDriveIndex = 0;

    if (ka.state.currentChoice === null) {
        ka.state.initialChoiceMade = true;

        $('#boom-choice-right, #boom-choice-splitter').velocity('fadeOut', {display: null, duration: 360});
        $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: 360, complete: function (elements) {
            $('#boom-button-selection-floater').css('opacity', 1);
        }});
    } else {
        $('#boom-button-start-floater').velocity({opacity: 0, backgroundColorGreen: 0, backgroundColorBlue: 0}, {duration: 720});

        $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: 360, easing: 'ease-in'});
        $('#boom-choice-left, #boom-choice-splitter').velocity('fadeIn', {display: null, duration: 360});
        $('#boom-choice-right').velocity('fadeOut', {display: null, duration: 360, complete: function (elements) {
            $('#boom-choice-splitter').velocity('fadeOut', {display: null, duration: 360});
            $("#boom-split-choices").velocity({marginLeft: '+=420'}, {duration: 360, easing: 'ease-out', complete: function () {
                $('#boom-button-selection-floater').css('opacity', 1);
            }});
        }});

        /* if (ka.state.hasDrivesSelected) {
            $('#boom-choice-confirm .boom-button').velocity('fadeIn', {display: 'inline-block', duration: 360});
        } else {

        } */
    }

    ka.state.currentChoice = 'left';
}


function handleKeypressRight() {
    if (ka.state.currentChoice == 'right') return;

    if (ka.state.currentChoice === null) {
        ka.state.initialChoiceMade = true;

        $('#boom-button-start-floater').velocity({opacity: 1, backgroundColorGreen: 116, backgroundColorBlue: 217}, {duration: 360});

        $('#boom-choice-left, #boom-choice-splitter').velocity('fadeOut', {display: null, duration: 360});
        $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: 360});
        $('#boom-choice-confirm .boom-button').velocity('fadeIn', {display: 'inline-block', duration: 360});
    } else {
        $('#boom-button-selection-floater').css('opacity', 0);
        $('#boom-button-start-floater').velocity({opacity: 1, backgroundColorGreen: 116, backgroundColorBlue: 217}, {duration: 720});

        $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: 360, easing: 'ease-in'});
        $('#boom-choice-right, #boom-choice-splitter').velocity('fadeIn', {display: null, duration: 360});
        $('#boom-choice-left').velocity('fadeOut', {display: null, duration: 360, complete: function (elements) {
            $('#boom-choice-splitter').velocity('fadeOut', {display: null, duration: 360});
            $("#boom-split-choices").velocity({marginLeft: '-=420'}, {duration: 360, easing: 'ease-out'});
        }});
    }

    ka.state.currentChoice = 'right';
}


function handleKeypressSelect() {
    if (ka.state.currentChoice === null) {
        demandInitialChoice();
    } else if (ka.state.currentChoice == 'left') {
        var checkbox = $('#boom-drives-list li').eq(ka.state.currentDriveIndex).find('i');
        if (checkbox.hasClass('fa-square')) {
            checkbox.removeClass('fa-square').addClass('fa-check-square');
        } else {
            checkbox.removeClass('fa-check-square').addClass('fa-square');
        }

        var previouslySelected = ka.state.hasDrivesSelected;
        ka.state.hasDrivesSelected = $('#boom-drives-list li .fa-check-square').size() > 0;
        if (ka.state.hasDrivesSelected && !previouslySelected) {
            $('#boom-choice-confirm .boom-button').velocity('fadeIn', {display: 'inline-block', duration: 360});
        } else if (!ka.state.hasDrivesSelected && previouslySelected) {
            $('#boom-choice-confirm .boom-button').velocity('fadeOut', {display: 'none', duration: 360});
        }
    }
}


function handleKeypressQuit() {

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

    // document.body.addEventListener('keypress', ka.lib.handleKeypressLetter);
}


/* Prevent all input events. */
document.oncontextmenu = document.onmousedown = function (event) { event.preventDefault(); };


$(document).ready(function () {


    /* ... */
    registerHotkeys();

    $.ajax({
        url: '/movies/top250',
        success: function (list) {
            for (var index = 0; index < 10; index++) {
                $('<li>', {
                    text: list[index][0] + ' (' + list[index][1] + ')'
                }).appendTo('#boom-top250-list');
            }
        }
    });

    $.ajax({
        url: '/drives/mounted',
        success: function (list) {
            ka.data.drives = list.concat();

            for (var index = 0; index < list.length; index++) {
                $('<li>', {
                    html: '<i class="fa fa-square"></i>' + list[index][1] + ' (' + list[index][0] + ':)'
                }).appendTo('#boom-drives-list');
            }
        }
    });
});