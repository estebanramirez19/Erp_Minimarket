// ===========================
// GESTOR DE TEMA (CLARO/OSCURO)
// ===========================

class ThemeManager {
    constructor() {
        this.STORAGE_KEY = 'erp-theme';
        this.DARK_THEME = 'dark';
        this.LIGHT_THEME = 'light';
        this.init();
    }

    init() {
        // Detectar preferencia guardada o preferencia del sistema
        const savedTheme = localStorage.getItem(this.STORAGE_KEY);
        const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? this.DARK_THEME : this.LIGHT_THEME;
        const theme = savedTheme || systemPreference;
        
        this.setTheme(theme);
        this.setupListeners();
    }

    setTheme(theme) {
        const html = document.documentElement;
        
        if (theme === this.DARK_THEME) {
            html.setAttribute('data-theme', 'dark');
            localStorage.setItem(this.STORAGE_KEY, this.DARK_THEME);
            this.updateToggleButton(true);
        } else {
            html.removeAttribute('data-theme');
            localStorage.setItem(this.STORAGE_KEY, this.LIGHT_THEME);
            this.updateToggleButton(false);
        }
    }

    getCurrentTheme() {
        return localStorage.getItem(this.STORAGE_KEY) || this.LIGHT_THEME;
    }

    toggleTheme() {
        const currentTheme = this.getCurrentTheme();
        const newTheme = currentTheme === this.DARK_THEME ? this.LIGHT_THEME : this.DARK_THEME;
        this.setTheme(newTheme);
    }

    updateToggleButton(isDark) {
        const button = document.getElementById('theme-toggle-btn');
        if (button) {
            button.innerHTML = isDark 
                ? '<i class="bi bi-sun"></i>' 
                : '<i class="bi bi-moon"></i>';
            button.setAttribute('aria-label', isDark ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
        }
    }

    setupListeners() {
        const button = document.getElementById('theme-toggle-btn');
        if (button) {
            button.addEventListener('click', () => this.toggleTheme());
        }

        // Escuchar cambios de preferencia del sistema
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem(this.STORAGE_KEY)) {
                this.setTheme(e.matches ? this.DARK_THEME : this.LIGHT_THEME);
            }
        });
    }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new ThemeManager());
} else {
    new ThemeManager();
}
