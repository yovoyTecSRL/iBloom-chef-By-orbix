from odoo import http
from odoo.http import request


class IBloomCombosController(http.Controller):

    @http.route(
        "/combos",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def combos(self, **kwargs):

        # Utiliza el buscador nativo de Website Sale.
        # Así no dependemos de un slug fijo.
        return request.redirect(
            "/shop?search=Combo"
        )
