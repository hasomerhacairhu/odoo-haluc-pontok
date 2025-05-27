from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    haluc_point_balance = fields.Integer(
        string="Háluc Point Balance",
        compute='_compute_haluc_point_balance',
        store=True  # Optional: set to True if you want to store the value in the database and allow searching/grouping
    )

    @api.depends('haluc_point_transaction_ids.points', 'haluc_point_transaction_ids.state')
    def _compute_haluc_point_balance(self):
        for partner in self:
            confirmed_transactions = self.env['haluc.point.transaction'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'confirmed')
            ])
            partner.haluc_point_balance = sum(confirmed_transactions.mapped('points'))

    haluc_point_transaction_ids = fields.One2many(
        'haluc.point.transaction',
        'partner_id',
        string="Háluc Point Transactions"
    )