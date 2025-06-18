let map;
let markers = [];
let markerMode = true;
let currentClickCoords = null;
let mapInitialized = false;

window.mapLibraryLoaded = false;
window.mapElementExists = false;

// Verifica si las coordenadas son válidas
function isValidCoordinate(lat, lng) {
    return typeof lat === 'number' && typeof lng === 'number' &&
           !isNaN(lat) && !isNaN(lng) &&
           lat >= -90 && lat <= 90 &&
           lng >= -180 && lng <= 180;
}

document.addEventListener('DOMContentLoaded', function() {
    // Evento principal: inicializa el sistema de mapas al cargar el DOM
    console.log('map.js DOM loaded, starting map initialization...');
    updateMapStatus('Inicializando sistema de mapas...');
    
    window.toggleDebug = toggleDebug;
    window.updateMapStatus = updateMapStatus;
    window.updateDebugInfo = updateDebugInfo;
    window.openSidebar = openSidebar;
    window.closeSidebar = closeSidebar;
    window.openPopup = openPopup;
    window.closePopup = closePopup;
    
    console.log('Global functions assigned');
    
    waitForLeaflet();
    setupEventListeners();
    updateMarkersCount();
    setupMapMonitoring();
});

// Verifica si la librería Leaflet está cargada
function checkLeafletLoaded() {
    if (window.L) {
        window.mapLibraryLoaded = true;
        console.log('Leaflet library loaded successfully');
        return true;
    }
    return false;
}

// Espera hasta que Leaflet esté disponible antes de inicializar el mapa
function waitForLeaflet() {
    if (checkLeafletLoaded()) {
        console.log('Leaflet is ready, starting map initialization');
        updateMapStatus('Leaflet cargado, inicializando mapa...');
        
        setTimeout(() => {
            initializeMap();
        }, 200); // antes: 1000
    } else {
        console.log('Waiting for Leaflet to load...');
        updateMapStatus('Esperando que se cargue Leaflet...');
        setTimeout(waitForLeaflet, 100); // antes: 500
    }
}

// Monitorea el estado de carga del mapa y actualiza el estado visual
function setupMapMonitoring() {
    let mapCheckInterval = setInterval(function() {
        if (window.mapInitialized) {
            updateMapStatus('Mapa cargado correctamente');
            clearInterval(mapCheckInterval);
        } else if (window.map) {
            updateMapStatus('Mapa detectado, configurando eventos...');
        }
    }, 300); // antes: 1000
    
    setTimeout(function() {
        if (!window.mapInitialized) {
            updateMapStatus('Mapa no se cargó automáticamente - Usa "Crear Mapa"', true);
            clearInterval(mapCheckInterval);
        }
    }, 5000); // antes: 30000
}

// Carga los marcadores almacenados en localStorage
function loadMarkers() {
    const saved = localStorage.getItem('mapMarkers');
    if (!saved) {
        console.warn('No se encontraron marcadores en localStorage');
        return;
    }

    try {
        const markersData = JSON.parse(saved);
        markersData.forEach(data => {
            if (isValidCoordinate(data.lat, data.lng)) {
                addMarkerWithInfo(data.lat, data.lng, data.name, data.description, data.color);
            }
        });
        showNotification(`${markersData.length} marcadores locales cargados`);
    } catch (error) {
        console.error('Error al cargar marcadores locales:', error);
        showNotification('Error al cargar marcadores locales');
    }
}

// Muestra u oculta el panel de depuración y actualiza la información periódicamente
function toggleDebug() {
    const debugDiv = document.getElementById('map-debug');
    const debugInfo = document.getElementById('debug-info');
    
    if (debugDiv.style.display === 'none') {
        debugDiv.style.display = 'block';
        updateDebugInfo();
        
        if (window.debugInterval) {
            clearInterval(window.debugInterval);
        }
        window.debugInterval = setInterval(updateDebugInfo, 500); // antes: 2000
    } else {
        debugDiv.style.display = 'none';
        if (window.debugInterval) {
            clearInterval(window.debugInterval);
        }
    }
}

