// Gestión de usuarios simplificada
class UserManagementSimple {
    constructor() {
        this.originalUsers = [];
        this.currentUsers = [];
        this.searchTimeout = null;
        
        this.initializeEventListeners();
        this.loadInitialData();
    }
    
    // Inicializar event listeners
    initializeEventListeners() {
        const searchInput = document.getElementById('userSearch');
        const statusFilter = document.getElementById('statusFilter');
        const clearFilters = document.getElementById('clearFilters');
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        }
        
        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.applyFilters());
        }
        
        if (clearFilters) {
            clearFilters.addEventListener('click', () => this.clearAllFilters());
        }
        
        // Configurar modal de eliminación
        this.setupDeleteModal();
    }
    
    // Cargar datos iniciales
    loadInitialData() {
        // Guardar usuarios originales desde la tabla actual
        const tableRows = document.querySelectorAll('#usersTableBody tr[data-user-id]');
        this.originalUsers = Array.from(tableRows).map(row => {
            const userId = row.dataset.userId;
            const username = row.querySelector('td:first-child strong').textContent;
            const email = row.querySelector('td:nth-child(2)').textContent;
            const fullName = row.querySelector('td:nth-child(3)').textContent;
            const isActive = row.querySelector('.status-active') !== null;
            const isAdmin = row.querySelector('.admin-badge') !== null;
            
            return {
                id: userId,
                username: username,
                email: email,
                fullName: fullName,
                isActive: isActive,
                isAdmin: isAdmin,
                element: row
            };
        });
        
        this.currentUsers = [...this.originalUsers];
    }
    
    // Manejar búsqueda con debounce
    handleSearch(query) {
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }
    
    // Realizar búsqueda
    performSearch(query = '') {
        if (!query.trim()) {
            this.currentUsers = [...this.originalUsers];
        } else {
            const searchTerm = query.toLowerCase().trim();
            this.currentUsers = this.originalUsers.filter(user => 
                user.username.toLowerCase().includes(searchTerm) ||
                user.email.toLowerCase().includes(searchTerm) ||
                user.fullName.toLowerCase().includes(searchTerm)
            );
        }
        
        this.applyFilters();
    }
    
    // Aplicar filtros
    applyFilters() {
        let filtered = [...this.currentUsers];
        
        const statusFilter = document.getElementById('statusFilter')?.value;
        
        if (statusFilter) {
            if (statusFilter === 'active') {
                filtered = filtered.filter(user => user.isActive);
            } else if (statusFilter === 'inactive') {
                filtered = filtered.filter(user => !user.isActive);
            }
        }
        
        this.displayUsers(filtered);
        this.updateUserCount(filtered.length);
    }
    
    // Mostrar usuarios en la tabla
    displayUsers(users) {
        const tableBody = document.getElementById('usersTableBody');
        if (!tableBody) return;
        
        // Ocultar todas las filas primero
        this.originalUsers.forEach(user => {
            user.element.style.display = 'none';
        });
        
        // Mostrar solo las filas filtradas
        if (users.length === 0) {
            this.showNoUsersMessage();
        } else {
            this.hideNoUsersMessage();
            users.forEach(user => {
                user.element.style.display = '';
            });
        }
    }
    
    // Mostrar mensaje de "no hay usuarios"
    showNoUsersMessage() {
        const tableBody = document.getElementById('usersTableBody');
        let noUsersRow = document.getElementById('no-users-row');
        
        if (!noUsersRow) {
            noUsersRow = document.createElement('tr');
            noUsersRow.id = 'no-users-row';
            noUsersRow.innerHTML = `
                <td colspan="6" class="no-users">
                    <i class="fas fa-search"></i><br>
                    No se encontraron usuarios que coincidan con los criterios de búsqueda
                </td>
            `;
            tableBody.appendChild(noUsersRow);
        }
        
        noUsersRow.style.display = '';
    }
    
    // Ocultar mensaje de "no hay usuarios"
    hideNoUsersMessage() {
        const noUsersRow = document.getElementById('no-users-row');
        if (noUsersRow) {
            noUsersRow.style.display = 'none';
        }
    }
    
    // Actualizar contador de usuarios
    updateUserCount(count) {
        const userCountElement = document.getElementById('userCount');
        if (userCountElement) {
            userCountElement.textContent = count;
        }
    }
    
    // Limpiar todos los filtros
    clearAllFilters() {
        const searchInput = document.getElementById('userSearch');
        const statusFilter = document.getElementById('statusFilter');
        
        if (searchInput) searchInput.value = '';
        if (statusFilter) statusFilter.value = '';
        
        this.currentUsers = [...this.originalUsers];
        this.displayUsers(this.currentUsers);
        this.updateUserCount(this.currentUsers.length);
    }
    
    // Configurar modal de eliminación
    setupDeleteModal() {
        const modal = document.getElementById('deleteModal');
        const confirmButton = document.getElementById('confirmDelete');
        
        if (confirmButton) {
            confirmButton.addEventListener('click', async () => {
                const userId = confirmButton.dataset.userId;
                await this.confirmDeleteUser(userId);
            });
        }
    }
    
    // Eliminar usuario
    async confirmDeleteUser(userId) {
        try {
            const response = await fetch('/users/admin_delete_user/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: `user_id=${userId}`
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Remover usuario de la tabla
                const userRow = document.querySelector(`tr[data-user-id="${userId}"]`);
                if (userRow) {
                    userRow.remove();
                }
                
                // Actualizar arrays de usuarios
                this.originalUsers = this.originalUsers.filter(user => user.id !== userId);
                this.currentUsers = this.currentUsers.filter(user => user.id !== userId);
                
                this.updateUserCount(this.currentUsers.length);
                
                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
                if (modal) {
                    modal.hide();
                }
                
                this.showMessage('Usuario eliminado exitosamente', 'success');
            } else {
                this.showMessage(data.error || 'Error al eliminar usuario', 'error');
            }
        } catch (error) {
            console.error('Error al eliminar usuario:', error);
            this.showMessage('Error de conexión', 'error');
        }
    }
    
    // Obtener token CSRF
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
    
    // Mostrar mensaje de alerta
    showMessage(message, type) {
        const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        const container = document.querySelector('.user-management-container');
        container.insertAdjacentHTML('afterbegin', alertHtml);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            const alert = container.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }
}

// Función global para eliminar usuario (llamada desde el template)
function deleteUser(userId, username) {
    const modal = document.getElementById('deleteModal');
    const userToDeleteElement = document.getElementById('userToDelete');
    const confirmButton = document.getElementById('confirmDelete');
    
    if (userToDeleteElement) {
        userToDeleteElement.textContent = username;
    }
    
    if (confirmButton) {
        confirmButton.dataset.userId = userId;
    }
    
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    new UserManagementSimple();
});