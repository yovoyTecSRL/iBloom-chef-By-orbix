from odoo import api, fields, models


class IBloomKioskOrder(models.Model):
    _name = "ibloom.kiosk.order"
    _description = "Pedido Kiosco iBLOOM"
    _order = "id desc"

    name = fields.Char(
        string="Pedido",
        default="Nuevo",
        readonly=True,
        copy=False,
    )

    state = fields.Selection(
        [
            ("new", "Nuevo"),
            ("preparing", "Preparando"),
            ("ready", "Listo"),
            ("delivered", "Entregado"),
            ("cancelled", "Cancelado"),
        ],
        default="new",
        required=True,
        index=True,
    )

    order_mode = fields.Selection(
        [
            ("here", "Comer aquí"),
            ("takeaway", "Para llevar"),
        ],
        default="here",
        required=True,
    )

    payment_mode = fields.Selection(
        [
            ("counter", "Pagar en caja"),
            ("cash", "Efectivo en caja"),
            ("sinpe", "SINPE en caja"),
        ],
        default="counter",
        required=True,
    )

    line_ids = fields.One2many(
        "ibloom.kiosk.order.line",
        "order_id",
        string="Productos",
    )

    amount_total = fields.Monetary(
        compute="_compute_amount_total",
        store=True,
    )

    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    note = fields.Text(string="Observaciones")

    create_date = fields.Datetime(
        string="Hora del pedido",
        readonly=True,
    )

    @api.depends("line_ids.subtotal")
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(
                order.line_ids.mapped("subtotal")
            )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            if record.name == "Nuevo":
                record.name = (
                    self.env["ir.sequence"]
                    .next_by_code("ibloom.kiosk.order")
                    or f"K-{record.id:04d}"
                )

        return records


class IBloomKioskOrderLine(models.Model):
    _name = "ibloom.kiosk.order.line"
    _description = "Línea Pedido Kiosco iBLOOM"

    order_id = fields.Many2one(
        "ibloom.kiosk.order",
        required=True,
        ondelete="cascade",
    )

    product_id = fields.Many2one(
        "product.product",
        required=True,
    )

    product_name = fields.Char(
        related="product_id.name",
        store=True,
    )

    qty = fields.Float(
        default=1.0,
        required=True,
    )

    price_unit = fields.Monetary(
        required=True,
    )

    currency_id = fields.Many2one(
        related="order_id.currency_id",
        store=True,
    )

    subtotal = fields.Monetary(
        compute="_compute_subtotal",
        store=True,
    )

    @api.depends("qty", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.price_unit
