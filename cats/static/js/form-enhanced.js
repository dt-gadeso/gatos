document.addEventListener('DOMContentLoaded', function() {
    
    function animateElements() {
        const formGroups = document.querySelectorAll('.form-group');
        formGroups.forEach((group, index) => {
            group.style.opacity = '0';
            group.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                group.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                group.style.opacity = '1';
                group.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }
    
    function handleFieldStates() {
        const fields = document.querySelectorAll('.search-form-container input, .search-form-container select, .search-form-container textarea');
        
        fields.forEach(field => {
            field.addEventListener('click', function(e) {
                createRipple(e, this);
            });
            
            field.addEventListener('input', function() {
                validateField(this);
            });
            field.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
                addGlowEffect(this);
            });
            
            field.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
                removeGlowEffect(this);
            });
        });
    }
    
    function createRipple(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    function validateField(field) {
        const formGroup = field.parentElement;
        const errorMessage = formGroup.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
        
        let isValid = true;
        let errorText = '';
        
        if (field.hasAttribute('required') && !field.value.trim()) {
            isValid = false;
            errorText = 'Este campo es obligatorio';
        } else if (field.type === 'email' && field.value && !isValidEmail(field.value)) {
            isValid = false;
            errorText = 'Por favor ingresa un email válido';
        } else if (field.name === 'chip' && field.value && !isValidChip(field.value)) {
            isValid = false;
            errorText = 'El chip debe tener un formato válido';
        }
        
        if (!isValid) {
            field.style.borderColor = '#dc2626';
            field.style.boxShadow = '0 0 0 4px rgba(220, 38, 38, 0.1)';
            showError(formGroup, errorText);
        } else {
            field.style.borderColor = '#22c55e';
            field.style.boxShadow = '0 0 0 4px rgba(34, 197, 94, 0.1)';
        }
    }
    
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    function isValidChip(chip) {
        return chip.length >= 10;
    }
    function showError(formGroup, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        formGroup.appendChild(errorDiv);
    }
    
    function addGlowEffect(element) {
        element.style.filter = 'brightness(1.05)';
        element.style.boxShadow = '0 0 20px rgba(210, 105, 30, 0.2)';
    }
    
    function removeGlowEffect(element) {
        element.style.filter = 'brightness(1)';
    }
    function enhanceFileInput() {
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    // Crear preview de imagen
                    createImagePreview(file, this);
                    
                    // Mostrar información del archivo
                    showFileInfo(file, this);
                }
            });
            
            // Efectos de drag & drop
            fileInput.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.style.borderColor = '#d2691e';
                this.style.background = 'linear-gradient(145deg, #fed7aa 0%, #fdba74 100%)';
            });
            
            fileInput.addEventListener('dragleave', function(e) {
                e.preventDefault();
                this.style.borderColor = '#d2691e';
                this.style.background = 'linear-gradient(145deg, #fef7f0 0%, #fed7aa 10%, #fef7f0 100%)';
            });
            
            fileInput.addEventListener('drop', function(e) {
                e.preventDefault();
                this.style.borderColor = '#d2691e';
                this.style.background = 'linear-gradient(145deg, #fef7f0 0%, #fed7aa 10%, #fef7f0 100%)';
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.files = files;
                    createImagePreview(files[0], this);
                    showFileInfo(files[0], this);
                }
            });
        }
    }
    
    function createImagePreview(file, input) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                let preview = document.querySelector('.image-preview');
                if (!preview) {
                    preview = document.createElement('div');
                    preview.className = 'image-preview';
                    input.parentElement.insertBefore(preview, input.nextSibling);
                }
                
                preview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview" style="
                        max-width: 200px;
                        max-height: 200px;
                        border-radius: 12px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        margin-top: 16px;
                        object-fit: cover;
                        border: 3px solid #d2691e;
                    ">
                `;
            };
            reader.readAsDataURL(file);
        }
    }
    
    function showFileInfo(file, input) {
        let fileInfo = document.querySelector('.file-info');
        if (!fileInfo) {
            fileInfo = document.createElement('div');
            fileInfo.className = 'file-info';
            input.parentElement.insertBefore(fileInfo, input.nextSibling);
        }
        
        const sizeInMB = (file.size / 1024 / 1024).toFixed(2);
        fileInfo.innerHTML = `
            <div style="
                margin-top: 12px;
                padding: 12px;
                background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%);
                border-radius: 8px;
                border: 1px solid #0ea5e9;
                font-size: 14px;
                color: #0c4a6e;
            ">
                <strong>📄 ${file.name}</strong><br>
                <span style="opacity: 0.8;">Tamaño: ${sizeInMB} MB</span>
            </div>
        `;
    }
    
    function enhanceButtons() {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (this.type === 'submit') {
                    this.classList.add('loading');
                    this.disabled = true;
                    
                    // Simular tiempo de carga mínimo
                    setTimeout(() => {
                        this.classList.remove('loading');
                        this.disabled = false;
                    }, 1000);
                }
                
                // Efecto de partículas
                createParticles(e, this);
            });
        });
    }
    
    function createParticles(event, button) {
        const rect = button.getBoundingClientRect();
        const particles = 6;
        
        for (let i = 0; i < particles; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = '4px';
            particle.style.height = '4px';
            particle.style.background = '#d2691e';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.left = (event.clientX - 2) + 'px';
            particle.style.top = (event.clientY - 2) + 'px';
            particle.style.zIndex = '9999';
            
            document.body.appendChild(particle);
            
            const angle = (i * 60) * Math.PI / 180;
            const velocity = 50;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;
            
            particle.animate([
                { transform: 'translate(0, 0) scale(1)', opacity: 1 },
                { transform: `translate(${vx}px, ${vy}px) scale(0)`, opacity: 0 }
            ], {
                duration: 600,
                easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
            }).onfinish = () => {
                particle.remove();
            };
        }
    }
    
    animateElements();
    handleFieldStates();
    enhanceFileInput();
    enhanceButtons();
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(210, 105, 30, 0.3);
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .form-group.focused label {
            color: #d2691e;
            transform: translateX(8px) scale(1.05);
        }
        
        .image-preview {
            text-align: center;
            animation: fadeIn 0.5s ease-out;
        }
        
        .file-info {
            animation: slideUp 0.3s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
});
