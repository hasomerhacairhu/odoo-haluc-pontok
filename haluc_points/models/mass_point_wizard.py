from odoo import models, fields, api

class HalucPointMassWizard(models.TransientModel):
    _name = 'haluc.point.mass.wizard'
    _description = 'Háluc Points Mass Addition Wizard'

    partner_ids = fields.Many2many('res.partner', string='Madrichim', required=True, domain="[('is_company', '=', False)]") # Assuming madrichim are individuals
    points = fields.Integer(string='Points to Award', required=True)
    name = fields.Char(string="Transaction Description", required=True, help="Common description for all transactions, e.g., 'End of Year Bonus'")
    category = fields.Char(string='Category')
    notes = fields.Text(string='Notes')
    date = fields.Date(string='Transaction Date', required=True, default=fields.Date.today)
    notify = fields.Boolean(string='Notify Madrichim', default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Initial Status', default='confirmed', required=True, help="Initial status for the created transactions.")

    def action_add_points(self):
        self.ensure_one()
        transaction_model = self.env['haluc.point.transaction']
        transactions_created = self.env['haluc.point.transaction']

        if not self.partner_ids:
            raise models.UserError("Please select at least one Madrich.")
        if self.points == 0:
            raise models.UserError("Points to award cannot be zero.")
        
        # Use a more descriptive name if the user doesn't provide one, or make it mandatory.
        # For now, let's assume 'name' field is provided by user.

        for partner in self.partner_ids:
            vals = {
                'name': self.name, # Using the wizard's name field
                'partner_id': partner.id,
                'date': self.date,
                'points': self.points,
                'category': self.category,
                'notes': self.notes,
                'state': self.state, # Use the state selected in the wizard
                'notify': self.notify,
            }
            new_transaction = transaction_model.create(vals)
            transactions_created += new_transaction
            
            # The email notification is handled by the overridden create/write methods of haluc.point.transaction
            # if state is 'confirmed' and notify is True.

        if transactions_created:
            # Optional: Return an action to view the created transactions or simply close the wizard
            action = {
                'type': 'ir.actions.act_window',
                'name': 'Created Point Transactions',
                'res_model': 'haluc.point.transaction',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', transactions_created.ids)],
            }
            # If we want to show a specific message:
            # message = {
            #     'type': 'ir.actions.client',
            #     'tag': 'display_notification',
            #     'params': {
            #         'title': ('Success'),
            #         'message': '%s point transactions created.' % len(transactions_created),
            #         'sticky': False,
            #         'next': action, # Optionally, chain with another action
            #     }
            # }
            # return message
            return action

        return {'type': 'ir.actions.act_window_close'}