// Actualiza la información de depuración en pantalla
function updateDebugInfo() {
    const debugInfo = document.getElementById('debug-info');
    if (!debugInfo) return;
    
    let info = [];
    
    const leafletLoaded = checkLeafletLoaded();
    info.push(`Leaflet: ${leafletLoaded ? '✓' : '✗'}`);
    
    const mapEl = document.getElementById('map');
    window.mapElementExists = !!mapEl;
    info.push(`Map element: ${mapEl ? '✓' : '✗'}`);
    
    if (mapEl) {
        const leafletContainers = mapEl.querySelectorAll('.leaflet-container');
        info.push(`Leaflet containers: ${leafletContainers.length}`);
        
        const foliumMaps = mapEl.querySelectorAll('[id^="map_"]');
        info.push(`Folium maps: ${foliumMaps.length}`);
        
        const mapDivs = mapEl.querySelectorAll('div[id]');
        info.push(`Map divs: ${mapDivs.length}`);
    }
    
    let mapVarCount = 0;
    for (let key in window) {
        if ((key.startsWith('map_') || key === 'map') && window[key] && typeof window[key] === 'object') {
            try {
                if (window[key].getCenter) mapVarCount++;
            } catch (e) {
            }
        }
    }
    info.push(`Map variables: ${mapVarCount}`);
    
    info.push(`Map initialized: ${window.mapInitialized ? '✓' : '✗'}`);
    info.push(`Map object: ${window.map ? '✓' : '✗'}`);
    
    info.push(`Django map HTML: ${document.getElementById('map').innerHTML.length > 100 ? '✓' : '✗'}`);
    
    debugInfo.textContent = info.join(' | ');
}

// Actualiza el estado visual del mapa en la interfaz
function updateMapStatus(status, isError = false) {
    const statusElement = document.getElementById('map-status-text');
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.style.color = isError ? '#dc3545' : '#28a745';
    }
    console.log('Map Status:', status);
}

// Inicializa el mapa buscando instancias existentes o creando una nueva si es necesario
function initializeMap() {
    if (!window.L) {
        console.log('Leaflet not available yet, waiting...');
        updateMapStatus('Esperando biblioteca Leaflet...');
        setTimeout(initializeMap, 200); // antes: 1000
        return;
    }
    
    let attempts = 0;
    const maxAttempts = 15;
    
    function tryInitialize() {
        attempts++;
        console.log(`Map initialization attempt ${attempts}/${maxAttempts}`);
        updateMapStatus(`Intento ${attempts}/${maxAttempts} - Buscando mapa...`);
        
        const mapElement = document.getElementById('map');
        if (mapElement) {
            console.log('Map element found');
            
            const leafletContainers = mapElement.querySelectorAll('.leaflet-container');
            console.log('Found leaflet containers:', leafletContainers.length);
            
            for (let container of leafletContainers) {
                if (container._leaflet_id) {
                    const leafletId = container._leaflet_id;
                    console.log('Found leaflet container with ID:', leafletId);
                    
                    for (let key in window) {
                        if (key.startsWith('map_') && window[key] && typeof window[key] === 'object') {
                            if (window[key].getContainer && window[key].getContainer() === container) {
                                map = window[key];
                                setupMapEvents();
                                mapInitialized = true;
                                updateMapStatus('Mapa Folium cargado correctamente');
                                console.log('Map initialized via Folium container method');
                                return;
                            }
                        }
                    }
                }
            }
            
            const foliumMaps = mapElement.querySelectorAll('[id^="map_"]');
            console.log('Found potential Folium maps:', foliumMaps.length);
            
            for (let foliumMap of foliumMaps) {
                const mapId = foliumMap.id;
                console.log('Checking map ID:', mapId);
                
                if (window[mapId] && typeof window[mapId] === 'object') {
                    if (window[mapId].getCenter || window[mapId]._container) {
                        map = window[mapId];
                        setupMapEvents();
                        mapInitialized = true;
                        updateMapStatus('Mapa Folium cargado por ID');
                        console.log('Map initialized via Folium ID method');
                        return;
                    }
                }
            }
        }
        
        console.log('Searching globally for Leaflet maps...');
        for (let key in window) {
            const obj = window[key];
            if (obj && 
                typeof obj === 'object' && 
                obj.getCenter && 
                typeof obj.getCenter === 'function' &&
                obj._container &&
                obj.on &&
                typeof obj.on === 'function') {
                
                console.log('Found potential map object:', key);
                try {
                    obj.getCenter();
                    map = obj;
                    setupMapEvents();
                    mapInitialized = true;
                    updateMapStatus('Mapa detectado globalmente');
                    console.log('Map initialized via global search:', key);
                    return;
                } catch (e) {
                    console.log('Object', key, 'is not a valid map:', e.message);
                }
            }
        }
        
        if (attempts >= Math.floor(maxAttempts * 0.8)) {
            console.log('Creating fallback map due to repeated failures...');
            createFallbackMap();
            return;
        }
        
        if (attempts < maxAttempts) {
            const delay = Math.min(100 + (attempts * 50), 500); // antes: Math.min(500 + (attempts * 200), 3000)
            updateMapStatus(`Reintentando en ${delay}ms...`);
            setTimeout(tryInitialize, delay);
        } else {
            console.error('Could not initialize map after', maxAttempts, 'attempts');
            updateMapStatus('No se pudo cargar automáticamente - Usa "Crear Mapa"', true);
            showNotification('No se pudo cargar el mapa automáticamente. Haz clic en "Crear Mapa".');
        }
    }
    
    tryInitialize();
}

