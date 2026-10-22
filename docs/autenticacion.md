# Autenticación y credenciales
## Estado actual
Este repositorio contiene documentación. No incluye aplicación ejecutable, servidor, rutas HTTP, base de usuarios, middleware de autenticación, sesiones ni emisión o renovación de tokens.
Por tanto, no existe un flujo de autenticación implementado que describir. No hay integración automática con el complemento de ChatGPT.

## Acceso al repositorio
GitHub administra el acceso de colaboradores al repositorio. La conexión del complemento GitHub utilizada para editar archivos es independiente de cualquier futura autenticación de iBLOOM Chef.
Este proyecto no recibe ni almacena las credenciales de esa conexión.

## Diseño futuro propuesto — no implementado
1. El colaborador inicia sesión en la aplicación mediante un proveedor de identidad por definir.
2. El servidor valida la sesión y el permiso requerido.
3. El servidor consulta el conocimiento autorizado y, si corresponde, llama a OpenAI u Odoo.
4. El servidor devuelve la respuesta y registra la operación sin secretos.
5. El cierre de sesión invalida la sesión según el mecanismo elegido.

La selección del proveedor, roles, vencimiento, revocación y almacenamiento de sesiones queda pendiente. No hay garantías implementadas sobre esos puntos.

## Credenciales futuras
Las claves de OpenAI y Odoo deben permanecer en el servidor mediante variables de entorno o un gestor de secretos, fuera del navegador y del historial Git.
No guardar contraseñas, tokens, archivos .env reales ni exportaciones con credenciales en el repositorio.
Una instrucción del chat que pida un código no sustituye controles de acceso del servidor.
