# Guía de Estilos Uniformes - Mishilovers

## Descripción General
Se ha implementado un sistema de estilos uniforme para toda la aplicación Mishilovers que garantiza consistencia visual y funcionalidad completa de modo oscuro/claro en todas las páginas.

## Archivos Actualizados

### CSS Actualizados:
- `home/static/styles/index.css` - Página principal
- `cats/static/styles/cats.css` - Sección de gatos
- `users/static/styles/areaStaff.css` - Área de personal
- `users/static/styles/association.css` - Asociaciones
- `users/static/styles/login.css` - Login y autenticación
- `colonies/static/css/map.css` - Mapas y colonias

### Nuevo Archivo Base:
- `home/static/styles/base.css` - Estilos base comunes (NUEVO)

### JavaScript para Modo Oscuro:
- `home/static/js/darkMode.js`
- `cats/static/js/darkMode.js`
- `users/static/js/darkMode.js`
- `colonies/static/js/darkMode.js`
- `veterinarian/static/js/darkMode.js`

## Características Principales

### 1. Diseño Uniforme
- **Colores primarios**: #d2691e (naranja) y #ffe4e1 (rosa claro)
- **Tipografía**: 'Segoe UI', Arial, sans-serif
- **Bordes**: Redondeados (8px-18px)
- **Sombras**: Consistentes en toda la aplicación
- **Gradientes**: Utilizados en botones y elementos destacados

### 2. Modo Oscuro Completo
- **Fondo**: Gradiente de grises oscuros (#1a1a1a a #2a2a2a)
- **Texto**: #f1f1f1 para lectura óptima
- **Acentos**: #ffb380 (naranja claro) para elementos destacados
- **Persistencia**: Se guarda la preferencia en localStorage
- **Sincronización**: Entre pestañas del navegador

### 3. Componentes Estandarizados

#### Botones:
```css
.btn - Botón base
.btn-primary - Botón principal (naranja)
.btn-secondary - Botón secundario (gris)
.btn-success - Botón de éxito (verde)
.btn-danger - Botón de peligro (rojo)
.btn-info - Botón informativo (azul)
.btn-warning - Botón de advertencia (amarillo)
```

#### Formularios:
- Campos con bordes redondeados
- Focus states con color de marca
- Validación visual consistente
- Adaptación completa a modo oscuro

#### Tablas:
- Encabezados con gradiente de marca
- Hover effects suaves
- Filas alternadas para mejor legibilidad
- Bordes redondeados

#### Navegación:
- Fondo consistente con la marca
- Estados activos y hover definidos
- Responsive design

### 4. Responsive Design
- Breakpoint principal: 768px
- Adaptación de espaciados
- Reorganización de elementos
- Botón de modo oscuro reposicionado en móviles

## Cómo Implementar

### En HTML:
```html
<!-- Incluir CSS base (recomendado) -->
<link rel="stylesheet" href="{% static 'styles/base.css' %}">

<!-- Incluir CSS específico de la sección -->
<link rel="stylesheet" href="{% static 'styles/cats.css' %}">

<!-- Incluir JavaScript de modo oscuro -->
<script src="{% static 'js/darkMode.js' %}"></script>
```

### Estructura HTML Recomendada:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mishilovers</title>
    <link rel="stylesheet" href="{% static 'styles/base.css' %}">
    <link rel="stylesheet" href="{% static 'styles/section-specific.css' %}">
</head>
<body>
    <nav>
        <!-- Navegación -->
    </nav>
    
    <main>
        <!-- Contenido principal -->
    </main>
    
    <footer>
        <!-- Footer -->
        <!-- El botón de modo oscuro se agrega automáticamente aquí -->
    </footer>
    
    <script src="{% static 'js/darkMode.js' %}"></script>
</body>
</html>
```

## Clases CSS Útiles

### Utilidades de Espaciado:
- `.mb-1`, `.mb-2`, `.mb-3`, `.mb-4`, `.mb-5` - Margin bottom
- `.mt-1`, `.mt-2`, `.mt-3`, `.mt-4`, `.mt-5` - Margin top

### Utilidades de Texto:
- `.text-center` - Texto centrado
- `.text-left` - Texto alineado a la izquierda
- `.text-right` - Texto alineado a la derecha
- `.text-muted` - Texto en color gris

### Alertas:
- `.alert` - Alerta base
- `.alert-success` - Alerta de éxito
- `.alert-error` / `.alert-danger` - Alerta de error
- `.alert-info` - Alerta informativa
- `.alert-warning` - Alerta de advertencia

## JavaScript - Modo Oscuro

### Uso Básico:
```javascript
// El modo oscuro se inicializa automáticamente
// Detecta preferencias del sistema si no hay configuración guardada

// Métodos disponibles:
window.darkModeManager.toggle()        // Alternar modo
window.darkModeManager.enable()        // Activar modo oscuro
window.darkModeManager.disable()       // Desactivar modo oscuro
window.darkModeManager.isDarkMode()    // Verificar estado actual
```

### Eventos:
```javascript
// Escuchar cambios de modo oscuro
document.addEventListener('darkModeChange', (event) => {
    const isDark = event.detail.isDark;
    console.log('Modo oscuro:', isDark ? 'activado' : 'desactivado');
});
```

## Mejores Prácticas

### 1. Consistencia:
- Usar las clases CSS proporcionadas
- Mantener la paleta de colores definida
- Seguir los patrones de espaciado establecidos

### 2. Accesibilidad:
- Todos los elementos tienen focus states
- Contraste adecuado en ambos modos
- Soporte para `prefers-reduced-motion`

### 3. Performance:
- Transiciones CSS optimizadas
- Carga condicional de estilos cuando sea posible
- Uso eficiente de localStorage

### 4. Mantenimiento:
- Documentar cambios específicos por sección
- Testear en ambos modos (claro/oscuro)
- Verificar responsive en diferentes dispositivos

## Personalización Avanzada

### Variables CSS (Para futuras mejoras):
```css
:root {
    --primary-color: #d2691e;
    --secondary-color: #ffe4e1;
    --dark-bg: #1a1a1a;
    --dark-text: #f1f1f1;
    --border-radius: 8px;
    --box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

### Modo Oscuro para Elementos Específicos:
```css
.dark-mode .mi-elemento-personalizado {
    background: #2a2a2a !important;
    color: #f1f1f1 !important;
    border-color: #555 !important;
}
```

## Resolución de Problemas

### El modo oscuro no funciona:
1. Verificar que el archivo `darkMode.js` esté incluido
2. Comprobar que no hay errores en la consola
3. Asegurar que existe un `<footer>` o el botón se agregará al `<body>`

### Estilos inconsistentes:
1. Incluir `base.css` como primer archivo CSS
2. Verificar que no hay CSS conflictivo con `!important`
3. Comprobar el orden de carga de los archivos CSS

### Problemas responsive:
1. Incluir el meta viewport en `<head>`
2. Testear en diferentes tamaños de pantalla
3. Verificar que las media queries no están siendo sobrescritas

## Mantenimiento Futuro

### Al agregar nuevas páginas:
1. Incluir `base.css` y el JavaScript de modo oscuro
2. Seguir la estructura HTML recomendada
3. Testear en ambos modos de color
4. Verificar responsive design

### Al modificar estilos existentes:
1. Actualizar tanto modo claro como oscuro
2. Mantener consistencia con la guía de estilos
3. Documentar cambios significativos
4. Testear en todas las páginas afectadas