// Crea un mapa de respaldo si no se pudo inicializar automáticamente
function createFallbackMap() {
    console.log('Creating fallback map...');
    updateMapStatus('Creando mapa de respaldo...');
    
    if (!window.L) {
        console.error('Leaflet not available for fallback map');
        updateMapStatus('Error: Leaflet no disponible', true);
        return;
    }
    
    try {
        const mapContainer = document.getElementById('map');
        if (!mapContainer) {
            console.error('Map container not found');
            updateMapStatus('Error: Contenedor no encontrado', true);
            return;
        }
        
        mapContainer.innerHTML = '<div id="fallback-map" style="width: 100%; height: 100%; min-height: 400px;"></div>';
        
        map = L.map('fallback-map', {
            attributionControl: true
        }).setView([41.383, 2.178], 10);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Powered by <a href="https://leafletjs.com">Leaflet</a>'
        }).addTo(map);
        
        setupMapEvents();
        mapInitialized = true;
        window.mapInitialized = true;
        window.map = map;
        
        updateMapStatus('Mapa de respaldo creado exitosamente');
        console.log('Fallback map created successfully');
        showNotification('Mapa de respaldo cargado - ¡Ya puedes añadir marcadores!');
        
    } catch (error) {
        console.error('Error creating fallback map:', error);
        updateMapStatus('Error al crear mapa de respaldo: ' + error.message, true);
    }
}

// Configura los listeners de eventos para los formularios y botones de la interfaz
function setupEventListeners() {
    const coordinatesForm = document.getElementById('coordinates-form');
    if (coordinatesForm) {
        coordinatesForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const lat = parseFloat(document.getElementById('latitude').value);
            const lng = parseFloat(document.getElementById('longitude').value);
            
            if (isValidCoordinate(lat, lng)) {
                currentClickCoords = { lat, lng };
                openPopup(lat, lng);
                updateMapView(lat, lng);
            } else {
                alert('Por favor, ingresa coordenadas válidas');
            }
        });
    }

    const clearButton = document.getElementById('clear-markers');
    if (clearButton) {
        clearButton.addEventListener('click', clearAllMarkers);
    }

    const saveButton = document.getElementById('save-markers');
    if (saveButton) {
        saveButton.addEventListener('click', saveMarkers);
    }

    const loadButton = document.getElementById('load-markers');
    if (loadButton) {
        loadButton.addEventListener('click', async function() {
            if (window.loadLocationsFromDB && typeof window.loadLocationsFromDB === 'function') {
                showNotification('Cargando marcadores desde la base de datos...');
                try {
                    await window.loadLocationsFromDB();
                    showNotification('Marcadores cargados desde la base de datos');
                } catch (error) {
                    console.error('Error al cargar marcadores de la base de datos:', error);
                    showNotification('Error al cargar marcadores de la base de datos');
                }
            } else {
                showNotification('Cargando marcadores locales...');
                loadMarkers();
            }
        });
    }

    const toggleButton = document.getElementById('toggle-marker-mode');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleMarkerMode);
    }

    const locationForm = document.getElementById('location-form');
    if (locationForm) {
        locationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveLocationMarker();
        });
    }
}

