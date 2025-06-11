let map;
let markers = [];
let markerMode = true;
let currentClickCoords = null;
let mapInitialized = false;

// Global variables for debugging
window.mapLibraryLoaded = false;
window.mapElementExists = false;

function isValidCoordinate(lat, lng) {
    return typeof lat === 'number' && typeof lng === 'number' &&
           !isNaN(lat) && !isNaN(lng) &&
           lat >= -90 && lat <= 90 &&
           lng >= -180 && lng <= 180;
}

// Initialize map functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('map.js DOM loaded, starting map initialization...');
    updateMapStatus('Inicializando sistema de mapas...');
    
    // Make sure functions are available
    window.forceCreateMap = forceCreateMap;
    window.toggleDebug = toggleDebug;
    window.updateMapStatus = updateMapStatus;
    window.updateDebugInfo = updateDebugInfo;
    window.openSidebar = openSidebar;
    window.closeSidebar = closeSidebar;
    window.openPopup = openPopup;
    window.closePopup = closePopup;
    
    console.log('Global functions assigned');
    
    // Start waiting for Leaflet and initialize everything
    waitForLeaflet();
    setupEventListeners();
    updateMarkersCount();
    setupMapMonitoring();
});

// Check Leaflet loading
function checkLeafletLoaded() {
    if (window.L) {
        window.mapLibraryLoaded = true;
        console.log('Leaflet library loaded successfully');
        return true;
    }
    return false;
}

// Wait for Leaflet to load before initializing
function waitForLeaflet() {
    if (checkLeafletLoaded()) {
        console.log('Leaflet is ready, starting map initialization');
        updateMapStatus('Leaflet cargado, inicializando mapa...');
        
        // Give a moment for any Django-generated map to load
        setTimeout(() => {
            initializeMap();
        }, 1000);
    } else {
        console.log('Waiting for Leaflet to load...');
        updateMapStatus('Esperando que se cargue Leaflet...');
        setTimeout(waitForLeaflet, 500);
    }
}

// Monitor map initialization
function setupMapMonitoring() {
    let mapCheckInterval = setInterval(function() {
        if (window.mapInitialized) {
            updateMapStatus('Mapa cargado correctamente');
            clearInterval(mapCheckInterval);
        } else if (window.map) {
            updateMapStatus('Mapa detectado, configurando eventos...');
        }
    }, 1000);
    
    // Stop checking after 30 seconds
    setTimeout(function() {
        if (!window.mapInitialized) {
            updateMapStatus('Mapa no se cargó automáticamente - Usa "Crear Mapa"', true);
            clearInterval(mapCheckInterval);
        }
    }, 30000);
}
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


// Force create map function
function forceCreateMap() {
    console.log('forceCreateMap called from map.js');
    updateMapStatus('Forzando creación del mapa...');
    
    if (!checkLeafletLoaded()) {
        updateMapStatus('Error: Biblioteca Leaflet no disponible', true);
        showNotification('Error: La biblioteca de mapas no está disponible. Revisa tu conexión a internet.');
        return;
    }
    
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        updateMapStatus('Error: Contenedor del mapa no encontrado', true);
        showNotification('Error: Contenedor del mapa no encontrado');
        return;
    }
    
    console.log('Map container found, creating forced map...');
    
    // Clear existing content
    mapContainer.innerHTML = '<div id="forced-map" style="width: 100%; height: 100%; min-height: 400px; background: #f0f0f0; display: flex; align-items: center; justify-content: center;"><div>Cargando mapa...</div></div>';
    
    // Give a moment for the HTML to render
    setTimeout(() => {
        try {
            console.log('Creating Leaflet map...');
            
            // Create map with Barcelona coordinates
            map = L.map('forced-map', {
                attributionControl: true
            }).setView([41.383, 2.178], 10);
            
            console.log('Map created, adding tiles...');
            
            // Add OpenStreetMap tiles with proper attribution
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Powered by <a href="https://leafletjs.com">Leaflet</a>'
            }).addTo(map);
            
            console.log('Tiles added, setting up events...');
            
            // Setup map events
            setupMapEvents();
            mapInitialized = true;
            window.mapInitialized = true;
            window.map = map;
            
            updateMapStatus('Mapa creado manualmente');
            showNotification('Mapa creado exitosamente - ¡Ya puedes añadir marcadores!');
            
            console.log('Forced map creation completed successfully');
            
        } catch (error) {
            console.error('Error creating forced map:', error);
            updateMapStatus('Error al crear el mapa: ' + error.message, true);
            showNotification('Error al crear el mapa: ' + error.message);
            
            // Fallback HTML message
            mapContainer.innerHTML = `
                <div style="width: 100%; height: 100%; min-height: 400px; background: #f8f9fa; display: flex; align-items: center; justify-content: center; color: #dc3545; text-align: center; padding: 20px;">
                    <div>
                        <h4>Error al crear el mapa</h4>
                        <p>${error.message}</p>
                        <button onclick="window.location.reload()" style="padding: 10px 20px; background: #d2691e; color: white; border: none; border-radius: 5px; cursor: pointer;">
                            Recargar Página
                        </button>
                    </div>
                </div>
            `;
        }
    }, 100);
}

