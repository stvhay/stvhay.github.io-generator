/**
 * Theme initialization - runs before page render to prevent flash
 * This script should be loaded with blocking behavior in <head>
 */
(function () {
    "use strict";

    var THEME_COLORS = { light: "#f2efe9", dark: "#1f1f1f" };
    var saved = null;

    try {
        saved = localStorage.getItem("theme-preference");
        if (saved) {
            document.documentElement.setAttribute("data-theme", saved);
        }
    } catch (e) {
        // localStorage not available
    }

    var effective =
        saved ||
        (window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark"
            : "light");
    var themeColors = document.querySelectorAll('meta[name="theme-color"]');
    for (var i = 0; i < themeColors.length; i++) {
        themeColors[i].setAttribute("content", THEME_COLORS[effective]);
    }
})();
