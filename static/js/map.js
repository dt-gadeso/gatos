document.addEventListener('DOMContentLoaded', function() {
    // Coordenadas aproximadas de Sant Pere de Ribes
    var map = L.map('map').setView([41.2631, 1.7726], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Marcador inicial
    L.marker([41.2631, 1.7726]).addTo(map)
        .bindPopup('Sant Pere de Ribes')
        .openPopup();

    // Permitir al usuario poner un marcador al hacer clic
    var userMarker = null;
    map.on('click', function(e) {
        if (userMarker) {
            map.removeLayer(userMarker);
        }
        userMarker = L.marker(e.latlng).addTo(map)
            .bindPopup('Marcador personalizado')
            .openPopup();
    });
});
