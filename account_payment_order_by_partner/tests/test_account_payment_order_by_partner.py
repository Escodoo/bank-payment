# Copyright 2025 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import tagged

from odoo.addons.account_payment_order.tests.test_payment_order_inbound import (
    TestPaymentOrderInboundBase,
)


@tagged("post_install", "-at_install")
class TestPaymentOrderByPartner(TestPaymentOrderInboundBase):
    def test_partner_consistency_flag_true(self):
        self.inbound_order.payment_mode_id.individual_payment = True

        # Create the first payment line with the existing partner
        self.env["account.payment.line"].create(
            {
                "partner_id": self.partner.id,
                "amount_currency": 100.0,
                "currency_id": self.company_data["currency"].id,
                "order_id": self.inbound_order.id,
                "name": "Payment for Partner",
                "communication": "Invoice #001",
            }
        )

        # Attempt to add a second line with a different partner
        another_partner = self.env["res.partner"].create({"name": "Another Partner"})
        with self.assertRaises(ValidationError):
            self.env["account.payment.line"].create(
                {
                    "partner_id": another_partner.id,
                    "amount_currency": 50.0,
                    "currency_id": self.company_data["currency"].id,
                    "order_id": self.inbound_order.id,
                    "name": "Payment for Another Partner",
                    "communication": "Invoice #002",
                }
            )

    def test_partner_consistency_flag_false(self):
        self.inbound_order.payment_mode_id.individual_payment = False

        # Clear any existing payment lines in the order
        self.inbound_order.payment_line_ids.unlink()

        # Create the first payment line with the existing partner
        self.env["account.payment.line"].create(
            {
                "partner_id": self.partner.id,
                "amount_currency": 100.0,
                "currency_id": self.company_data["currency"].id,
                "order_id": self.inbound_order.id,
                "name": "Payment for Partner",
                "communication": "Invoice #001",
            }
        )

        # Add a second line with a different partner
        another_partner = self.env["res.partner"].create({"name": "Another Partner"})
        self.env["account.payment.line"].create(
            {
                "partner_id": another_partner.id,
                "amount_currency": 50.0,
                "currency_id": self.company_data["currency"].id,
                "order_id": self.inbound_order.id,
                "name": "Payment for Another Partner",
                "communication": "Invoice #002",
            }
        )

        # Assert that both lines are present
        self.assertEqual(len(self.inbound_order.payment_line_ids), 2)

    def test_draft2open_individual_payment_invalid(self):
        self.inbound_order.payment_mode_id.individual_payment = True

        self.env["account.payment.line"].create(
            {
                "partner_id": self.partner.id,
                "amount_currency": 100.0,
                "currency_id": self.company_data["currency"].id,
                "order_id": self.inbound_order.id,
                "name": "Payment for Partner",
                "communication": "Invoice #001",
            }
        )

        another_partner = self.env["res.partner"].create({"name": "Another Partner"})
        with self.assertRaises(ValidationError):
            self.env["account.payment.line"].create(
                {
                    "partner_id": another_partner.id,
                    "amount_currency": 50.0,
                    "currency_id": self.company_data["currency"].id,
                    "order_id": self.inbound_order.id,
                    "name": "Payment for Another Partner",
                    "communication": "Invoice #002",
                }
            )

        with self.assertRaises(UserError):
            self.inbound_order.draft2open()

    def test_draft2open_multiple_partners_allowed(self):
        self.inbound_order.payment_mode_id.individual_payment = False

        # Create payment lines for multiple partners
        self.env["account.payment.line"].create(
            {
                "partner_id": self.partner.id,
                "amount_currency": 100.0,
                "currency_id": self.company_data["currency"].id,
                "order_id": self.inbound_order.id,
                "name": "Payment for Partner",
                "communication": "Invoice #001",
            }
        )
        another_partner = self.env["res.partner"].create({"name": "Another Partner"})
        self.env["account.payment.line"].create(
            {
                "partner_id": another_partner.id,
                "amount_currency": 50.0,
                "currency_id": self.company_data["currency"].id,
                "order_id": self.inbound_order.id,
                "name": "Payment for Another Partner",
                "communication": "Invoice #002",
            }
        )

        # Attempt to change the order state to open
        self.inbound_order.draft2open()
        self.assertEqual(self.inbound_order.state, "open")
