from odoo import fields, models


class OrbixSocialTemplate(models.Model):

    _name = "orbix.social.template"
    _description = "Plantilla Social Orbix"
    _order = "name"

    name = fields.Char(
        string="Nombre",
        required=True,
    )

    active = fields.Boolean(
        default=True,
    )

    platform = fields.Selection(
        [
            ("all", "Todas"),
            ("facebook", "Facebook"),
            ("instagram", "Instagram"),
            ("linkedin", "LinkedIn"),
            ("tiktok", "TikTok"),
        ],
        default="all",
        required=True,
    )

    body = fields.Text(
        string="Plantilla",
        required=True,
        default=(
            "✨ {product_name}\n\n"
            "{description}\n\n"
            "Precio: {price}\n"
            "🛍 {url}\n\n"
            "#DahianLuxury"
        ),
    )
