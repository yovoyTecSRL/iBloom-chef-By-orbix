import json
from datetime import datetime

from odoo import http
from odoo.http import request


class IBloomKitchenController(http.Controller):

    def _get_orders(self):

        Order = request.env["sale.order"].sudo()

        orders = Order.search(
            [
                ("website_id", "!=", False),
                ("state", "in", ["sale", "done"]),
                (
                    "ibloom_kitchen_state",
                    "in",
                    ["new", "preparing", "ready"],
                ),
            ],
            order="date_order asc, id asc",
            limit=100,
        )

        now = datetime.utcnow()

        result = []

        for order in orders:

            lines = []

            for line in order.order_line:

                if line.display_type:
                    continue

                if not line.product_id:
                    continue

                lines.append({
                    "name": line.product_id.display_name,
                    "qty": line.product_uom_qty,
                })

            elapsed = 0

            if order.date_order:

                try:
                    elapsed = max(
                        0,
                        int(
                            (
                                now - order.date_order
                            ).total_seconds() / 60
                        ),
                    )
                except Exception:
                    elapsed = 0

            result.append({
                "id": order.id,
                "name": order.name,
                "state": (
                    order.ibloom_kitchen_state
                    or "new"
                ),
                "mode": (
                    order.ibloom_order_mode
                    or "here"
                ),
                "time": (
                    order.date_order.strftime("%H:%M")
                    if order.date_order
                    else ""
                ),
                "elapsed": elapsed,
                "partner": (
                    order.partner_id.name
                    if order.partner_id
                    else ""
                ),
                "reference": (
                    order.client_order_ref
                    or ""
                ),
                "lines": lines,
            })

        return result


    @http.route(
        "/cocina",
        type="http",
        auth="user",
        website=True,
        sitemap=False,
    )
    def kitchen(self, **kwargs):

        orders = self._get_orders()

        counts = {
            "new": 0,
            "preparing": 0,
            "ready": 0,
        }

        for order in orders:

            if order["state"] in counts:
                counts[order["state"]] += 1

        return request.render(
            "ibloom_kiosk.kitchen_page",
            {
                "kitchen_orders": orders,
                "kitchen_counts": counts,
            }
        )


    @http.route(
        "/ibloom/kitchen/orders",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def kitchen_orders(self, **kwargs):

        response = request.make_json_response({
            "ok": True,
            "orders": self._get_orders(),
        })

        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )

        return response


    @http.route(
        "/ibloom/kitchen/state",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def kitchen_state(self, **kwargs):

        try:

            payload = json.loads(
                request.httprequest.data.decode("utf-8")
            )

            order_id = int(
                payload.get("order_id")
            )

            state = payload.get("state")

        except Exception:

            return request.make_json_response(
                {
                    "ok": False,
                    "error": "Solicitud inválida",
                },
                status=400,
            )

        allowed = {
            "new",
            "preparing",
            "ready",
            "delivered",
            "cancelled",
        }

        if state not in allowed:

            return request.make_json_response(
                {
                    "ok": False,
                    "error": "Estado inválido",
                },
                status=400,
            )

        order = request.env[
            "sale.order"
        ].sudo().browse(
            order_id
        ).exists()

        if not order:

            return request.make_json_response(
                {
                    "ok": False,
                    "error": "Pedido no encontrado",
                },
                status=404,
            )

        # IMPORTANTE:
        # El estado del inventario NO se valida aquí.
        # Cocina procesa el pedido aun con stock 0.
        order.write({
            "ibloom_kitchen_state": state,
        })

        return request.make_json_response({
            "ok": True,
            "order": order.name,
            "state": state,
        })


    @http.route(
        "/ibloom/kitchen/history",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def kitchen_history(self, **kwargs):

        orders = request.env[
            "sale.order"
        ].sudo().search(
            [
                ("website_id", "!=", False),
                (
                    "ibloom_kitchen_state",
                    "=",
                    "delivered",
                ),
            ],
            order="id desc",
            limit=30,
        )

        data = []

        for order in orders:

            data.append({
                "id": order.id,
                "name": order.name,
                "time": (
                    order.date_order.strftime("%H:%M")
                    if order.date_order
                    else ""
                ),
            })

        return request.make_json_response({
            "ok": True,
            "orders": data,
        })
