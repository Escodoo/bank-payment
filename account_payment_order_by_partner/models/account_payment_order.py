# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):

    _inherit = "account.payment.order"

    def draft2open(self):
        for order in self:
            if order.payment_mode_id.individual_payment:
                partners = order.payment_line_ids.mapped("partner_id")
                if len(set(partners.ids)) > 1:
                    raise UserError(
                        _(
                            "The Payment Mode '%s' requires individual payments. "
                            "Ensure that all payment lines belong to the same partner."
                        )
                        % order.payment_mode_id.name
                    )
        super().draft2open()