// Configura los eventos del mapa, como el click para añadir marcadores
function setupMapEvents() {
    if (!map) {
        console.error('Cannot setup events: map is null');
        return;
    }

    try {
        console.log('Setting up map events...');
        
        map.on('click', function(e) {
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;
            
            console.log('Map clicked at:', lat, lng);
            
            updateCoordinateDisplay(lat, lng);
            updateCoordinateInputs(lat, lng);
            
            if (markerMode) {
                currentClickCoords = { lat, lng };
                
                if (window.showLocationPopup && typeof window.showLocationPopup === 'function') {
                    window.showLocationPopup(lat, lng);
                } else {
                    openPopup(lat, lng);
                }
            }
        });

        map.whenReady(function() {
            console.log('Map is ready for interaction');
            updateMapStatus('Mapa listo para usar');
            showNotification('Mapa cargado - Haz clic para añadir marcadores');
        });

        window.mapInitialized = mapInitialized;
        window.map = map;

        console.log('Map events setup complete');
        
    } catch (error) {
        console.error('Error setting up map events:', error);
        updateMapStatus('Error al configurar eventos del mapa', true);
        showNotification('Error al configurar el mapa');
    }
}

// Abre el popup para añadir información de un marcador en las coordenadas dadas
function openPopup(lat, lng) {
    if (!lat || !lng || isNaN(lat) || isNaN(lng)) {
        console.error('Invalid coordinates for popup:', lat, lng);
        alert('Error: Coordenadas inválidas');
        return;
    }

    const popupOverlay = document.getElementById('popup-overlay');
    const popupLatElement = document.getElementById('popup-lat');
    const popupLngElement = document.getElementById('popup-lng');
    
    if (!popupOverlay || !popupLatElement || !popupLngElement) {
        console.error('Popup elements not found');
        alert('Error: No se pudo abrir el popup');
        return;
    }

    popupLatElement.textContent = lat.toFixed(6);
    popupLngElement.textContent = lng.toFixed(6);
    
    popupOverlay.style.display = 'flex';
    
    const locationName = document.getElementById('location-name');
    const locationAddress = document.getElementById('location-address');
    const locationDescription = document.getElementById('location-description');
    const markerColor = document.getElementById('marker-color');
    
    if (locationName) locationName.value = '';
    if (locationAddress) locationAddress.value = '';
    if (locationDescription) locationDescription.value = '';
    if (markerColor) markerColor.value = 'red';
}

// Cierra el popup de añadir marcador
function closePopup() {
    const popupOverlay = document.getElementById('popup-overlay');
    if (popupOverlay) {
        popupOverlay.style.display = 'none';
    }
    currentClickCoords = null;
}

// Guarda un marcador usando los datos del popup y lo añade al mapa
function saveLocationMarker() {
    if (!currentClickCoords) {
        alert('Error: No se ha seleccionado una ubicación. Haz clic en el mapa primero.');
        return;
    }

    if (!mapInitialized || !map) {
        alert('Error: El mapa no está cargado. Espera un momento e intenta de nuevo.');
        return;
    }

    const nameElement = document.getElementById('location-name');
    const addressElement = document.getElementById('location-address');
    const descriptionElement = document.getElementById('location-description');
    const colorElement = document.getElementById('marker-color');

    if (!nameElement) {
        alert('Error: No se encontró el campo de nombre');
        return;
    }

    const name = nameElement.value.trim();
    const address = addressElement ? addressElement.value.trim() : '';
    const description = descriptionElement ? descriptionElement.value.trim() : '';
    const color = colorElement ? colorElement.value : 'red';

    if (!name) {
        alert('Por favor, ingresa un nombre para el lugar');
        return;
    }

    try {
        addMarkerWithInfo(currentClickCoords.lat, currentClickCoords.lng, name, description, color, address);
        closePopup();
        showNotification(`Marcador "${name}" añadido exitosamente`);
    } catch (error) {
        console.error('Error adding marker:', error);
        alert('Error al añadir el marcador. Intenta de nuevo.');
    }
}

