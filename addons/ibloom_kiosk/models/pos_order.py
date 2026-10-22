from odoo import fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    ibloom_kitchen_state = fields.Selection(
        selection=[
            ("new", "Recepción"),
            ("preparing", "Preparando"),
            ("ready", "Listo"),
            ("delivered", "Entregado"),
        ],
        string="Estado Cocina iBLOOM",
        default="new",
        copy=False,
        index=True,
    )
