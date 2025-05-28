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

    haluc_motivational_status = fields.Char(
        string="Motivational Status",
        compute='_compute_haluc_motivational_status',
        store=False # No need to store, purely display
    )

    @api.depends('haluc_point_balance')
    def _compute_haluc_motivational_status(self):
        for partner in self:
            balance = partner.haluc_point_balance
            if balance > 200:
                partner.haluc_motivational_status = "Point Guru ✨"
            elif balance > 100:
                partner.haluc_motivational_status = "Active Contributor 👍"
            elif balance > 50:
                partner.haluc_motivational_status = "Rising Star ⭐"
            elif balance > 0:
                partner.haluc_motivational_status = "Getting Started 🌱"
            else:
                partner.haluc_motivational_status = "Ready to Earn! 💪"

    def get_last_n_transactions(self, n=5):
        self.ensure_one()
        return self.env['haluc.point.transaction'].search([
            ('partner_id', '=', self.id),
            ('state', '=', 'confirmed')
        ], order='date desc, id desc', limit=n)