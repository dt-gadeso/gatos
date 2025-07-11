// Script mejorado para asegurar que los selectores se muestren correctamente
document.addEventListener('DOMContentLoaded', function() {
    // Encuentra todos los selectores en el formulario
    const selects = document.querySelectorAll('.search-form-container select');
    
    selects.forEach(function(select) {
        // Fuerza el estilo del selector
        select.style.display = 'block';
        select.style.visibility = 'visible';
        select.style.opacity = '1';
        select.style.position = 'relative';
        select.style.zIndex = '1';
        
        // Aplica estilos específicos para selectores
        select.style.width = '100%';
        select.style.minHeight = '56px';
        select.style.padding = '16px 50px 16px 20px';
        select.style.border = '2px solid #e9ecef';
        select.style.borderRadius = '12px';
        select.style.fontSize = '15px';
        select.style.fontFamily = 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif';
        select.style.cursor = 'pointer';
        select.style.outline = 'none';
        select.style.boxSizing = 'border-box';
        
        // Elimina apariencias por defecto
        select.style.webkitAppearance = 'none';
        select.style.mozAppearance = 'none';
        select.style.appearance = 'none';
        
        // Aplica fondo y flecha personalizada
        select.style.backgroundColor = 'white';
        select.style.color = '#333';
        select.style.backgroundImage = "url(\"data:image/svg+xml;charset=utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='%23333' d='M6 9L1.5 4.5h9z'/></svg>\")";
        select.style.backgroundRepeat = 'no-repeat';
        select.style.backgroundPosition = 'right 16px center';
        select.style.backgroundSize = '12px';
        
        // Añade eventos para mejorar la experiencia del usuario
        select.addEventListener('focus', function() {
            this.style.borderColor = '#d2691e';
            this.style.boxShadow = '0 0 0 4px rgba(210, 105, 30, 0.15)';
            this.style.transform = 'translateY(-1px)';
        });
        
        select.addEventListener('blur', function() {
            this.style.borderColor = '#e9ecef';
            this.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
            this.style.transform = 'translateY(0)';
        });
        
        // Maneja selectores múltiples
        if (select.multiple) {
            select.style.minHeight = '120px';
            select.style.paddingRight = '20px';
            select.style.backgroundImage = 'none';
            select.style.resize = 'vertical';
            select.style.overflowY = 'auto';
        }
        
        // Mejora las opciones del selector
        const options = select.querySelectorAll('option');
        options.forEach(function(option) {
            option.style.padding = '10px 15px';
            option.style.fontSize = '15px';
            option.style.lineHeight = '1.5';
            option.style.backgroundColor = 'white';
            option.style.color = '#333';
            option.style.border = 'none';
        });
    });
    
    // Función para aplicar modo oscuro a selectores
    function updateSelectorsForDarkMode() {
        const isDarkMode = document.body.classList.contains('dark-mode');
        
        selects.forEach(function(select) {
            if (isDarkMode) {
                select.style.backgroundColor = '#333';
                select.style.color = '#f1f1f1';
                select.style.borderColor = '#555';
                select.style.backgroundImage = "url(\"data:image/svg+xml;charset=utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='%23f1f1f1' d='M6 9L1.5 4.5h9z'/></svg>\")";
                
                // Actualiza las opciones para modo oscuro
                const options = select.querySelectorAll('option');
                options.forEach(function(option) {
                    option.style.backgroundColor = '#333';
                    option.style.color = '#f1f1f1';
                });
            } else {
                select.style.backgroundColor = 'white';
                select.style.color = '#333';
                select.style.borderColor = '#e9ecef';
                select.style.backgroundImage = "url(\"data:image/svg+xml;charset=utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='%23333' d='M6 9L1.5 4.5h9z'/></svg>\")";
                
                // Actualiza las opciones para modo claro
                const options = select.querySelectorAll('option');
                options.forEach(function(option) {
                    option.style.backgroundColor = 'white';
                    option.style.color = '#333';
                });
            }
        });
    }
    
    // Ejecuta la función al cargar
    updateSelectorsForDarkMode();
    
    // Escucha cambios en el modo oscuro
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            setTimeout(updateSelectorsForDarkMode, 100);
        });
    }
    
    // Observa cambios en las clases del body para detectar modo oscuro
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                updateSelectorsForDarkMode();
            }
        });
    });
    
    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ['class']
    });
    
    // Corrección adicional para selectores específicos
    const specificSelectors = [
        'select[name="sex"]',
        'select[name="sterilized"]', 
        'select[name="colony"]',
        'select[name="dead"]'
    ];
    
    specificSelectors.forEach(function(selector) {
        const element = document.querySelector(selector);
        if (element) {
            // Fuerza la visibilidad del selector
            element.style.display = 'block';
            element.style.visibility = 'visible';
            element.style.opacity = '1';
            element.style.position = 'relative';
            element.style.zIndex = '10';
            
            // Corrección específica para problemas de renderizado
            setTimeout(function() {
                element.style.transform = 'translateZ(0)';
            }, 100);
        }
    });
});
