from odoo import models, fields

class HalucPointTransaction(models.Model):
    _name = 'haluc.point.transaction'
    _description = 'Háluc Point Transaction'

    name = fields.Char(string='Description', required=True)
    partner_id = fields.Many2one('res.partner', string='Madrich', required=True)
    date = fields.Date(string='Transaction Date', required=True, default=fields.Date.today)
    points = fields.Integer(string='Points', required=True)
    category = fields.Char(string='Category')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft', required=True)
    notify = fields.Boolean(string='Notify Madrich', default=False) # New field

    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'confirmed'
        return True