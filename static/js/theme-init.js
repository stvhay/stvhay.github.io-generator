/**
 * Theme initialization - runs before page render to prevent flash
 * This script should be loaded with blocking behavior in <head>
 */
(function () {
    "use strict";
    try {
        var saved = localStorage.getItem("theme-preference");
        if (saved) {
            document.documentElement.setAttribute("data-theme", saved);
        }
    } catch (e) {
        // localStorage not available
    }
})();
