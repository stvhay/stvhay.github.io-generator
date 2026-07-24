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
    var themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) {
        themeColor.setAttribute("content", THEME_COLORS[effective]);
    }
})();
