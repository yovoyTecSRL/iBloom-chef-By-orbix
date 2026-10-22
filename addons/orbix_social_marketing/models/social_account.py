from odoo import fields, models


class OrbixSocialAccount(models.Model):

    _name = "orbix.social.account"
    _description = "Cuenta Social Orbix"
    _order = "platform, name"

    name = fields.Char(
        string="Nombre",
        required=True,
    )

    active = fields.Boolean(
        default=True,
    )

    platform = fields.Selection(
        [
            ("facebook", "Facebook"),
            ("instagram", "Instagram"),
            ("linkedin", "LinkedIn"),
            ("tiktok", "TikTok"),
        ],
        string="Plataforma",
        required=True,
    )

    page_id = fields.Char(
        string="Page ID",
    )

    instagram_account_id = fields.Char(
        string="Instagram Business Account ID",
    )

    access_token = fields.Char(
        string="Access Token",
        groups="orbix_social_marketing.group_orbix_social_manager",
    )

    notes = fields.Text(
        string="Notas",
    )
