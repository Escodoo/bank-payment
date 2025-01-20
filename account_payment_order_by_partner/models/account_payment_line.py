# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountPaymentLine(models.Model):

    _inherit = "account.payment.line"

    @api.constrains("partner_id", "order_id")
    def _check_partner_consistency(self):
        for line in self:
            if line.order_id.payment_mode_id.individual_payment:
                partners = line.order_id.payment_line_ids.mapped("partner_id")
                if len(set(partners)) > 1:
                    raise ValidationError(
                        _(
                            "The payment order contains lines with multiple partners. "
                            "When the payment mode requires individual payments, "
                            "all lines must belong to the same partner."
                        )
                    )
