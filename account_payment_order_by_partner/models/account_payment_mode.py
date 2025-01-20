# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPaymentMode(models.Model):

    _inherit = "account.payment.mode"
    individual_payment = fields.Boolean(
        string="Individual Payment per Partner",
        help="Enable this option to process payments individually"
        " for this partner instead of combining them in a single payment order.",
    )
