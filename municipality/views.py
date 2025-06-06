from django.shortcuts import render
import folium

# Create your views here.
def municipality(request):
    # Crear un mapa centrado en Sant Pere de Ribes
    mapa = folium.Map(location=[41.383, 2.178], zoom_start=12)

    # Agregar un marcador con popup personalizado
    popup_html = """
    <div style="width: 200px;">
        <h4 style="margin-bottom: 10px; color: #2c3e50;">Sant Pere de Ribes</h4>
        <p style="margin-bottom: 10px;">¡Haz clic aquí para ver más información!</p>
        <button onclick="parent.handleMapClick()" style="
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        ">Ver Detalles 📍</button>
    </div>
    """

    folium.Marker(
        [41.383, 2.178],
        tooltip="Haz clic para más información",
        popup=folium.Popup(popup_html, max_width=250)
    ).add_to(mapa)

    # Convertir el mapa a HTML
    mapa_html = mapa._repr_html_()

    # Pasar el HTML del mapa a la plantilla
    return render(request, 'municipality.html', {'mapa_html': mapa_html})