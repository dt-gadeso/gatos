// // Función para eliminar triángulos duplicados en campos de selección
// document.addEventListener('DOMContentLoaded', function() {
//     // Seleccionar todos los elementos select
//     const selectElements = document.querySelectorAll('select, .form-select');
    
//     selectElements.forEach(function(select) {
//         // Asegurar que no aparezcan los estilos nativos
//         select.style.appearance = 'none';
//         select.style.webkitAppearance = 'none';
//         select.style.mozAppearance = 'none';
        
//         // Para Internet Explorer/Edge
//         select.style.msFilter = 'none';
        
//         // Asegurar que solo haya una flecha personalizada
//         const computedStyle = window.getComputedStyle(select);
//         if (computedStyle.backgroundImage && computedStyle.backgroundImage !== 'none') {
//             // Ya tiene una imagen de fondo personalizada
//             select.style.backgroundRepeat = 'no-repeat';
//             select.style.backgroundPosition = 'right 16px center';
//             select.style.backgroundSize = '12px';
//         }
//     });
    
//     // Función para manejar cambios dinámicos
//     function handleSelectChanges() {
//         const newSelects = document.querySelectorAll('select:not([data-processed]), .form-select:not([data-processed])');
//         newSelects.forEach(function(select) {
//             select.setAttribute('data-processed', 'true');
//             select.style.appearance = 'none';
//             select.style.webkitAppearance = 'none';
//             select.style.mozAppearance = 'none';
//             select.style.msFilter = 'none';
//         });
//     }
    
//     // Observar cambios en el DOM
//     const observer = new MutationObserver(handleSelectChanges);
//     observer.observe(document.body, {
//         childList: true,
//         subtree: true
//     });
    
//     // Marcar elementos procesados
//     selectElements.forEach(function(select) {
//         select.setAttribute('data-processed', 'true');
//     });
// });

// // Función adicional para navegadores específicos
// if (navigator.userAgent.indexOf('Edge') > -1 || navigator.userAgent.indexOf('Trident') > -1) {
//     // Código específico para Edge/IE
//     document.addEventListener('DOMContentLoaded', function() {
//         const style = document.createElement('style');
//         style.textContent = `
//             select::-ms-expand,
//             .form-select::-ms-expand {
//                 display: none !important;
//             }
//         `;
//         document.head.appendChild(style);
//     });
// }

document.addEventListener('DOMContentLoaded', function () {
    const selects = document.querySelectorAll('select, .form-select');

    function styleSelect(select) {
        // Evita reprocesar
        if (select.dataset.processed === 'true') return;
        select.dataset.processed = 'true';

        // Oculta la flecha nativa
        select.style.appearance = 'none';
        select.style.webkitAppearance = 'none';
        select.style.mozAppearance = 'none';
        select.style.msFilter = 'none';

        // Estilos base
        select.style.width = '100%';
        select.style.minHeight = select.multiple ? '120px' : '56px';
        select.style.padding = select.multiple ? '16px 20px' : '16px 50px 16px 20px';
        select.style.border = '2px solid #e9ecef';
        select.style.borderRadius = '12px';
        select.style.fontSize = '15px';
        select.style.fontFamily = 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif';
        select.style.cursor = 'pointer';
        select.style.outline = 'none';
        select.style.boxSizing = 'border-box';
        select.style.backgroundRepeat = 'no-repeat';
        select.style.backgroundPosition = 'right 16px center';
        select.style.backgroundSize = '12px';
        select.style.zIndex = '1';

        // Aplica imagen de flecha personalizada si no es múltiple
        if (!select.multiple) {
            select.style.backgroundImage =
                "url(\"data:image/svg+xml;charset=utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='%23333' d='M6 9L1.5 4.5h9z'/></svg>\")";
        } else {
            select.style.backgroundImage = 'none';
            select.style.overflowY = 'auto';
            select.style.resize = 'vertical';
        }

        // Eventos de foco
        select.addEventListener('focus', function () {
            this.style.borderColor = '#d2691e';
            this.style.boxShadow = '0 0 0 4px rgba(210, 105, 30, 0.15)';
            this.style.transform = 'translateY(-1px)';
        });

        select.addEventListener('blur', function () {
            this.style.borderColor = '#e9ecef';
            this.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
            this.style.transform = 'translateY(0)';
        });

        // Estilos de opciones (limitado, ya que muchos navegadores no permiten personalizar <option>)
        const options = select.querySelectorAll('option');
        options.forEach(function (option) {
            option.style.fontSize = '15px';
            option.style.color = '#333';
            option.style.padding = '10px 15px';
        });
    }

    // Aplica estilos iniciales
    selects.forEach(styleSelect);

    // Observa cambios en el DOM (si se insertan nuevos selectores dinámicamente)
    const observer = new MutationObserver(function () {
        const newSelects = document.querySelectorAll('select:not([data-processed]), .form-select:not([data-processed])');
        newSelects.forEach(styleSelect);
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Modo oscuro
    function updateSelectorsForDarkMode() {
        const isDarkMode = document.body.classList.contains('dark-mode');
        document.querySelectorAll('select[data-processed="true"]').forEach(function (select) {
            if (!select.multiple) {
                const arrowColor = isDarkMode ? '%23f1f1f1' : '%23333';
                select.style.backgroundImage =
                    `url("data:image/svg+xml;charset=utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='${arrowColor}' d='M6 9L1.5 4.5h9z'/></svg>")`;
            }
            select.style.backgroundColor = isDarkMode ? '#333' : 'white';
            select.style.color = isDarkMode ? '#f1f1f1' : '#333';
            select.style.borderColor = isDarkMode ? '#555' : '#e9ecef';

            const options = select.querySelectorAll('option');
            options.forEach(function (option) {
                option.style.backgroundColor = isDarkMode ? '#333' : 'white';
                option.style.color = isDarkMode ? '#f1f1f1' : '#333';
            });
        });
    }

    updateSelectorsForDarkMode();

    // Cambios en modo oscuro por toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => setTimeout(updateSelectorsForDarkMode, 100));
    }

    // Observar cambios de clase (modo oscuro dinámico)
    new MutationObserver(() => updateSelectorsForDarkMode()).observe(document.body, {
        attributes: true,
        attributeFilter: ['class']
    });

    // IE/Edge: Ocultar flecha antigua
    if (navigator.userAgent.includes('Edge') || navigator.userAgent.includes('Trident')) {
        const style = document.createElement('style');
        style.textContent = `
            select::-ms-expand,
            .form-select::-ms-expand {
                display: none !important;
            }
        `;
        document.head.appendChild(style);
    }
});
