from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home


class OrbixPortalShopRedirect(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):

        # Ejecutar primero el login estándar de Odoo.
        response = super().web_login(
            redirect=redirect,
            **kw
        )

        uid = request.session.uid

        # Si todavía no inició sesión, devolver login normal.
        if not uid:
            return response

        user = request.env['res.users'].sudo().browse(uid)

        if not user.exists():
            return response

        # Usuarios internos siguen entrando normalmente al backend.
        if user.has_group('base.group_user'):
            return response

        # Clientes / portal van a la tienda.
        return request.redirect('/shop')