// Debug functions
function toggleDebug() {
    const debugDiv = document.getElementById('map-debug');
    const debugInfo = document.getElementById('debug-info');
    
    if (debugDiv.style.display === 'none') {
        debugDiv.style.display = 'block';
        updateDebugInfo();
        
        // Update debug info every 2 seconds
        if (window.debugInterval) {
            clearInterval(window.debugInterval);
        }
        window.debugInterval = setInterval(updateDebugInfo, 2000);
    } else {
        debugDiv.style.display = 'none';
        if (window.debugInterval) {
            clearInterval(window.debugInterval);
        }
    }
}

function updateDebugInfo() {
    const debugInfo = document.getElementById('debug-info');
    if (!debugInfo) return;
    
    let info = [];
    
    // Check for Leaflet
    const leafletLoaded = checkLeafletLoaded();
    info.push(`Leaflet: ${leafletLoaded ? '✓' : '✗'}`);
    
    // Check for map elements
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
    
    // Check for map variables
    let mapVarCount = 0;
    for (let key in window) {
        if ((key.startsWith('map_') || key === 'map') && window[key] && typeof window[key] === 'object') {
            try {
                if (window[key].getCenter) mapVarCount++;
            } catch (e) {
                // Not a valid map object
            }
        }
    }
    info.push(`Map variables: ${mapVarCount}`);
    
    // Check current map status
    info.push(`Map initialized: ${window.mapInitialized ? '✓' : '✗'}`);
    info.push(`Map object: ${window.map ? '✓' : '✗'}`);
    
    // Additional debugging
    info.push(`Django map HTML: ${document.getElementById('map').innerHTML.length > 100 ? '✓' : '✗'}`);
    
    debugInfo.textContent = info.join(' | ');
}

function updateMapStatus(status, isError = false) {
    const statusElement = document.getElementById('map-status-text');
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.style.color = isError ? '#dc3545' : '#28a745';
    }
    console.log('Map Status:', status);
}

function initializeMap() {
    if (!window.L) {
        console.log('Leaflet not available yet, waiting...');
        updateMapStatus('Esperando biblioteca Leaflet...');
        setTimeout(initializeMap, 1000);
        return;
    }
    
    let attempts = 0;
    const maxAttempts = 15;
    
    function tryInitialize() {
        attempts++;
        console.log(`Map initialization attempt ${attempts}/${maxAttempts}`);
        updateMapStatus(`Intento ${attempts}/${maxAttempts} - Buscando mapa...`);
        
        // Method 1: Direct Folium map detection
        const mapElement = document.getElementById('map');
        if (mapElement) {
            console.log('Map element found');
            
            // Look for any div with leaflet-container class
            const leafletContainers = mapElement.querySelectorAll('.leaflet-container');
            console.log('Found leaflet containers:', leafletContainers.length);
            
            for (let container of leafletContainers) {
                if (container._leaflet_id) {
                    // Try to get map from Leaflet's internal registry
                    const leafletId = container._leaflet_id;
                    console.log('Found leaflet container with ID:', leafletId);
                    
                    // Check window for map instances
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
            
            // Method 2: Check for Folium map in window
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
        
        // Method 3: Global search for any Leaflet map
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
                    // Test if it's a real map by calling a method
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
        
        // Method 4: Create fallback map if we're at 80% of attempts
        if (attempts >= Math.floor(maxAttempts * 0.8)) {
            console.log('Creating fallback map due to repeated failures...');
            createFallbackMap();
            return;
        }
        
        // Retry if not found and attempts remaining
        if (attempts < maxAttempts) {
            const delay = Math.min(500 + (attempts * 200), 3000);
            updateMapStatus(`Reintentando en ${delay}ms...`);
            setTimeout(tryInitialize, delay);
        } else {
            console.error('Could not initialize map after', maxAttempts, 'attempts');
            updateMapStatus('No se pudo cargar automáticamente - Usa "Crear Mapa"', true);
            showNotification('No se pudo cargar el mapa automáticamente. Haz clic en "Crear Mapa".');
        }
    }
    
    // Start trying immediately since Leaflet is available
    tryInitialize();
}

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
        
        // Clear any existing content
        mapContainer.innerHTML = '<div id="fallback-map" style="width: 100%; height: 100%; min-height: 400px;"></div>';
        
        // Create new map centered on Barcelona/Catalonia with attribution
        map = L.map('fallback-map', {
            attributionControl: true
        }).setView([41.383, 2.178], 10);
        
        // Add OpenStreetMap tile layer with enhanced attribution
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Powered by <a href="https://leafletjs.com">Leaflet</a>'
        }).addTo(map);
        
        // Setup events and mark as initialized
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

function setupEventListeners() {
    // Coordinates form submission
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

    // Clear markers button
    const clearButton = document.getElementById('clear-markers');
    if (clearButton) {
        clearButton.addEventListener('click', clearAllMarkers);
    }

    // Save markers button
    const saveButton = document.getElementById('save-markers');
    if (saveButton) {
        saveButton.addEventListener('click', saveMarkers);
    }

    // Load markers button
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
                // Fallback: cargar desde localStorage
                showNotification('Cargando marcadores locales...');
                loadMarkers();
            }
        });
    }

    // Toggle marker mode
    const toggleButton = document.getElementById('toggle-marker-mode');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleMarkerMode);
    }

    // Location form submission
    const locationForm = document.getElementById('location-form');
    if (locationForm) {
        locationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveLocationMarker();
        });
    }
}

