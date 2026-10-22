{
    "name": "Orbix Social Marketing",
    "version": "19.0.1.0.0",
    "summary": "Marketing social y publicaciones desde productos Odoo Community",
    "description": """
Orbix Social Marketing
======================

Módulo para Odoo 19 Community orientado a:

* Facebook
* Instagram
* LinkedIn
* TikTok
* Publicaciones desde productos
* Calendario y programación
* Plantillas
* Integración futura con Meta Graph API
    """,

    "author": "Sistemas Orbix",
    "website": "https://sistemasorbix.com",

    "category": "Marketing",

    "license": "LGPL-3",

    "depends": [
        "base",
        "mail",
        "product",
        "website",
        "website_sale",
        "sale_management",
    ],

    "data": [
        "security/orbix_social_security.xml",
        "security/ir.model.access.csv",

        "views/orbix_social_account_views.xml",
        "views/orbix_social_template_views.xml",
        "views/orbix_social_post_views.xml",
        "views/product_template_views.xml",
        "views/orbix_social_menu.xml",
    ],

    "application": True,
    "installable": True,
    "auto_install": False,
}
