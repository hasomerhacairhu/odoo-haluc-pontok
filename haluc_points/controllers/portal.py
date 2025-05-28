from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class HalucPointsCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'haluc_points_count' in counters:
            partner = request.env.user.partner_id
            values['haluc_points_count'] = request.env['haluc.point.transaction'].search_count([
                ('partner_id', '=', partner.id),
                ('state', '=', 'confirmed')
            ])
            values['haluc_point_balance'] = partner.haluc_point_balance
            values['haluc_motivational_status'] = partner.haluc_motivational_status # Added motivational status
            # For the home page, we might not need last_5_transactions, but it could be added if desired.
            # For now, focusing on the dedicated points page for last 5 transactions.
        return values

    @http.route(['/my/haluc_points', '/my/haluc_points/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_haluc_points(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        partner = request.env.user.partner_id
        HalucPointTransaction = request.env['haluc.point.transaction']

        domain = [('partner_id', '=', partner.id)]

        # For now, only show confirmed transactions in portal, can be adjusted
        domain.append(('state', '=', 'confirmed'))

        searchbar_sortings = {
            'date': {'label': 'Transaction Date', 'order': 'date desc'},
            'name': {'label': 'Description', 'order': 'name asc'},
            'points': {'label': 'Points', 'order': 'points desc'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # count for pager
        transaction_count = HalucPointTransaction.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/haluc_points",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=transaction_count,
            page=page,
            step=self._items_per_page
        )

        transactions = HalucPointTransaction.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )

        values = self._prepare_portal_layout_values()
        values.update({
            'transactions': transactions,
            'page_name': 'haluc_points',
            'pager': pager,
            'default_url': '/my/haluc_points',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'haluc_point_balance': partner.haluc_point_balance, # Get balance from partner
            'haluc_motivational_status': partner.haluc_motivational_status, # Added motivational status
            'last_5_transactions': partner.get_last_n_transactions(5), # Added last 5 transactions
        })
        return request.render("haluc_points.portal_my_haluc_points_list", values)
