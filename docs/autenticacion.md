# Autenticacion de los addons importados
Revision estatica del archivo custom-addons.tar.gz. No es una auditoria completa ni una prueba del servidor.

## Componentes
- addons/ibloom_kiosk/controllers/menu.py: /menu y /kiosco usan auth="public"; consultan productos con sudo().
- addons/ibloom_kiosk/controllers/main.py: /cocina y las rutas kitchen/orders, kitchen/history y kitchen/state usan auth="user".
- addons/ibloom_kiosk/controllers/pos_kitchen.py: lectura y cambio de estado de pedidos POS requieren auth="user"; el cambio comprueba el POS configurado como ID 3.
- addons/ibloom_kiosk/controllers/unified_kitchen.py: all-orders requiere auth="user" y combina pedidos de ventas y POS usando sudo().
- addons/orbix_portal_shop_redirect/controllers/main.py: delega web_login al controlador estandar de Odoo, lee request.session.uid y redirige al portal a /shop. Segun la consulta del servidor este modulo NO esta instalado.
- addons/orbix_login_redirect_shop/controllers/main.py: delega al login estandar sin redireccion propia; NO instalado segun la consulta.

## Flujo
El navegador solicita la pagina. Odoo procesa auth="public" o auth="user" antes del controlador. Las rutas de cocina esperan una sesion autenticada de Odoo. El controlador consulta los modelos y devuelve HTML o JSON. Los endpoints de estado reciben order_id y state y escriben usando sudo().
El login, creacion y expiracion de sesiones y manejo de contrasenas pertenecen al nucleo Odoo, que no esta incluido aqui. El commit reportado por el servidor es 1e661df964b1b264c9cef3ab28430d4785be3fda; no se inspecciono ese nucleo en esta revision.
No hay autenticacion propia de Chef AI ni emision de JWT o claves API en estos addons.

## Credenciales y tokens
No se detectaron valores de credenciales incrustados durante la revision de los archivos importados.
orbix_social_marketing/models/social_account.py define access_token como fields.Char restringido al grupo de administracion social. La vista lo enmascara con password="True"; eso no cifra el dato. El codigo no implementa cifrado, renovacion o revocacion del token. El modulo no esta instalado en ibloom segun la consulta y action_publish indica que el conector Meta no esta habilitado.
No se importaron datos de cuentas ni valores de tokens, configuracion del servidor o base de datos.

## Hallazgos pendientes
- auth="user" exige login, pero las rutas de cocina no comprueban explicitamente un grupo interno o de cocina antes de elevar permisos con sudo(). Revisar acceso de usuarios portal y alcance por empresa/sitio.
- Los POST kitchen/state y pos-kitchen/state declaran csrf=False sin mecanismo alternativo visible. Revisar proteccion CSRF.
- kitchen/state busca sale.order por ID con sudo() sin restringirlo al sitio o empresa.
- /menu consulta productos con sudo() sin filtro explicito de publicacion web. Revisar exposicion de productos no publicados.
No se corrigio ni desplego nada: la importacion conserva el codigo recibido.
