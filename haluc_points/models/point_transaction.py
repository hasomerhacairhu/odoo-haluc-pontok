from odoo import models, fields, api

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
                # Call write with {'state': 'confirmed'} to trigger the overridden write method
                rec.write({'state': 'confirmed'})
        return True

    @api.model
    def create(self, vals):
        record = super(HalucPointTransaction, self).create(vals)
        if record.state == 'confirmed' and record.notify and record.points > 0:
            self._send_notification_email(record)
        return record

    def write(self, vals):
        # Track state changes before the write
        old_states = {rec: rec.state for rec in self}
        res = super(HalucPointTransaction, self).write(vals)
        for rec in self:
            # Check if state changed to 'confirmed' in this write operation
            if vals.get('state') == 'confirmed' and old_states.get(rec) != 'confirmed':
                if rec.notify and rec.points > 0: # Assuming positive points are "earn" transactions
                    self._send_notification_email(rec)
            # If only notify is set to true on an already confirmed transaction
            elif vals.get('notify') is True and rec.state == 'confirmed' and rec.points > 0:
                self._send_notification_email(rec)
        return res

    def _send_notification_email(self, transaction_record):
        self.ensure_one() # Ensure we are working with a single record
        template = self.env.ref('haluc_points.email_template_haluc_point_notification', raise_if_not_found=False)
        if template:
            template.send_mail(transaction_record.id, force_send=True)