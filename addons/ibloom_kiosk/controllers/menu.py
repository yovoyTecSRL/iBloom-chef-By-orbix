from odoo import http
from odoo.http import request


class IBloomMenuController(http.Controller):

    @http.route(
        ["/menu", "/kiosco"],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def menu(self, **kwargs):

        Category = request.env[
            "product.public.category"
        ].sudo()

        Product = request.env[
            "product.template"
        ].sudo()

        root = Category.search(
            [("name", "=", "iBLOOM Deli")],
            limit=1,
        )

        categories = []

        if root:

            children = Category.search(
                [
                    ("id", "child_of", root.id),
                    ("id", "!=", root.id),
                ],
                order="sequence, name",
            )

            for category in children:

                products = Product.search([
                    ("active", "=", True),
                    ("sale_ok", "=", True),
                    (
                        "public_categ_ids",
                        "in",
                        category.id,
                    ),
                ], order="name")

                if not products:
                    continue

                categories.append({
                    "id": category.id,
                    "name": category.name,
                    "products": products,
                })

        return request.render(
            "ibloom_kiosk.menu_preview",
            {
                "categories": categories,
            }
        )
