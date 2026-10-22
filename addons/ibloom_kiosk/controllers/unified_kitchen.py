from odoo import http
from odoo.http import request


class IBloomUnifiedKitchen(http.Controller):

    # ---------------------------------------------------------
    # COMPATIBILIDAD /menu.html
    # ---------------------------------------------------------

    @http.route(
        "/menu.html",
        type="http",
        auth="public",
        website=True,
        methods=["GET"],
    )
    def menu_html_alias(self, **kwargs):

        return request.redirect("/menu")


    # ---------------------------------------------------------
    # API KDS UNIFICADA
    # ---------------------------------------------------------

    @http.route(
        "/ibloom/kitchen/all-orders",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def all_orders(self, **kwargs):

        SaleOrder = request.env["sale.order"].sudo()
        PosOrder = request.env["pos.order"].sudo()

        result = []

        # =====================================================
        # ECOMMERCE / SALE.ORDER
        # =====================================================

        sale_orders = SaleOrder.search(
            [
                ("state", "in", ["sale", "done"]),
                (
                    "ibloom_kitchen_state",
                    "in",
                    [
                        "new",
                        "preparing",
                        "ready",
                    ],
                ),
            ],
            order="date_order asc, id asc",
            limit=300,
        )

        for order in sale_orders:

            lines = []

            for line in order.order_line:

                product = line.product_id

                if not product:
                    continue

                # ---------------------------------------------
                # No mandar delivery como producto de cocina
                # ---------------------------------------------

                default_code = (
                    product.default_code
                    or ""
                )

                if default_code.lower().startswith(
                    "delivery"
                ):
                    continue

                name = product.display_name or ""

                if (
                    "envío estándar" in name.lower()
                    or
                    "envio estándar" in name.lower()
                    or
                    "envio estandar" in name.lower()
                ):
                    continue

                lines.append({
                    "product_id": product.id,
                    "name": name,
                    "qty": line.product_uom_qty,
                })

            if not lines:
                continue

            result.append({
                "source": "sale",
                "source_label": "eCommerce / Web",
                "id": order.id,
                "reference": order.name,
                "state": (
                    order.ibloom_kitchen_state
                    or "new"
                ),
                "customer": (
                    order.partner_id.name
                    if order.partner_id
                    else ""
                ),
                "date_order": str(
                    order.date_order or ""
                ),
                "total": order.amount_total,
                "lines": lines,
            })


        # =====================================================
        # POS DELI / RESTAURANTE
        # =====================================================

        pos_orders = PosOrder.search(
            [
                (
                    "state",
                    "not in",
                    ["cancel"],
                ),
            ],
            order="date_order asc, id asc",
            limit=300,
        )

        for order in pos_orders:

            config = None

            if (
                "config_id" in order._fields
                and order.config_id
            ):
                config = order.config_id

            elif (
                order.session_id
                and order.session_id.config_id
            ):
                config = order.session_id.config_id

            if not config:
                continue

            config_name = (
                config.name
                or ""
            )

            normalized_name = (
                config_name
                .strip()
                .lower()
            )

            # ---------------------------------------------
            # Boutique NUNCA entra a cocina
            # ---------------------------------------------

            if "boutique" in normalized_name:
                continue

            # ---------------------------------------------
            # Sólo puntos gastronómicos
            # ---------------------------------------------

            if not (
                "deli" in normalized_name
                or
                "restaurante" in normalized_name
                or
                "restaurant" in normalized_name
            ):
                continue

            state = (
                order.ibloom_kitchen_state
                or "new"
            )

            # ---------------------------------------------
            # Ocultar entregados/finalizados
            # ---------------------------------------------

            if state in (
                "delivered",
                "done",
            ):
                continue

            lines = []

            for line in order.lines:

                product = line.product_id

                if not product:
                    continue

                lines.append({
                    "product_id": product.id,
                    "name": (
                        product.display_name
                        or ""
                    ),
                    "qty": line.qty,
                })

            if not lines:
                continue

            reference = (
                order.name
                if order.name
                and order.name != "/"
                else f"POS-{order.id}"
            )

            result.append({
                "source": "pos",
                "source_label": config_name,
                "id": order.id,
                "reference": reference,
                "state": state,
                "customer": (
                    order.partner_id.name
                    if order.partner_id
                    else ""
                ),
                "date_order": str(
                    order.date_order or ""
                ),
                "total": order.amount_total,
                "lines": lines,
            })


        # =====================================================
        # ORDEN GLOBAL
        # =====================================================

        result.sort(
            key=lambda x: (
                x.get("date_order") or "",
                x.get("source") or "",
                x.get("id") or 0,
            )
        )

        summary = {
            "sale": 0,
            "pos": 0,
            "new": 0,
            "preparing": 0,
            "ready": 0,
        }

        for item in result:

            source = item.get("source")

            if source in summary:
                summary[source] += 1

            state = item.get("state")

            if state in summary:
                summary[state] += 1

        return {
            "ok": True,
            "count": len(result),
            "summary": summary,
            "orders": result,
        }
