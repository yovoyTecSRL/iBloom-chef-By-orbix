from odoo import models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    def action_orbix_create_social_post(self):

        self.ensure_one()

        post = self.env[
            "orbix.social.post"
        ].create_from_product(self)

        return {
            "type": "ir.actions.act_window",
            "name": "Publicación Social",
            "res_model": "orbix.social.post",
            "view_mode": "form",
            "res_id": post.id,
            "target": "current",
        }