// Modifica addMarkerWithInfo para aceptar address y guardarlo en el objeto data
function addMarkerWithInfo(lat, lng, name, description, color = 'red', address = '') {
    if (!mapInitialized || !map) {
        console.error('Mapa no inicializado');
        return null;
    }

    if (!isValidCoordinate(lat, lng)) {
        console.error('Coordenadas inválidas:', lat, lng);
        return null;
    }

    try {
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div class="marker-pin marker-${color}">📍</div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 30]
        });

        const marker = L.marker([lat, lng], { icon }).addTo(map);

        marker.bindPopup(`
            <div class="marker-popup">
                <h4>${escapeHtml(name)}</h4>
                ${address ? `<div><b>Dirección:</b> ${escapeHtml(address)}</div>` : ''}
                ${description ? `<p>${escapeHtml(description)}</p>` : ''}
                <small>Lat: ${lat.toFixed(5)}, Lng: ${lng.toFixed(5)}</small>
            </div>
        `);

        markers.push({ marker, data: { lat, lng, name, address, description, color } });
        updateMarkersCount();

        return marker;
    } catch (e) {
        console.error('Error creando marcador:', e);
        return null;
    }
}

// Escapa caracteres peligrosos para evitar XSS en los popups
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Permite editar un marcador existente (eliminándolo y abriendo el popup con sus datos)
function editMarker(index) {
    if (markers[index]) {
        const markerData = markers[index].data;
        currentClickCoords = { lat: markerData.lat, lng: markerData.lng };
        
        const locationName = document.getElementById('location-name');
        const locationDescription = document.getElementById('location-description');
        const markerColor = document.getElementById('marker-color');
        
        if (locationName) locationName.value = markerData.name;
        if (locationDescription) locationDescription.value = markerData.description || '';
        if (markerColor) markerColor.value = markerData.color;
        
        removeMarker(index);
        
        openPopup(markerData.lat, markerData.lng);
    }
}

// Elimina un marcador específico del mapa y del arreglo
function removeMarker(index) {
    if (markers[index] && map) {
        try {
            map.removeLayer(markers[index].marker);
            markers.splice(index, 1);
            updateMarkersCount();
            showNotification('Marcador eliminado');
        } catch (error) {
            console.error('Error removing marker:', error);
        }
    }
}

// Elimina todos los marcadores del mapa y del arreglo
function clearAllMarkers() {
    if (markers.length === 0) {
        alert('No hay marcadores para eliminar');
        return;
    }
    
    if (confirm('¿Estás seguro de que quieres eliminar todos los marcadores?')) {
        if (map) {
            markers.forEach(markerData => {
                try {
                    map.removeLayer(markerData.marker);
                } catch (error) {
                    console.error('Error removing marker:', error);
                }
            });
        }
        markers = [];
        updateMarkersCount();
        showNotification('Todos los marcadores eliminados');
    }
}

// Guarda los marcadores en la base de datos o en localStorage si no hay backend
async function saveMarkers() {
    if (markers.length === 0) {
        alert('No hay marcadores para guardar');
        return;
    }

    if (window.saveLocationToDB && typeof window.saveLocationToDB === 'function') {
        let successCount = 0;
        let errorCount = 0;
        
        showNotification('Guardando marcadores en la base de datos...');

        try {
            for (let markerData of markers) {
                const locationData = {
                    name: markerData.data.name,
                    address: markerData.data.address || '',
                    description: markerData.data.description || '',
                    municipality_id: 1,
                    latitude: markerData.data.lat,
                    longitude: markerData.data.lng
                };

                try {
                    const savedId = await window.saveLocationToDB(locationData);
                    if (savedId) {
                        successCount++;
                    } else {
                        errorCount++;
                    }
                } catch (error) {
                    errorCount++;
                    console.error('Error saving marker to database:', error);
                }
            }

            if (successCount > 0) {
                showNotification(`${successCount} marcadores guardados en la base de datos`);
                
                clearAllMarkers();
                
                if (window.loadLocationsFromDB) {
                    await window.loadLocationsFromDB();
                }
            }
            
            if (errorCount > 0) {
                showNotification(`Error: ${errorCount} marcadores no se pudieron guardar`);
            }

        } catch (error) {
            console.error('Error saving markers to database:', error);
            saveMarkersToLocalStorage();
        }
    } else {
        saveMarkersToLocalStorage();
    }
}

