/**
 *  Application loop.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */

; var ka = ka || {}; if (!('data' in ka)) ka.data = {};

ka.data.cortex = {
    all: new Cortex([])
  , byYear: new Cortex({})
  , byUuid: new Cortex({})
  , byLetter: new Cortex({})
};
ka.data.cortex.all.on('update', ka.lib.renderMovieThumbnail);

function boot() {
    $.ajax({
        url: '/movies/all',
        success: function (list) {
            var index = list.length;
            while (index--) {
                ka.lib.addMovie(list[index]);
            }

            // ka.data.cortex.all.forEach(function (item, index) { console.log(item.titleOriginal.getValue(), '->', item.titleSortable.getValue())})
        }
    });

    var dispatcher = new ka.lib.WebSocketDispatcher('wss://127.0.0.1:' + WEBSOCKET_PORT + '/');
    dispatcher.bind('receive:movie:item', function (record) {
        /* $('<div>', {
            'text': record
        }).appendTo('body'); */
        // console.log(record)
        // http://image.tmdb.org/t/p/original/9gZZyQ8XStpUJBFU1ceU4xx1crv.jpg
        // http://image.tmdb.org/t/p/w130/qKkFk9HELmABpcPoc1HHZGIxQ5a.jpg
        $('<img>', {
            'src': 'https://127.0.0.1:' + HTTP_PORT + '/movie/poster/' + record + '.jpg/150' // record.replace('http:', 'https:').replace('/original/', '/w150/')
          , 'width': 150
        }).appendTo('body');
    });
}

/* document.oncontextmenu = function (evt) {
    evt.preventDefault();
}; */

document.addEventListener('DOMContentLoaded', function(event) {
    /* Notify backend that UI is ready. */
    $.ajax({url: BOOT_TOKEN, type: 'PATCH', success: boot});

    $('#content').onepage_scroll({
   sectionContainer: "section",     // sectionContainer accepts any kind of selector in case you don't want to use section
   easing: "ease",                  // Easing options accepts the CSS3 easing animation such "ease", "linear", "ease-in",
                                    // "ease-out", "ease-in-out", or even cubic bezier value such as "cubic-bezier(0.175, 0.885, 0.420, 1.310)"
   animationTime: 1000,             // AnimationTime let you define how long each section takes to animate
   pagination: false,                // You can either show or hide the pagination. Toggle true for show, false for hide.
   updateURL: false,                // Toggle this true if you want the URL to be updated automatically when the user scroll to each page.
   // beforeMove: function(index) {},  // This option accepts a callback function. The function will be called before the page moves.
   // afterMove: function(index) {},   // This option accepts a callback function. The function will be called after the page moves.
   loop: false,                     // You can have the page loop back to the top/bottom when the user navigates at up/down on the first/last page.
   keyboard: true,                  // You can activate the keyboard controls
   responsiveFallback: false        // You can fallback to normal page scroll by defining the width of the browser in which
                                    // you want the responsive fallback to be triggered. For example, set this to 600 and whenever
                                    // the browser's width is less than 600, the fallback will kick in.
});

    /*
    setTimeout(function () {
        // todo: websocket.close()
        // https://developer.mozilla.org/en-US/docs/WebSockets/Writing_WebSocket_client_applications
        bridge.shutdown();
    }, 3000);
    */


    /*
    setTimeout(function () {
        $('#app-logo').animate({opacity: 0}, 500, 'linear');
        $('#app-info').animate({opacity: 0}, 500, 'linear');
        $('.spinner').animate({borderRadius: 0, padding: 0, width: '100%', height: '100%'}, 1000, 'linear');
        $('.spinner div').animate({marginLeft: 256, marginRight: 256, opacity: 0}, 1000, 'linear');
        $('.spinner .container').animate({marginTop: 512, opacity: 0}, 1000, 'linear', function () {

        });
    }, 3000); */
});
