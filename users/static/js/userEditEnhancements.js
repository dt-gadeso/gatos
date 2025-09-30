// Mejoras UX para el formulario de edición de usuarios
class UserEditEnhancements {
    constructor() {
        this.initializeEnhancements();
        this.setupFormValidation();
        this.setupInteractiveElements();
    }
    
    // Inicializar mejoras generales
    initializeEnhancements() {
        // Agregar efectos de loading
        this.addLoadingStates();
        
        // Mejorar la navegación
        this.enhanceNavigation();
        
        // Agregar confirmaciones inteligentes
        this.setupSmartConfirmations();
        
        // Mejorar tooltips
        this.enhanceTooltips();
    }
    
    // Configurar validación del formulario
    setupFormValidation() {
        const form = document.getElementById('editUserForm');
        if (!form) return;
        
        // Validación en tiempo real
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearValidationErrors(input));
        });
        
        // Validación especial para campos relacionados
        this.setupRelatedFieldValidation();
    }
    
    // Validar campo individual
    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';
        
        // Limpiar errores previos
        this.clearValidationErrors(field);
        
        switch (fieldName) {
            case 'username':
                if (value.length < 3) {
                    isValid = false;
                    errorMessage = 'El nombre de usuario debe tener al menos 3 caracteres';
                } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
                    isValid = false;
                    errorMessage = 'El nombre de usuario solo puede contener letras, números y guiones bajos';
                }
                break;
                
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (value && !emailRegex.test(value)) {
                    isValid = false;
                    errorMessage = 'Por favor, introduce un email válido';
                }
                break;
                
            case 'phone':
                if (value && !/^[\d\s\-\+\(\)]+$/.test(value)) {
                    isValid = false;
                    errorMessage = 'Por favor, introduce un teléfono válido';
                }
                break;
        }
        
        if (!isValid) {
            this.showFieldError(field, errorMessage);
        }
        
        return isValid;
    }
    
    // Mostrar error en campo
    showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        // Remover error existente si existe
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
        
        // Agregar nuevo error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
        field.parentNode.appendChild(errorDiv);
    }
    
    // Limpiar errores de validación
    clearValidationErrors(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    // Configurar validación de campos relacionados
    setupRelatedFieldValidation() {
        const casaAcogida = document.getElementById('casa_acogida');
        const tieneRelevo = document.getElementById('tiene_relevo');
        const esCapturador = document.getElementById('es_capturador');
        const trapType = document.getElementById('trap_type');
        
        if (casaAcogida && tieneRelevo) {
            casaAcogida.addEventListener('change', () => {
                if (!casaAcogida.checked) {
                    tieneRelevo.checked = false;
                    this.animateFieldChange(tieneRelevo.parentNode);
                }
            });
        }
        
        if (esCapturador && trapType) {
            esCapturador.addEventListener('change', () => {
                if (esCapturador.checked) {
                    trapType.style.borderColor = '#28a745';
                    this.showFieldHint(trapType, 'Recuerda seleccionar el tipo de trampa');
                } else {
                    trapType.style.borderColor = '';
                    this.hideFieldHint(trapType);
                }
            });
        }
    }
    
    // Mostrar sugerencia en campo
    showFieldHint(field, message) {
        this.hideFieldHint(field); // Limpiar hint existente
        
        const hintDiv = document.createElement('div');
        hintDiv.className = 'field-hint';
        hintDiv.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;
        hintDiv.style.cssText = `
            color: #28a745;
            font-size: 12px;
            margin-top: 5px;
            padding: 5px 10px;
            background: #f8fff9;
            border-left: 3px solid #28a745;
            border-radius: 4px;
            animation: fadeIn 0.3s ease;
        `;
        field.parentNode.appendChild(hintDiv);
    }
    
    // Ocultar sugerencia de campo
    hideFieldHint(field) {
        const hint = field.parentNode.querySelector('.field-hint');
        if (hint) {
            hint.remove();
        }
    }
    
    // Configurar elementos interactivos
    setupInteractiveElements() {
        // Mejorar checkboxes
        this.enhanceCheckboxes();
        
        // Mejorar selects
        this.enhanceSelects();
        
        // Agregar efectos de hover
        this.addHoverEffects();
    }
    
    // Mejorar checkboxes
    enhanceCheckboxes() {
        const checkboxes = document.querySelectorAll('.form-check');
        checkboxes.forEach(checkbox => {
            const input = checkbox.querySelector('input[type="checkbox"]');
            
            if (input) {
                input.addEventListener('change', () => {
                    this.animateFieldChange(checkbox);
                    
                    if (input.checked) {
                        checkbox.style.backgroundColor = '#e8f5e8';
                        checkbox.style.borderColor = '#28a745';
                    } else {
                        checkbox.style.backgroundColor = '';
                        checkbox.style.borderColor = '';
                    }
                });
            }
        });
    }
    
    // Mejorar selects
    enhanceSelects() {
        const selects = document.querySelectorAll('select.form-control');
        selects.forEach(select => {
            select.addEventListener('change', () => {
                this.animateFieldChange(select);
                
                if (select.value) {
                    select.style.color = '#333';
                    select.style.fontWeight = '600';
                } else {
                    select.style.color = '#6c757d';
                    select.style.fontWeight = '400';
                }
            });
            
            // Estado inicial
            if (select.value) {
                select.style.color = '#333';
                select.style.fontWeight = '600';
            }
        });
    }
    
    // Agregar efectos de hover
    addHoverEffects() {
        const formGroups = document.querySelectorAll('.form-group');
        formGroups.forEach(group => {
            const input = group.querySelector('.form-control');
            if (input) {
                group.addEventListener('mouseenter', () => {
                    if (!input.matches(':focus')) {
                        input.style.transform = 'translateY(-1px)';
                        input.style.boxShadow = '0 4px 8px rgba(0,0,0,0.08)';
                    }
                });
                
                group.addEventListener('mouseleave', () => {
                    if (!input.matches(':focus')) {
                        input.style.transform = '';
                        input.style.boxShadow = '';
                    }
                });
            }
        });
    }
    
    // Animar cambio de campo
    animateFieldChange(element) {
        element.style.transform = 'scale(1.02)';
        element.style.transition = 'transform 0.2s ease';
        
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 200);
    }
    
    // Agregar estados de loading
    addLoadingStates() {
        const form = document.getElementById('editUserForm');
        if (!form) return;
        
        form.addEventListener('submit', (e) => {
            const submitBtn = document.querySelector('.btn-save');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.8';
            }
        });
    }
    
    // Mejorar navegación
    enhanceNavigation() {
        // Confirmación antes de salir si hay cambios
        const form = document.getElementById('editUserForm');
        if (!form) return;
        
        let formChanged = false;
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                formChanged = true;
            });
        });
        
        // Advertir antes de salir
        window.addEventListener('beforeunload', (e) => {
            if (formChanged) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
        
        // Limpiar flag al enviar formulario
        form.addEventListener('submit', () => {
            formChanged = false;
        });
    }
    
    // Configurar confirmaciones inteligentes
    setupSmartConfirmations() {
        const cancelBtn = document.querySelector('.btn-cancel');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', (e) => {
                const form = document.getElementById('editUserForm');
                const formData = new FormData(form);
                let hasChanges = false;
                
                // Verificar si hay cambios
                for (let [key, value] of formData.entries()) {
                    const originalInput = form.querySelector(`[name="${key}"]`);
                    if (originalInput && originalInput.defaultValue !== value) {
                        hasChanges = true;
                        break;
                    }
                }
                
                if (hasChanges) {
                    e.preventDefault();
                    this.showCancelConfirmation();
                }
            });
        }
    }
    
    // Mostrar confirmación de cancelación
    showCancelConfirmation() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle text-warning"></i>
                            Confirmar Cancelación
                        </h5>
                    </div>
                    <div class="modal-body">
                        <p>Tienes cambios sin guardar. ¿Estás seguro de que deseas cancelar?</p>
                        <p class="text-muted">Los cambios se perderán si continúas.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">
                            Continuar Editando
                        </button>
                        <button type="button" class="btn btn-warning" id="confirmCancel">
                            Cancelar Sin Guardar
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        $(modal).modal('show');
        
        document.getElementById('confirmCancel').addEventListener('click', () => {
            window.location.href = document.querySelector('.btn-cancel').href;
        });
        
        $(modal).on('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }
    
    // Mejorar tooltips
    enhanceTooltips() {
        // Agregar tooltips informativos
        const tooltipData = {
            'username': 'El nombre de usuario debe ser único y contener solo letras, números y guiones bajos',
            'email': 'Dirección de email válida para notificaciones del sistema',
            'role': 'El rol determina los permisos del usuario en el sistema',
            'association': 'Asociación a la que pertenece el usuario',
            'trap_type': 'Tipo de trampa que utiliza si es capturador',
            'activo': 'Usuario activo puede acceder al sistema',
            'casa_acogida': 'Usuario que puede acoger gatos temporalmente',
            'es_capturador': 'Usuario autorizado para capturar gatos'
        };
        
        Object.keys(tooltipData).forEach(fieldName => {
            const field = document.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.setAttribute('title', tooltipData[fieldName]);
                field.setAttribute('data-toggle', 'tooltip');
                field.setAttribute('data-placement', 'top');
            }
        });
        
        // Inicializar tooltips
        $('[data-toggle="tooltip"]').tooltip();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Solo inicializar en la página de edición de usuarios
    if (document.getElementById('editUserForm')) {
        new UserEditEnhancements();
        
        // Agregar animaciones CSS adicionales
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            .field-hint {
                animation: fadeIn 0.3s ease;
            }
            
            .form-check:hover {
                animation: pulse 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }
});