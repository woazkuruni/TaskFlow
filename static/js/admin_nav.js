(function () {
    document.addEventListener('DOMContentLoaded', function () {
        const button = document.querySelector('[data-admin-menu-button]');
        const drawer = document.querySelector('[data-admin-menu]');
        const backdrop = document.querySelector('[data-admin-menu-backdrop]');
        const closeButton = document.querySelector('[data-admin-menu-close]');

        if (!button || !drawer || !backdrop) {
            return;
        }

        function openMenu() {
            drawer.classList.add('is-open');
            backdrop.classList.add('is-open');
            document.body.classList.add('taskflow-menu-open');
            drawer.setAttribute('aria-hidden', 'false');
            button.setAttribute('aria-expanded', 'true');
        }

        function closeMenu() {
            drawer.classList.remove('is-open');
            backdrop.classList.remove('is-open');
            document.body.classList.remove('taskflow-menu-open');
            drawer.setAttribute('aria-hidden', 'true');
            button.setAttribute('aria-expanded', 'false');
        }

        button.addEventListener('click', function () {
            if (drawer.classList.contains('is-open')) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        backdrop.addEventListener('click', closeMenu);
        if (closeButton) {
            closeButton.addEventListener('click', closeMenu);
        }

        drawer.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', closeMenu);
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                closeMenu();
            }
        });

        window.addEventListener('resize', function () {
            if (window.innerWidth > 900) {
                closeMenu();
            }
        });
    });
})();