// Guarda los marcadores en localStorage
function saveMarkersToLocalStorage() {
    try {
        const markersData = markers.map(markerData => markerData.data);
        localStorage.setItem('mapMarkers', JSON.stringify(markersData));
        showNotification(`${markers.length} marcadores guardados localmente`);
    } catch (error) {
        console.error('Error saving markers to localStorage:', error);
        alert('Error al guardar los marcadores');
    }
}

// Espera a que el mapa esté listo para cargar los marcadores locales
function onMapReady() {
    if (mapInitialized) {
        setTimeout(() => {
            loadMarkers();
        }, 200); // antes: 1000
    } else {
        setTimeout(onMapReady, 100); // antes: 500
    }
}

setTimeout(() => {
    setTimeout(onMapReady, 1000); // antes: 8000
}, 20); // antes: 100

// Abre la barra lateral de la interfaz
function openSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    if (sidebar) sidebar.classList.add('open');
    if (overlay) overlay.classList.add('active');
}

// Cierra la barra lateral de la interfaz
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
}

document.addEventListener('keydown', function(e) {
    // Permite cerrar la barra lateral y el popup con la tecla Escape
    if (e.key === 'Escape') {
        closeSidebar();
        closePopup();
    }
});

window.toggleDebug = toggleDebug;

// Obtiene ubicaciones desde la base de datos y las muestra en el mapa
function fetchAndDisplayDatabaseLocations() {
    if (!window.mapInitialized || !window.map) {
        console.warn('Mapa no está listo. Esperando...');
        return;
    }

    fetch('/colonies/get_locations_json/')
        .then(response => response.json())
        .then(data => {
            if (!Array.isArray(data.locations)) {
                console.warn('Respuesta no contiene lista de ubicaciones');
                return;
            }

            // Limpiar marcadores existentes antes de agregar los nuevos
            if (map) {
                markers.forEach(markerData => {
                    try {
                        map.removeLayer(markerData.marker);
                    } catch (error) {
                        console.error('Error removing marker:', error);
                    }
                });
            }
            markers = [];
            updateMarkersCount();

            console.log('Ubicaciones cargadas desde la BD:', data.locations.length);

            data.locations.forEach(loc => {
                if (isValidCoordinate(loc.latitude, loc.longitude)) {
                    addMarkerWithInfo(
                        loc.latitude,
                        loc.longitude,
                        loc.name || 'Sin nombre',
                        loc.description || '',
                        'blue'
                    );
                }
            });
        })
        .catch(error => {
            console.error('Error al obtener ubicaciones de la base de datos:', error);
        });
}

window.fetchAndDisplayDatabaseLocations = fetchAndDisplayDatabaseLocations;
window.loadMarkers = loadMarkers;

// Muestra la lista de marcadores con botón para borrar individualmente
function updateMarkersList() {
    const listDiv = document.getElementById('markers-list');
    if (!listDiv) return;
    if (markers.length === 0) {
        listDiv.innerHTML = '<small>No hay marcadores.</small>';
        return;
    }
    let html = '<ul style="list-style:none;padding:0;">';
    markers.forEach((m, idx) => {
        html += `<li style="margin-bottom:4px;">
            <span title="Lat: ${m.data.lat}, Lng: ${m.data.lng}">${escapeHtml(m.data.name)}</span>
            <button type="button" class="map-btn btn-danger" style="margin-left:8px;padding:2px 8px;font-size:0.9em;" onclick="removeMarker(${idx})">Borrar</button>
        </li>`;
    });
    html += '</ul>';
    listDiv.innerHTML = html;
}

// Actualiza el contador y la lista de marcadores
function updateMarkersCount() {
    const countElement = document.getElementById('markers-count');
    if (countElement) {
        countElement.textContent = markers.length;
    }
    updateMarkersList();
}

