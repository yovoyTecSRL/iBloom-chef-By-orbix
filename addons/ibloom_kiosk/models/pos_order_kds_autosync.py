from odoo import api, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------

    def _ibloom_get_pos_config(self):
        self.ensure_one()

        config = self.config_id

        if not config and self.session_id:
            config = self.session_id.config_id

        return config

    def _ibloom_is_gastronomic_pos(self):
        self.ensure_one()

        config = self._ibloom_get_pos_config()

        if not config:
            return False

        name = (config.name or "").strip().lower()

        # Boutique nunca debe ir a cocina.
        if "boutique" in name:
            return False

        return any(
            token in name
            for token in (
                "deli",
                "restaurante",
                "restaurant",
            )
        )

    def _ibloom_initialize_kitchen_state(self):
        """
        Toda orden perteneciente a un POS gastronómico debe
        tener un estado KDS válido.

        No sobrescribe preparing / ready / delivered.
        Solamente inicializa valores vacíos.
        """

        if "ibloom_kitchen_state" not in self._fields:
            return

        for order in self:

            if order.state == "cancel":
                continue

            if not order._ibloom_is_gastronomic_pos():
                continue

            if not order.ibloom_kitchen_state:
                order.with_context(
                    ibloom_skip_kds_autosync=True
                ).write({
                    "ibloom_kitchen_state": "new",
                })

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):

        orders = super().create(vals_list)

        if not self.env.context.get(
            "ibloom_skip_kds_autosync"
        ):
            orders._ibloom_initialize_kitchen_state()

        return orders

    # ----------------------------------------------------------
    # WRITE
    # ----------------------------------------------------------

    def write(self, vals):

        result = super().write(vals)

        if not self.env.context.get(
            "ibloom_skip_kds_autosync"
        ):
            self._ibloom_initialize_kitchen_state()

        return result
