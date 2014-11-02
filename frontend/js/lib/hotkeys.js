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

; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.handleKeypressAny = function (evt) {
    if (ka.state.view != 'grid') {
        return;
    } else {
        var character = String.fromCharCode(evt.keyCode);

        if (/^[a-z]$/i.test(character)) {
            var key = character.toUpperCase();
            if (key in ka.state.gridLookupLinesByKey) {
                var line = ka.state.gridLookupLinesByKey[key][0] % ka.settings.gridMaxRows;
                ka.state.gridPage = Math.floor(ka.state.gridLookupLinesByKey[key][0] / ka.settings.gridMaxRows);
                ka.state.gridFocusX = 0;
                ka.state.gridFocusY = line;

                ka.lib.repositionGrid();

                $('#boom-movie-grid-key-' + key).velocity({
                    color: '#000000'
                  , backgroundColor: '#ffffff'
                  , borderColor: '#ffffff'
                }, ka.settings.durationNormal).velocity('reverse');
            } else {
                $('#boom-movie-grid-container').velocity('callout.shake');
            }
        } else if (/^[1-7]$/.test(character)) {
            ka.lib.moveFocusToIndex(character - 1);
        }
    }
};


ka.lib.handleKeypressFirstItem = function () {
    if (ka.state.view == 'grid') {
        ka.lib.moveFocusFirstItem();
    }
};


ka.lib.handleKeypressLastItem = function () {
    if (ka.state.view == 'grid') {
        ka.lib.moveFocusLastItem();
    }
};


ka.lib.handleKeypressPreviousPage = function () {
    if (ka.state.view == 'grid') {
        ka.lib.moveFocusPageUp();
    }
};


ka.lib.handleKeypressNextPage = function () {
    if (ka.state.view == 'grid') {
        ka.lib.moveFocusPageDown();
    }
};


ka.lib.handleKeypressUp = function () {
    if (ka.state.view == 'config') {
        if (ka.state.currentConfigButton > 0) {
            ka.state.currentConfigButton -= 1;
            ka.lib.updateMenuButtonSelection();
        }
    } else if (ka.state.view == 'detail') {
        ka.lib.browser.expandUp();
    } else if (ka.state.view == 'grid') {
        ka.lib.moveFocusUp();
    } else if (ka.state.view == 'grid-compilation') {
        ka.lib.moveCompilationFocusUp();
    } else if (ka.state.view == 'select-stream') {
        ka.lib.moveStreamSelectionUp();
    }
};


ka.lib.handleKeypressDown = function () {
    if (ka.state.view == 'config') {
        if (ka.state.currentConfigButton + 1 < ka.state.maxConfigButton) {
            ka.state.currentConfigButton += 1;
            ka.lib.updateMenuButtonSelection();
        }
    } else if (ka.state.view == 'detail') {
        ka.lib.browser.contractDown();
    } else if (ka.state.view == 'grid') {
        ka.lib.moveFocusDown();
    } else if (ka.state.view == 'grid-compilation') {
        ka.lib.moveCompilationFocusDown();
    } else if (ka.state.view == 'select-stream') {
        ka.lib.moveStreamSelectionDown();
    }
};


ka.lib.handleKeypressLeft = function () {
    if (ka.state.view == 'grid') {
        ka.lib.moveFocusLeft();
    } else if (ka.state.view == 'grid-compilation') {
        ka.lib.moveCompilationFocusLeft();
    } else if (ka.state.view == 'detail') {
        ka.lib.moveDetailBrowserLeft();
    }
};


ka.lib.handleKeypressRight = function () {
    if (ka.state.view == 'grid') {
        ka.lib.moveFocusRight();
    } else if (ka.state.view == 'grid-compilation') {
        ka.lib.moveCompilationFocusRight();
    } /* else if (ka.state.view == 'config') {
        ka.transition.menu.to.grid();
    } */ else if (ka.state.view == 'detail') {
        ka.lib.moveDetailBrowserRight();
    }
};


ka.lib.handleKeypressToggle = function () {
    if (ka.state.view == 'grid') {
        ka.lib.toggleGridFocus();
    } else if (ka.state.view == 'grid-compilation') {
        ka.lib.toggleCompilationFocus();
    } else if (ka.state.view == 'detail') {
        ka.lib.browser.toggle();
    }
};


ka.lib.handleKeypressSelect = function () {
    if (ka.state.view == 'config') {
        ka.lib.executeMenuSelection();
    } else if (ka.state.view == 'grid') {
        if (ka.lib.grid.focus.isPositionValid()) {
            if (ka.lib.isCompilationAtFocus()) {
                ka.transition.grid.to.compilation();
            } else {
                ka.transition.grid.to.detail(ka.lib.getVariantFromGridFocus(), false);
            }
        }
    } else if (ka.state.view == 'grid-compilation') {
        ka.transition.grid.to.detail(ka.lib.getVariantFromGridFocus()[ka.state.currentCompilationFocusIndex], true);
    } else if (ka.state.view == 'detail') {
        ka.lib.toggleAvailableStreams();
    } else if (ka.state.view == 'select-stream') {
        var selected = $('#boom-detail-available-streams .boom-active'),
            actionType = selected.data('boom.type');
        if (actionType == 'stream') {
            $('#boom-movie-detail').velocity('fadeOut', {duration: ka.settings.durationNormal, complete: function () {
                ka.state.view = 'play:movie';

                if (!ka.state.isPlayerUpdated) {
                    $('#boom-playback-wait').velocity('fadeIn', {display: 'flex', duration: ka.settings.durationNormal, complete: function () {
                        ka.state.socketDispatcher.push('movie:play', selected.data('boom.stream'));
                    }});
                } else {
                    ka.state.socketDispatcher.push('movie:play', selected.data('boom.stream'));
                }
            }});
        } else if (actionType == 'trailer') {
            $('#boom-movie-detail').velocity('fadeOut', {duration: ka.settings.durationNormal, complete: function () {
                ka.state.view = 'play:trailer';

                ka.lib.startTrailerPlayer(ka.data.byId[$('#boom-movie-detail').data('boom.id')].trailer);
            }});
        }
    }
};


ka.lib.handleKeypressBack = function () {
    if (ka.state.view == 'config') {
        ka.transition.menu.to.grid();
    } else if (ka.state.view == 'detail') {
        ka.transition.detail.to.grid();
    } else if (ka.state.view == 'select-stream') {
        ka.lib.toggleAvailableStreams();
    } else if (ka.state.view == 'grid-compilation') {
        ka.transition.compilation.to.grid();
    } else if (ka.state.view == 'grid') {
        ka.transition.grid.to.menu();
    } else if (ka.state.view == 'play:trailer') {
        ka.lib.closeTrailerPlayer();
    } else if (ka.state.view == 'credits') {
        ka.state.licenseTextIndex = -1;
        $('#boom-credit-text').stop();
    }
};
