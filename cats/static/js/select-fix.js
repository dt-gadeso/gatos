// Función para eliminar triángulos duplicados en campos de selección
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los elementos select
    const selectElements = document.querySelectorAll('select, .form-select');
    
    selectElements.forEach(function(select) {
        // Asegurar que no aparezcan los estilos nativos
        select.style.appearance = 'none';
        select.style.webkitAppearance = 'none';
        select.style.mozAppearance = 'none';
        
        // Para Internet Explorer/Edge
        select.style.msFilter = 'none';
        
        // Asegurar que solo haya una flecha personalizada
        const computedStyle = window.getComputedStyle(select);
        if (computedStyle.backgroundImage && computedStyle.backgroundImage !== 'none') {
            // Ya tiene una imagen de fondo personalizada
            select.style.backgroundRepeat = 'no-repeat';
            select.style.backgroundPosition = 'right 16px center';
            select.style.backgroundSize = '12px';
        }
    });
    
    // Función para manejar cambios dinámicos
    function handleSelectChanges() {
        const newSelects = document.querySelectorAll('select:not([data-processed]), .form-select:not([data-processed])');
        newSelects.forEach(function(select) {
            select.setAttribute('data-processed', 'true');
            select.style.appearance = 'none';
            select.style.webkitAppearance = 'none';
            select.style.mozAppearance = 'none';
            select.style.msFilter = 'none';
        });
    }
    
    // Observar cambios en el DOM
    const observer = new MutationObserver(handleSelectChanges);
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Marcar elementos procesados
    selectElements.forEach(function(select) {
        select.setAttribute('data-processed', 'true');
    });
});

// Función adicional para navegadores específicos
if (navigator.userAgent.indexOf('Edge') > -1 || navigator.userAgent.indexOf('Trident') > -1) {
    // Código específico para Edge/IE
    document.addEventListener('DOMContentLoaded', function() {
        const style = document.createElement('style');
        style.textContent = `
            select::-ms-expand,
            .form-select::-ms-expand {
                display: none !important;
            }
        `;
        document.head.appendChild(style);
    });
}
