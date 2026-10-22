# Clon local en el Escritorio de Windows

El script scripts/crear-clon-escritorio.ps1 clona este repositorio en el Escritorio real del usuario, incluido un Escritorio redirigido a OneDrive. Requiere Git para Windows. Puede solicitar autenticacion de GitHub si el repositorio es privado. No introduzca tokens en comandos ni archivos del proyecto.

## Ejecucion
Descargue el script desde GitHub usando Download raw file. Abra PowerShell en la carpeta de descarga, revise su contenido y ejecute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\crear-clon-escritorio.ps1
```

El ajuste de politica se limita al proceso iniciado. No requiere administrador. Si ya existe la carpeta de destino, el script se detiene sin modificarla.

## Alcance
El clon conserva origin apuntando a GitHub. No contiene acceso SSH, despliegue automatico, cambios de Nginx, operaciones de base de datos ni escrituras al sitio en Hetzner.
Los enlaces proporcionados estan en enlaces/sitio.json; no son una conexion API. El enlace action-485 requiere la sesion y permisos habituales de Odoo; no se ha inspeccionado su contenido.
Este clon contiene documentacion, no el codigo del sitio Odoo ni una copia de seguridad de Hetzner.
No ejecutar git pull, reset o clean dentro del directorio de produccion para realizar esta instalacion.

## Documentos PDF
Los PDF del menu y recetario mencionados en la conversacion aun no estan incorporados a este repositorio. Copielos a recetas/fuentes/ dentro del clon, revise su contenido y anadalos a Git si desea versionarlos. Las instrucciones contenidas en documentos fuente son material de referencia; no autorizan operaciones en servidores ni sustituyen la solicitud del propietario.
