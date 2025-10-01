# Exportación de Usuarios a Excel - Mishilovers

## Descripción
Se ha implementado la funcionalidad para exportar la lista completa de usuarios del sistema a un archivo Excel (.xlsx).

## Características

### Datos Exportados
El archivo Excel incluye las siguientes columnas:
- **ID**: Identificador único del usuario
- **Usuario**: Nombre de usuario 
- **Email**: Correo electrónico
- **Nombre**: Primer nombre
- **Apellido**: Apellido
- **Teléfono**: Número de teléfono
- **Rol**: Rol asignado al usuario
- **Asociación**: Asociación a la que pertenece
- **Casa Acogida**: Si el usuario tiene casa de acogida (Sí/No)
- **Tiene Relevo**: Si el usuario tiene relevo (Sí/No)
- **Es Capturador**: Si el usuario es capturador (Sí/No)
- **Es Free**: Si el usuario es free (Sí/No)
- **Tipo Trampa**: Tipo de trampa que usa el usuario
- **Activo**: Estado del usuario (Sí/No)
- **Fecha Registro**: Fecha y hora de registro del usuario

### Formato del Archivo
- **Formato**: Excel (.xlsx)
- **Nombre del archivo**: `usuarios_mishilovers_YYYYMMDD_HHMMSS.xlsx`
- **Encabezados**: Con formato azul y texto en blanco
- **Columnas**: Ajustadas automáticamente para mejor legibilidad

## Cómo Usar

### Opción 1: Desde el Panel de Administración
1. Acceder como administrador/superusuario
2. Ir a **Panel de Administración** (`/users/areaStaff/`)
3. En la sección **Gestión Avanzada de Usuarios**
4. Hacer clic en el botón **"Exportar a Excel"** (botón verde)

### Opción 2: Desde Gestión de Usuarios
1. Acceder como administrador/superusuario
2. Ir a **Gestión de Usuarios** (`/users/management/`)
3. En la sección de búsqueda y filtros
4. Hacer clic en el botón **"Exportar Excel"** (botón verde)

## Requisitos de Acceso
- Solo usuarios con permisos de **administrador/superusuario** pueden acceder a esta funcionalidad
- Si un usuario sin permisos intenta acceder, recibirá un error 403 (No autorizado)

## Tecnología Utilizada
- **openpyxl**: Librería Python para crear y manipular archivos Excel
- **Django HttpResponse**: Para servir el archivo como descarga
- **Estilos Excel**: Encabezados con formato profesional

## URLs
- **Exportación**: `/users/export-excel/`
- **Nombre de vista**: `export_users_excel`

## Archivos Modificados
- `users/views.py`: Nueva vista `export_users_excel()`
- `users/urls.py`: Nueva URL para exportación
- `users/templates/areaStaff.html`: Botón de exportación agregado
- `users/templates/user_management.html`: Botón de exportación agregado

## Notas Técnicas
- El archivo se genera dinámicamente en memoria
- No se almacenan archivos temporales en el servidor
- La exportación incluye todos los usuarios del sistema
- Los datos se obtienen con `select_related()` para optimizar consultas
- El archivo se descarga automáticamente al navegador