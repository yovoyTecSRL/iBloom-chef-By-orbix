from odoo import api, fields, models, _
from odoo.exceptions import UserError


class OrbixSocialPost(models.Model):

    _name = "orbix.social.post"
    _description = "Publicación Social Orbix"

    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]

    _order = "scheduled_date desc, id desc"

    name = fields.Char(
        string="Título",
        required=True,
        tracking=True,
    )

    product_id = fields.Many2one(
        "product.template",
        string="Producto",
        ondelete="set null",
        tracking=True,
    )

    website_id = fields.Many2one(
        "website",
        string="Website",
        tracking=True,
    )

    account_ids = fields.Many2many(
        "orbix.social.account",
        string="Redes sociales",
    )

    message = fields.Text(
        string="Texto de publicación",
        required=True,
        tracking=True,
    )

    image_1920 = fields.Binary(
        string="Imagen",
        attachment=True,
    )

    link_url = fields.Char(
        string="URL",
    )

    scheduled_date = fields.Datetime(
        string="Fecha programada",
        tracking=True,
    )

    published_date = fields.Datetime(
        string="Fecha publicación",
        readonly=True,
    )

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("approved", "Aprobado"),
            ("scheduled", "Programado"),
            ("published", "Publicado"),
            ("error", "Error"),
        ],
        string="Estado",
        default="draft",
        required=True,
        tracking=True,
    )

    error_message = fields.Text(
        string="Error",
        readonly=True,
    )

    @api.model
    def create_from_product(self, product):

        website = (
            product.website_id
            or self.env["website"].search([], limit=1)
        )

        base_url = ""

        if website and website.domain:
            base_url = website.domain.rstrip("/")

        relative_url = product.website_url or ""

        if base_url and relative_url:
            full_url = base_url + relative_url
        else:
            full_url = relative_url

        description = (
            product.description_sale
            or product.website_description
            or ""
        )

        if "<" in description:
            # texto simple para borrador; el usuario puede editarlo.
            description = _("Descubre esta pieza en Dahian Luxury.")

        currency = product.currency_id.symbol or "₡"

        message = (
            f"✨ {product.name}\n\n"
            f"{description}\n\n"
            f"Precio: {currency}{product.list_price:,.2f}\n"
            f"🛍 {full_url}\n\n"
            f"#DahianLuxury #Joyería #Boutique"
        )

        return self.create({
            "name": product.name,
            "product_id": product.id,
            "website_id": website.id if website else False,
            "message": message,
            "image_1920": product.image_1920,
            "link_url": full_url,
        })

    def action_approve(self):

        self.write({
            "state": "approved",
        })

        return True

    def action_schedule(self):

        for post in self:

            if not post.scheduled_date:
                raise UserError(
                    _("Debes indicar una fecha de publicación.")
                )

            post.state = "scheduled"

        return True

    def action_reset_draft(self):

        self.write({
            "state": "draft",
            "error_message": False,
        })

        return True

    def action_mark_published(self):

        self.write({
            "state": "published",
            "published_date": fields.Datetime.now(),
            "error_message": False,
        })

        return True

    def action_publish(self):

        self.ensure_one()

        if not self.account_ids:
            raise UserError(
                _(
                    "Selecciona al menos una cuenta social. "
                    "La conexión Meta API se agregará en la siguiente fase."
                )
            )

        raise UserError(
            _(
                "El módulo Orbix Social Marketing está instalado "
                "correctamente, pero el conector Meta todavía no está "
                "habilitado. Esta será la siguiente fase."
            )
        )
