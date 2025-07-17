// JavaScript para mejorar la experiencia del usuario en el módulo veterinario

document.addEventListener('DOMContentLoaded', function() {
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