function setupMapEvents() {
    if (!map) {
        console.error('Cannot setup events: map is null');
        return;
    }

    try {
        console.log('Setting up map events...');
        
        // Add click event to map
        map.on('click', function(e) {
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;
            
            console.log('Map clicked at:', lat, lng);
            
            // Always update coordinate display
            updateCoordinateDisplay(lat, lng);
            updateCoordinateInputs(lat, lng);
            
            if (markerMode) {
                currentClickCoords = { lat, lng };
                
                // Check if we have database integration available
                if (window.showLocationPopup && typeof window.showLocationPopup === 'function') {
                    // Use database integration popup
                    window.showLocationPopup(lat, lng);
                } else {
                    // Use local storage popup
                    openPopup(lat, lng);
                }
            }
        });

        // Add map ready event
        map.whenReady(function() {
            console.log('Map is ready for interaction');
            updateMapStatus('Mapa listo para usar');
            showNotification('Mapa cargado - Haz clic para añadir marcadores');
            // No cargar automáticamente los marcadores de la base de datos aquí
            // El usuario debe usar el botón "Cargar Marcadores"
        });

        // Update global variables
        window.mapInitialized = mapInitialized;
        window.map = map;

        console.log('Map events setup complete');
        
    } catch (error) {
        console.error('Error setting up map events:', error);
        updateMapStatus('Error al configurar eventos del mapa', true);
        showNotification('Error al configurar el mapa');
    }
}

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
    
    // Use flex display instead of classList for compatibility
    popupOverlay.style.display = 'flex';
    
    // Clear previous form data
    const locationName = document.getElementById('location-name');
    const locationAddress = document.getElementById('location-address');
    const locationDescription = document.getElementById('location-description');
    const markerColor = document.getElementById('marker-color');
    
    if (locationName) locationName.value = '';
    if (locationAddress) locationAddress.value = '';
    if (locationDescription) locationDescription.value = '';
    if (markerColor) markerColor.value = 'red';
}

function closePopup() {
    const popupOverlay = document.getElementById('popup-overlay');
    if (popupOverlay) {
        popupOverlay.style.display = 'none';
    }
    currentClickCoords = null;
}

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
    const descriptionElement = document.getElementById('location-description');
    const colorElement = document.getElementById('marker-color');

    if (!nameElement) {
        alert('Error: No se encontró el campo de nombre');
        return;
    }

    const name = nameElement.value.trim();
    const description = descriptionElement ? descriptionElement.value.trim() : '';
    const color = colorElement ? colorElement.value : 'red';

    if (!name) {
        alert('Por favor, ingresa un nombre para el lugar');
        return;
    }

    try {
        addMarkerWithInfo(currentClickCoords.lat, currentClickCoords.lng, name, description, color);
        closePopup();
        showNotification(`Marcador "${name}" añadido exitosamente`);
    } catch (error) {
        console.error('Error adding marker:', error);
        alert('Error al añadir el marcador. Intenta de nuevo.');
    }
}

// function addMarkerWithInfo(lat, lng, name, description, color = 'red') {
//     if (!mapInitialized || !map) {
//         console.error('Map not initialized');
//         alert('Error: El mapa no está disponible');
//         return null;
//     }

//     if (!isValidCoordinate(lat, lng)) {
//         console.error('Invalid coordinates:', lat, lng);
//         alert('Error: Coordenadas inválidas');
//         return null;
//     }

//     try {
//         // Ensure Leaflet is available
//         if (!window.L) {
//             throw new Error('Leaflet library not available');
//         }

//         // Create custom icon
//         const icon = L.divIcon({
//             className: 'custom-marker',
//             html: `<div class="marker-pin marker-${color}">📍</div>`,
//             iconSize: [30, 30],
//             iconAnchor: [15, 30]
//         });

