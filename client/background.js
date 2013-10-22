/*
 *  Copyright (c) 2013 Nikola Klaric
 */

/**
 *  Normal launch initiated by the user, let's start clean.
 *  Note that this is not related to the persistent state, which is
 *  appropriately handled in the window code.
 */
chrome.app.runtime.onLaunched.addListener(function () {
	runApp(false);
});


/**
 *	If restarted, try to get the transient saved state.
 */
chrome.app.runtime.onRestarted.addListener(function () {
 	runApp(true);
});


/**
 *
 */
function runApp(readInitialState) {
	chrome.app.window.create("index.html", {
		id: 'application', 
		frame: "none", 
		state: "fullscreen", 
		resizable: true,
		bounds: {width: 500, height: 309} 
	},
	/**
	 *	When the callback is executed, the DOM is loaded but no script was
	 * 	loaded yet. So, let's attach to the load event.
	 */
	function (win) {
		win.contentWindow.addEventListener("load", function() {		
			if (readInitialState) {
		  		win.contentWindow.setInitialState();
			} else {
		  		win.contentWindow.clearInitialState();
			}
	  	});
	});
}
