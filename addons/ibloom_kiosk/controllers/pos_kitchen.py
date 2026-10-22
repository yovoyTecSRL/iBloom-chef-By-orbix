import json
from datetime import timedelta

from odoo import fields, http
from odoo.http import request


DELI_CONFIG_ID = 3

VALID_STATES = {
    "new",
    "preparing",
    "ready",
    "delivered",
}


class IBloomPosKitchenController(http.Controller):

    def _serialize_order(self, order):
        """Convierte un pos.order Deli al formato requerido por cocina."""

        lines = []

        for line in order.lines:
            if line.qty <= 0:
                continue

            product_name = (
                line.full_product_name
                or line.product_id.display_name
                or "Producto"
            )

            note_parts = []

            if line.customer_note:
                note_parts.append(line.customer_note)

            if line.note:
                note_parts.append(line.note)

            lines.append({
                "id": line.id,
                "name": product_name,
                "qty": line.qty,
                "note": " · ".join(note_parts),
            })

        table_number = ""

        if order.table_id:
            table_number = str(
                order.table_id.table_number or ""
            )

        if order.name and order.name != "/":
            display_name = order.name
        else:
            display_name = "POS #%s" % order.id

        local_date = ""

        if order.date_order:
            local_dt = fields.Datetime.context_timestamp(
                request.env.user,
                order.date_order,
            )

            local_date = local_dt.strftime("%H:%M")

        state = (
            order.ibloom_kitchen_state
            or "new"
        )

        return {
            "id": order.id,
            "source": "pos",
            "key": "pos:%s" % order.id,
            "name": display_name,
            "state": state,
            "time": local_date,
            "table": table_number,
            "table_label": (
                "Mesa %s" % table_number
                if table_number
                else "POS Deli"
            ),
            "order_mode": (
                "dine_in"
                if table_number
                else "takeaway"
            ),
            "lines": lines,
            "amount_total": order.amount_total,
            "pos_state": order.state,
        }

    @http.route(
        "/ibloom/pos-kitchen/orders",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def pos_kitchen_orders(self, **kwargs):

        # Ventana de seguridad:
        # evita revivir pedidos antiguos nunca procesados.
        date_from = (
            fields.Datetime.now()
            - timedelta(hours=24)
        )

        orders = request.env[
            "pos.order"
        ].sudo().search(
            [
                ("config_id", "=", DELI_CONFIG_ID),
                ("state", "!=", "cancel"),
                ("date_order", ">=", date_from),
            ],
            order="date_order asc, id asc",
            limit=200,
        )

        data = []

        for order in orders:

            # Pedido ya terminado en cocina.
            if (
                order.ibloom_kitchen_state
                == "delivered"
            ):
                continue

            # Ignorar pedidos sin productos positivos.
            positive_lines = order.lines.filtered(
                lambda line: line.qty > 0
            )

            if not positive_lines:
                continue

            data.append(
                self._serialize_order(order)
            )

        return request.make_json_response({
            "ok": True,
            "orders": data,
        })

    @http.route(
        "/ibloom/pos-kitchen/state",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def pos_kitchen_state(self, **kwargs):

        try:
            payload = json.loads(
                request.httprequest.data
                or b"{}"
            )
        except Exception:
            return request.make_json_response(
                {
                    "ok": False,
                    "error": "JSON inválido",
                },
                status=400,
            )

        try:
            order_id = int(
                payload.get("order_id")
            )
        except Exception:
            return request.make_json_response(
                {
                    "ok": False,
                    "error": "order_id inválido",
                },
                status=400,
            )

        state = payload.get("state")

        if state not in VALID_STATES:
            return request.make_json_response(
                {
                    "ok": False,
                    "error": "Estado inválido",
                },
                status=400,
            )

        order = request.env[
            "pos.order"
        ].sudo().browse(order_id)

        if not order.exists():
            return request.make_json_response(
                {
                    "ok": False,
                    "error": "Orden POS inexistente",
                },
                status=404,
            )

        if order.config_id.id != DELI_CONFIG_ID:
            return request.make_json_response(
                {
                    "ok": False,
                    "error": (
                        "Esta orden no pertenece "
                        "al POS Deli"
                    ),
                },
                status=403,
            )

        if order.state == "cancel":
            return request.make_json_response(
                {
                    "ok": False,
                    "error": "La orden fue cancelada",
                },
                status=409,
            )

        order.write({
            "ibloom_kitchen_state": state,
        })

        return request.make_json_response({
            "ok": True,
            "order_id": order.id,
            "state": state,
        })
