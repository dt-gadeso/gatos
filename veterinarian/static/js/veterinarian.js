// JavaScript para mejorar la experiencia del usuario en el módulo veterinario

document.addEventListener('DOMContentLoaded', function() {
    // Función para aplicar estilos adicionales de modo oscuro a elementos específicos
    function applyDarkModeStyles() {
        const isDarkMode = document.body.classList.contains('dark-mode');
        const veterinarianContainer = document.querySelector('.veterinarian-container');
        
        if (!veterinarianContainer) return;
        
        // Aplicar estilos específicos para modo oscuro a contenedores
        const sections = document.querySelectorAll('section');
        const formContainers = document.querySelectorAll('.search-form-container, .form-container');
        const cards = document.querySelectorAll('.vet-search-card');
        const inputs = document.querySelectorAll('input, select, textarea');
        
        if (isDarkMode) {
            // Contenedor principal
            veterinarianContainer.style.background = 'linear-gradient(135deg, #1c1c1c 0%, #252525 100%)';
            veterinarianContainer.style.boxShadow = '0 10px 40px rgba(0,0,0,0.5)';
            veterinarianContainer.style.border = '1px solid rgba(76, 175, 80, 0.1)';
            
            // Secciones
            sections.forEach(section => {
                section.style.background = 'linear-gradient(135deg, #1c1c1c 0%, #252525 100%)';
                section.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
                section.style.border = '1px solid rgba(76, 175, 80, 0.1)';
            });
            
            // Formularios
            formContainers.forEach(container => {
                container.style.background = '#252525';
                container.style.border = '1px solid #333333';
            });
            
            // Tarjetas
            cards.forEach(card => {
                card.style.background = '#252525';
                card.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
                card.style.border = '1px solid rgba(76, 175, 80, 0.1)';
            });
            
            // Inputs y selects
            inputs.forEach(input => {
                input.style.background = '#2c2c2c';
                input.style.color = '#f8f8f8';
                input.style.borderColor = '#3d3d3d';
            });
        } else {
            // Restaurar estilos en modo claro
            veterinarianContainer.style.background = '';
            veterinarianContainer.style.boxShadow = '';
            veterinarianContainer.style.border = '';
            
            sections.forEach(section => {
                section.style.background = '';
                section.style.boxShadow = '';
                section.style.border = '';
            });
            
            formContainers.forEach(container => {
                container.style.background = '';
                container.style.border = '';
            });
            
            cards.forEach(card => {
                card.style.background = '';
                card.style.boxShadow = '';
                card.style.border = '';
            });
            
            inputs.forEach(input => {
                input.style.background = '';
                input.style.color = '';
                input.style.borderColor = '';
            });
        }
    }
    
    // Aplicar estilos al cargar la página
    applyDarkModeStyles();
    
    // Escuchar cambios en el modo oscuro
    document.addEventListener('darkModeChange', function(e) {
        applyDarkModeStyles();
    });
    
    // También verificar periódicamente por cambios de clase en el body
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                applyDarkModeStyles();
            }
        });
    });
    
    observer.observe(document.body, { attributes: true });

    // Gestión de campos dinámicos en el formulario de visitas
    const catSurvivedSelect = document.getElementById('id_cat_survived');
    const returnedToColonySelect = document.getElementById('id_returned_to_colony');
    const housingTypeSelect = document.getElementById('id_housing_type');

    if (catSurvivedSelect && returnedToColonySelect && housingTypeSelect) {
        console.log('Campos encontrados:', { 
            catSurvived: catSurvivedSelect,
            returnedToColony: returnedToColonySelect,
            housingType: housingTypeSelect 
        });

        const housingAddressGroup = document.querySelector('[for="id_housing_address"]')?.parentElement;
        console.log('Campo de dirección:', housingAddressGroup);

        // Function to handle visibility of returned to colony field
        function handleCatSurvivedChange() {
            console.log('Cambió estado de supervivencia:', catSurvivedSelect.value);
            const returnedToColonyGroup = returnedToColonySelect.closest('.form-group');
            const housingTypeGroup = housingTypeSelect.closest('.form-group');
            
            console.log('Valor actual de cat_survived:', catSurvivedSelect.value);
            if (catSurvivedSelect.value === 'True' || catSurvivedSelect.value === 'true') {
                console.log('El gato sobrevivió, mostrando campos adicionales');
                if (returnedToColonyGroup) returnedToColonyGroup.style.display = 'block';
                handleReturnedToColonyChange();
            } else {
                console.log('El gato no sobrevivió, ocultando campos');
                if (returnedToColonyGroup) returnedToColonyGroup.style.display = 'none';
                if (housingTypeGroup) housingTypeGroup.style.display = 'none';
                if (housingAddressGroup) housingAddressGroup.style.display = 'none';
            }
        }

        // Function to handle visibility of housing fields
        function handleReturnedToColonyChange() {
            console.log('Valor actual de returned_to_colony:', returnedToColonySelect.value);
            const housingTypeGroup = housingTypeSelect.closest('.form-group');
            
            if (returnedToColonySelect.value === 'False' || returnedToColonySelect.value === 'false') {
                console.log('No volvió a la colonia, mostrando opciones de alojamiento');
                if (housingTypeGroup) housingTypeGroup.style.display = 'block';
                handleHousingTypeChange();
            } else {
                console.log('Volvió a la colonia, ocultando opciones de alojamiento');
                if (housingTypeGroup) housingTypeGroup.style.display = 'none';
                if (housingAddressGroup) housingAddressGroup.style.display = 'none';
            }
        }

        // Function to handle visibility of address field
        function handleHousingTypeChange() {
            console.log('Cambió tipo de alojamiento:', housingTypeSelect.value);
            if (housingTypeSelect.value !== 'none') {
                console.log('Mostrando campo de dirección');
                if (housingAddressGroup) housingAddressGroup.style.display = 'block';
            } else {
                console.log('Ocultando campo de dirección');
                if (housingAddressGroup) housingAddressGroup.style.display = 'none';
            }
        }

        // Add event listeners
        catSurvivedSelect.addEventListener('change', handleCatSurvivedChange);
        returnedToColonySelect.addEventListener('change', handleReturnedToColonyChange);
        housingTypeSelect.addEventListener('change', handleHousingTypeChange);

        // Initial setup
        handleCatSurvivedChange();
    }

    // Animación suave para los botones
    const buttons = document.querySelectorAll('.btn-primary, .map-btn, .btn-management');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // Validación en tiempo real para campos de email
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isValidEmail(this.value)) {
                this.style.borderColor = '#d32f2f';
                showFieldError(this, 'Por favor ingresa un email válido');
            } else {
                this.style.borderColor = 'var(--primary-color)';
                hideFieldError(this);
            }
        });
    });

    // Validación para campos requeridos
    const requiredInputs = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.style.borderColor = '#d32f2f';
                showFieldError(this, 'Este campo es requerido');
            } else {
                this.style.borderColor = 'var(--primary-color)';
                hideFieldError(this);
            }
        });
    });

    // Mejorar la experiencia del select
    const selects = document.querySelectorAll('select');
    selects.forEach(select => {
        select.addEventListener('change', function() {
            this.style.borderColor = 'var(--primary-color)';
            hideFieldError(this);
        });
    });

    // Auto-resize para textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Confirmación antes de cancelar formularios
    const cancelButtons = document.querySelectorAll('.btn-management');
    cancelButtons.forEach(button => {
        if (button.textContent.includes('Cancelar')) {
            button.addEventListener('click', function(e) {
                const form = document.querySelector('form');
                const hasData = checkFormHasData(form);
                
                if (hasData) {
                    e.preventDefault();
                    if (confirm('¿Estás seguro de que quieres cancelar? Se perderán los cambios no guardados.')) {
                        window.location.href = '/veterinarian/';
                    }
                }
            });
        }
    });

    // Animación para las cards de resultados
    const cards = document.querySelectorAll('.vet-search-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-card');
    });
});

// Función para validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Función para mostrar errores de campo
function showFieldError(field, message) {
    hideFieldError(field); // Remover error anterior
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message field-error';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

// Función para ocultar errores de campo
function hideFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// Función para verificar si el formulario tiene datos
function checkFormHasData(form) {
    const inputs = form.querySelectorAll('input, select, textarea');
    for (let input of inputs) {
        if (input.type === 'checkbox' || input.type === 'radio') {
            if (input.checked) return true;
        } else if (input.value.trim()) {
            return true;
        }
    }
    return false;
}

// Función para animar las cards
function animateCards() {
    const cards = document.querySelectorAll('.vet-search-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Función para mejorar la búsqueda
function enhanceSearch() {
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.innerHTML = '🔍 Buscando...';
            submitButton.disabled = true;
            
            // Simular delay para mejor UX
            setTimeout(() => {
                submitButton.innerHTML = '🔍 Buscar veterinario';
                submitButton.disabled = false;
            }, 2000);
        });
    }
}

// Llamar a la función de mejora de búsqueda
enhanceSearch();
