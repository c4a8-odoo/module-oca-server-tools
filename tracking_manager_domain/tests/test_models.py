# Copyright 2025 glueckkanja AG (<https://www.glueckkanja.com>) - Christopher Rogos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import TransactionCase


class TestMailTrack(TransactionCase):
    def setUp(self):
        super().setUp()

        self.Field = self.env["ir.model.fields"]
        self.field_phone = self.Field.search(
            [("model", "=", "res.partner"), ("name", "=", "phone")], limit=1
        )
        self.field_phone.write({"tracking_domain": "[('is_company', '=', True)]"})

    def test_mail_track(self):
        # arrange
        company = self.env.ref("base.main_partner")
        tracked_fields = {"phone": {"string": "Phone", "type": "char"}}
        initial_values = {"phone": "1234"}

        # act
        changes, tracking_value_ids = company._mail_track(
            tracked_fields, initial_values
        )

        # assert
        # Check if changes and tracking_value_ids are returned correctly
        self.assertEqual(len(changes), 1)
        self.assertEqual(len(tracking_value_ids), 1)

        # Check if the field is tracked correctly
        tracking_value = tracking_value_ids[0][2]
        self.assertEqual(tracking_value["field_id"], self.field_phone.id)

    def test_mail_track_with_non_matching_domain(self):
        # arrange
        person = self.env.ref("base.partner_admin")

        tracked_fields = {"phone": {"string": "Phone", "type": "char"}}
        initial_values = {"phone": "1234"}

        # act
        changes, tracking_value_ids = person._mail_track(tracked_fields, initial_values)

        # assert
        # Check if changes and tracking_value_ids are empty when domain does not match
        self.assertEqual(len(changes), 0)
        self.assertEqual(len(tracking_value_ids), 0)
