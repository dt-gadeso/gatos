document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('darkModeToggle');
    if (!btn) return;

    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'on') {
        document.body.classList.add('dark-mode');
        btn.textContent = 'Modo claro';
    } else {
        document.body.classList.remove('dark-mode');
        btn.textContent = 'Modo oscuro';
    }

    btn.addEventListener('click', function() {
        const isDark = document.body.classList.toggle('dark-mode');
        if (isDark) {
            btn.textContent = 'Modo claro';
            localStorage.setItem('darkMode', 'on');
        } else {
            btn.textContent = 'Modo oscuro';
            localStorage.setItem('darkMode', 'off');
        }
    });
});
