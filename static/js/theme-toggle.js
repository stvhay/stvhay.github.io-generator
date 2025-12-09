/**
 * Theme Toggle - Allows users to switch between light and dark mode
 *
 * Behavior:
 * - If no override is set, follows system preference
 * - Button shows the opposite of the current effective theme
 * - Clicking switches to the opposite theme
 * - If the new theme matches system preference, clears the override
 * - If the new theme differs from system preference, saves the override
 */

(function () {
    "use strict";

    const STORAGE_KEY = "theme-preference";

    function getSystemTheme() {
        return window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark"
            : "light";
    }

    function getSavedTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY);
        } catch {
            return null;
        }
    }

    function saveTheme(theme) {
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch {
            // localStorage not available
        }
    }

    function clearSavedTheme() {
        try {
            localStorage.removeItem(STORAGE_KEY);
        } catch {
            // localStorage not available
        }
    }

    function getEffectiveTheme() {
        return getSavedTheme() || getSystemTheme();
    }

    function applyTheme(theme) {
        if (theme) {
            document.documentElement.setAttribute("data-theme", theme);
        } else {
            document.documentElement.removeAttribute("data-theme");
        }
    }

    function updateButtonText(button) {
        const effective = getEffectiveTheme();
        const opposite = effective === "dark" ? "Light" : "Dark";
        button.textContent = opposite + " mode";
        button.setAttribute(
            "aria-label",
            "Switch to " + opposite.toLowerCase() + " mode"
        );
    }

    function toggleTheme(button) {
        const system = getSystemTheme();
        const effective = getEffectiveTheme();
        const newTheme = effective === "dark" ? "light" : "dark";

        if (newTheme === system) {
            // Switching back to system preference - clear override
            clearSavedTheme();
            applyTheme(null);
        } else {
            // Switching away from system preference - save override
            saveTheme(newTheme);
            applyTheme(newTheme);
        }

        updateButtonText(button);
    }

    function initThemeToggle() {
        const button = document.getElementById("theme-toggle");
        if (!button) return;

        // Apply saved theme if exists
        const saved = getSavedTheme();
        if (saved) {
            applyTheme(saved);
        }

        // Set initial button text
        updateButtonText(button);

        // Handle click
        button.addEventListener("click", function () {
            toggleTheme(button);
        });

        // Update button text when system preference changes
        window
            .matchMedia("(prefers-color-scheme: dark)")
            .addEventListener("change", function () {
                // If no override, button text should update
                if (!getSavedTheme()) {
                    updateButtonText(button);
                }
            });
    }

    // Initialize when DOM is ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initThemeToggle);
    } else {
        initThemeToggle();
    }
})();
