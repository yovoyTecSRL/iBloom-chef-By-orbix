from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ibloom_kitchen_state = fields.Selection(
        [
            ("new", "Nuevo"),
            ("preparing", "Preparando"),
            ("ready", "Listo"),
            ("delivered", "Entregado"),
            ("cancelled", "Cancelado"),
        ],
        string="Estado Cocina iBLOOM",
        default="new",
        copy=False,
        index=True,
    )

    ibloom_order_mode = fields.Selection(
        [
            ("here", "Comer aquí"),
            ("takeaway", "Para llevar"),
        ],
        string="Modalidad iBLOOM",
        default="here",
        copy=False,
    )
