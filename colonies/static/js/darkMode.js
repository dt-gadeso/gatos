// Modo oscuro común para todas las páginas
class DarkModeManager {
    constructor() {
        this.darkModeKey = 'darkMode';
        this.init();
    }

    init() {
        // Crear el botón si no existe
        this.createToggleButton();
        
        // Aplicar el estado guardado
        this.applyStoredState();
        
        // Escuchar el evento de cambio
        this.attachEventListeners();
    }

    createToggleButton() {
        // Solo crear si no existe ya
        if (!document.getElementById('darkModeToggle')) {
            const button = document.createElement('button');
            button.id = 'darkModeToggle';
            button.innerHTML = '🌙';
            button.title = 'Cambiar modo oscuro/claro';
            button.setAttribute('aria-label', 'Toggle dark mode');
            
            // Agregar al footer si existe, sino al body
            const footer = document.querySelector('footer');
            if (footer) {
                footer.appendChild(button);
            } else {
                document.body.appendChild(button);
            }
        }
    }

    attachEventListeners() {
        const button = document.getElementById('darkModeToggle');
        if (button) {
            button.addEventListener('click', () => this.toggle());
        }

        // Escuchar cambios en localStorage desde otras pestañas
        window.addEventListener('storage', (e) => {
            if (e.key === this.darkModeKey) {
                this.applyStoredState();
            }
        });
    }

    toggle() {
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        if (isLight) {
            this.enable();
        } else {
            this.disable();
        }
    }

    enable() {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem(this.darkModeKey, 'true');
        this.updateButtonIcon(true);
        
        // Disparar evento personalizado
        this.dispatchChangeEvent(true);
    }

    disable() {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem(this.darkModeKey, 'false');
        this.updateButtonIcon(false);
        
        // Disparar evento personalizado
        this.dispatchChangeEvent(false);
    }

    applyStoredState() {
        const isDark = localStorage.getItem(this.darkModeKey) === 'true';
        
        if (isDark) {
            document.documentElement.removeAttribute('data-theme');
            this.updateButtonIcon(true);
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            this.updateButtonIcon(false);
        }
    }

    updateButtonIcon(isDark) {
        const button = document.getElementById('darkModeToggle');
        if (button) {
            button.innerHTML = isDark ? '☀️' : '🌙';
            button.title = isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro';
        }
    }

    dispatchChangeEvent(isDark) {
        const event = new CustomEvent('darkModeChange', {
            detail: { isDark }
        });
        document.dispatchEvent(event);
    }

    // Método público para obtener el estado actual
    isDarkMode() {
        return document.documentElement.getAttribute('data-theme') === 'dark';
    }

    // Método para detectar preferencia del sistema
    detectSystemPreference() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return true;
        }
        return false;
    }

    // Inicializar con preferencia del sistema si no hay configuración guardada
    initWithSystemPreference() {
        const stored = localStorage.getItem(this.darkModeKey);
        if (stored === null) {
            const systemPrefersDark = this.detectSystemPreference();
            if (systemPrefersDark) {
                this.enable();
            } else {
                this.disable();
            }
        }
    }
}

// Función para inicializar el modo oscuro
function initDarkMode() {
    // Esperar a que el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.darkModeManager = new DarkModeManager();
            window.darkModeManager.initWithSystemPreference();
        });
    } else {
        window.darkModeManager = new DarkModeManager();
        window.darkModeManager.initWithSystemPreference();
    }
}

// Auto-inicializar
initDarkMode();

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DarkModeManager;
}
