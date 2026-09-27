(function () {
    const storageKey = 'taskflow-theme';
    const root = document.documentElement;
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');

    function savedTheme() {
        try {
            return localStorage.getItem(storageKey);
        } catch (error) {
            return null;
        }
    }

    function currentTheme() {
        const saved = savedTheme();
        if (saved === 'light' || saved === 'dark') {
            return saved;
        }
        return systemTheme.matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        const darkMode = theme === 'dark';
        root.setAttribute('data-theme', theme);
        root.style.colorScheme = theme;

        document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
            button.setAttribute('data-theme-state', theme);
            button.setAttribute('aria-label', darkMode ? 'Switch to day mode' : 'Switch to night mode');
            button.setAttribute('title', darkMode ? 'Switch to day mode' : 'Switch to night mode');

            const icon = button.querySelector('[data-theme-icon]');
            const text = button.querySelector('[data-theme-text]');

            if (icon && !icon.classList.contains('theme-switch-icon')) {
                icon.textContent = darkMode ? '☀' : '☾';
            }
            if (text) {
                text.textContent = darkMode ? 'Day' : 'Night';
            }
        });
    }

    applyTheme(currentTheme());

    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(currentTheme());

        document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
            button.addEventListener('click', function () {
                const nextTheme = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
                try {
                    localStorage.setItem(storageKey, nextTheme);
                } catch (error) {
                    // Keep the selected theme for this page even if storage is unavailable.
                }
                applyTheme(nextTheme);
            });
        });
    });

    systemTheme.addEventListener('change', function (event) {
        if (!savedTheme()) {
            applyTheme(event.matches ? 'dark' : 'light');
        }
    });
})();
