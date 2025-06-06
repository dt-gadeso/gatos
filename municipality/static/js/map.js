// Función para abrir el sidebar
function openSidebar() {
    document.getElementById('sidebar').classList.add('open');
    document.getElementById('overlay').classList.add('active');
    document.getElementById('mainContent').classList.add('sidebar-open');
}

// Función para cerrar el sidebar
function closeSidebar() {
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('overlay').classList.remove('active');
    document.getElementById('mainContent').classList.remove('sidebar-open');
}

// Función para interceptar clics en el mapa
function interceptMapClicks() {
    // Esperar a que el mapa se cargue
    setTimeout(() => {
        const mapContainer = document.querySelector('.folium-map');
        if (mapContainer) {
            // Buscar todos los popups/markers
            const popups = mapContainer.querySelectorAll('.leaflet-popup, .leaflet-marker-icon');
            
            popups.forEach(popup => {
                popup.addEventListener('click', function(e) {
                    // Pequeño delay para permitir que el popup se abra primero
                    setTimeout(() => {
                        openSidebar();
                    }, 100);
                });
            });
        }
    }, 1000);
}

// Función alternativa para manejar clics en el mapa
function handleMapClick() {
    openSidebar();
}

// Inicializar cuando la página se carga
document.addEventListener('DOMContentLoaded', function() {
    interceptMapClicks();
    
    // También escuchar clics en el contenedor del mapa como fallback
    const mapContainer = document.querySelector('.map-container');
    if (mapContainer) {
        mapContainer.addEventListener('click', function(e) {
            // Solo abrir si el clic fue en un elemento del mapa
            if (e.target.closest('.leaflet-popup') || e.target.closest('.leaflet-marker-icon')) {
                setTimeout(() => {
                    openSidebar();
                }, 100);
            }
        });
    }
});

// Cerrar sidebar con tecla Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeSidebar();
    }
});