from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home


class OrbixLoginRedirectShop(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):

        # Este módulo queda neutralizado para no competir
        # con orbix_portal_shop_redirect.
        return super().web_login(
            redirect=redirect,
            **kw
        )
