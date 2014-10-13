/**
 *  ...
 *
 *  @author Nikola Klaric (nikola@klaric.org)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};

ka.lib.setupCollator = function () {
    ka.state.collator = new Intl.Collator(
        ['en-US', 'de-DE', 'fr-FR', 'es-ES', 'it-IT']
      , {
            usage: 'sort'
          , sensitivity: 'base'
          , ignorePunctuation: true
          , numeric: true
          , caseFirst: 'lower'
        }
    );
};
