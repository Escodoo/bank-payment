# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):

    _inherit = "account.move"

    def get_account_payment_domain(self, payment_mode):
        domain = super().get_account_payment_domain(payment_mode)
        if payment_mode.individual_payment:
            domain.append(("payment_line_ids.partner_id", "=", self.partner_id.id))
        return domain