//         // Create marker
//         const marker = L.marker([lat, lng], { icon: icon }).addTo(map);
        
//         // Create popup content
//         const popupContent = `
//             <div class="marker-popup">
//                 <h4>${escapeHtml(name)}</h4>
//                 ${description ? `<p>${escapeHtml(description)}</p>` : ''}
//                 <div class="popup-coords">
//                     <small>Lat: ${lat.toFixed(6)}, Lng: ${lng.toFixed(6)}</small>
//                 </div>
//                 <div class="popup-actions">
//                     <button onclick="editMarker(${markers.length})" class="edit-btn">✏️ Editar</button>
//                     <button onclick="removeMarker(${markers.length})" class="delete-btn">🗑️ Eliminar</button>
//                 </div>
//             </div>
//         `;
        
//         marker.bindPopup(popupContent);
        
//         // Store marker data
//         const markerData = {
//             marker: marker,
//             data: { name, description, color, lat, lng }
//         };
        
//         markers.push(markerData);
//         updateMarkersCount();
        
//         console.log('Marker created successfully:', name);
//         return marker;
//     } catch (error) {
//         console.error('Error creating marker:', error);
//         alert('Error al crear el marcador: ' + error.message);
//         return null;
//     }
// }
function addMarkerWithInfo(lat, lng, name, description, color = 'red') {
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
                ${description ? `<p>${escapeHtml(description)}</p>` : ''}
                <small>Lat: ${lat.toFixed(5)}, Lng: ${lng.toFixed(5)}</small>
            </div>
        `);

        markers.push({ marker, data: { lat, lng, name, description, color } });
        updateMarkersCount();

        return marker;
    } catch (e) {
        console.error('Error creando marcador:', e);
        return null;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function editMarker(index) {
    if (markers[index]) {
        const markerData = markers[index].data;
        currentClickCoords = { lat: markerData.lat, lng: markerData.lng };
        
        // Fill form with existing data
        const locationName = document.getElementById('location-name');
        const locationDescription = document.getElementById('location-description');
        const markerColor = document.getElementById('marker-color');
        
        if (locationName) locationName.value = markerData.name;
        if (locationDescription) locationDescription.value = markerData.description || '';
        if (markerColor) markerColor.value = markerData.color;
        
        // Remove old marker
        removeMarker(index);
        
        // Open popup for editing
        openPopup(markerData.lat, markerData.lng);
    }
}

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

// Updated saveMarkers function to save to database if available
async function saveMarkers() {
    if (markers.length === 0) {
        alert('No hay marcadores para guardar');
        return;
    }

    // Check if database saving is available
    if (window.saveLocationToDB && typeof window.saveLocationToDB === 'function') {
        let successCount = 0;
        let errorCount = 0;
        
        showNotification('Guardando marcadores en la base de datos...');

        try {
            for (let markerData of markers) {
                const locationData = {
                    name: markerData.data.name,
                    address: markerData.data.name, // Use name as address if no address provided
                    description: markerData.data.description || '',
                    municipality_id: 1, // Default municipality ID
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
                
                // Clear local markers since they're now in the database
                clearAllMarkers();
                
                // Reload markers from database
                if (window.loadLocationsFromDB) {
                    await window.loadLocationsFromDB();
                }
            }
            
            if (errorCount > 0) {
                showNotification(`Error: ${errorCount} marcadores no se pudieron guardar`);
            }

        } catch (error) {
            console.error('Error saving markers to database:', error);
            // Fallback to localStorage
            saveMarkersToLocalStorage();
        }
    } else {
        // Fallback to localStorage
        saveMarkersToLocalStorage();
    }
}

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

// Load saved markers when map is ready
function onMapReady() {
    if (mapInitialized) {
        setTimeout(() => {
            loadMarkers();
        }, 1000);
    } else {
        setTimeout(onMapReady, 500);
    }
}

// Start loading markers after a delay
setTimeout(() => {
    setTimeout(onMapReady, 8000);
}, 100);

// Sidebar functions
function openSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    if (sidebar) sidebar.classList.add('open');
    if (overlay) overlay.classList.add('active');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
}

// Close popup on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeSidebar();
        closePopup();
    }
});

// Make functions globally available immediately
window.forceCreateMap = forceCreateMap;
window.toggleDebug = toggleDebug;

function fetchAndDisplayDatabaseLocations() {
    if (!window.mapInitialized || !window.map) {
        console.warn('Mapa no está listo. Esperando...');
        return;
    }

    fetch('/municipality/get_locations_json/')
        .then(response => response.json())
        .then(data => {
            if (!Array.isArray(data.locations)) {
                console.warn('Respuesta no contiene lista de ubicaciones');
                return;
            }

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

