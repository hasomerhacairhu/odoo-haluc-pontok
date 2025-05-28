from odoo import models, fields, api
import json

class HalucDashboard(models.Model):
    _name = 'haluc.dashboard'
    _description = 'Háluc Points Dashboard Data'

    name = fields.Char(default="Háluc Points Admin Dashboard", readonly=True)

    top_contributors_html = fields.Html(compute='_compute_dashboard_data', string="Top Contributors")
    points_trends_monthly_chart_json = fields.Text(compute='_compute_dashboard_data', string="Monthly Trends (JSON)")
    total_earned_points = fields.Integer(compute='_compute_dashboard_data', string="Total Points Earned")
    total_spent_points = fields.Integer(compute='_compute_dashboard_data', string="Total Points Spent")
    most_active_categories_html = fields.Html(compute='_compute_dashboard_data', string="Most Active Categories")

    def _compute_dashboard_data(self):
        for record in self:
            record.top_contributors_html = record._get_top_contributors_html()
            record.points_trends_monthly_chart_json = record._get_points_trends_monthly_json()
            earned, spent = record._get_total_earned_vs_spent_values()
            record.total_earned_points = earned
            record.total_spent_points = spent
            record.most_active_categories_html = record._get_most_active_categories_html()

    @api.model
    def _get_top_contributors_html(self, limit=5):
        query = """
            SELECT rp.name, SUM(hpt.points) AS total_points
            FROM haluc_point_transaction hpt
            JOIN res_partner rp ON hpt.partner_id = rp.id
            WHERE hpt.state = 'confirmed' AND hpt.points > 0
            GROUP BY rp.id, rp.name
            ORDER BY total_points DESC
            LIMIT %s;
        """
        self.env.cr.execute(query, (limit,))
        contributors = self.env.cr.dictfetchall()
        if not contributors:
            return "<p>No contributor data available.</p>"

        html = "<ul>"
        for contrib in contributors:
            html += f"<li>{contrib['name']}: {contrib['total_points']} points</li>"
        html += "</ul>"
        return html

    @api.model
    def _get_points_trends_monthly_json(self):
        query_earned = """
            SELECT TO_CHAR(hpt.date, 'YYYY-MM') AS month, SUM(hpt.points) AS monthly_earned
            FROM haluc_point_transaction hpt
            WHERE hpt.state = 'confirmed' AND hpt.points > 0 AND hpt.date IS NOT NULL
            GROUP BY TO_CHAR(hpt.date, 'YYYY-MM')
            ORDER BY month;
        """
        query_spent = """
            SELECT TO_CHAR(hpt.date, 'YYYY-MM') AS month, SUM(ABS(hpt.points)) AS monthly_spent
            FROM haluc_point_transaction hpt
            WHERE hpt.state = 'confirmed' AND hpt.points < 0 AND hpt.date IS NOT NULL
            GROUP BY TO_CHAR(hpt.date, 'YYYY-MM')
            ORDER BY month;
        """
        self.env.cr.execute(query_earned)
        earned_data = self.env.cr.dictfetchall()
        self.env.cr.execute(query_spent)
        spent_data = self.env.cr.dictfetchall()

        labels = sorted(list(set([e['month'] for e in earned_data] + [s['month'] for s in spent_data])))
        earned_map = {e['month']: e['monthly_earned'] for e in earned_data}
        spent_map = {s['month']: s['monthly_spent'] for s in spent_data}

        earned_values = [earned_map.get(m, 0) for m in labels]
        spent_values = [spent_map.get(m, 0) for m in labels]

        chart_data = {
            'labels': labels,
            'datasets': [
                {'label': 'Points Earned', 'data': earned_values, 'backgroundColor': 'rgba(75, 192, 192, 0.2)', 'borderColor': 'rgba(75, 192, 192, 1)', 'fill': 'start'},
                {'label': 'Points Spent', 'data': spent_values, 'backgroundColor': 'rgba(255, 99, 132, 0.2)', 'borderColor': 'rgba(255, 99, 132, 1)', 'fill': 'start'}
            ]
        }
        return json.dumps(chart_data)

    @api.model
    def _get_total_earned_vs_spent_values(self):
        total_earned = self.env['haluc.point.transaction'].search_read(
            [('state', '=', 'confirmed'), ('points', '>', 0)],
            ['points'],
            group_by=[],
        )
        total_spent = self.env['haluc.point.transaction'].search_read(
            [('state', '=', 'confirmed'), ('points', '<', 0)],
            ['points'],
            group_by=[],
        )
        
        earned_sum = sum(t['points'] for t in total_earned if t['points']) if total_earned and total_earned[0].get('points') else 0
        spent_sum = sum(abs(t['points']) for t in total_spent if t['points']) if total_spent and total_spent[0].get('points') else 0
        
        # Fallback to SQL if search_read behaves unexpectedly for SUM, though it should work with read_group
        # For simplicity and directness, using SQL for aggregation is often clearer.
        # Re-implementing with direct SQL for clarity and robustness of SUM:

        query_earned_sum = """
            SELECT SUM(hpt.points)
            FROM haluc_point_transaction hpt
            WHERE hpt.state = 'confirmed' AND hpt.points > 0;
        """
        self.env.cr.execute(query_earned_sum)
        res_earned = self.env.cr.fetchone()
        earned_sum_sql = res_earned[0] if res_earned and res_earned[0] else 0

        query_spent_sum = """
            SELECT SUM(ABS(hpt.points))
            FROM haluc_point_transaction hpt
            WHERE hpt.state = 'confirmed' AND hpt.points < 0;
        """
        self.env.cr.execute(query_spent_sum)
        res_spent = self.env.cr.fetchone()
        spent_sum_sql = res_spent[0] if res_spent and res_spent[0] else 0
        
        return earned_sum_sql, spent_sum_sql

    @api.model
    def _get_most_active_categories_html(self, limit=5):
        query = """
            SELECT hpt.category, SUM(hpt.points) AS total_points
            FROM haluc_point_transaction hpt
            WHERE hpt.state = 'confirmed' AND hpt.points > 0 AND hpt.category IS NOT NULL AND hpt.category != ''
            GROUP BY hpt.category
            ORDER BY total_points DESC
            LIMIT %s;
        """
        self.env.cr.execute(query, (limit,))
        categories = self.env.cr.dictfetchall()
        if not categories:
            return "<p>No category data available.</p>"

        html = "<ul>"
        for cat in categories:
            html += f"<li>{cat['category']}: {cat['total_points']} points</li>"
        html += "</ul>"
        return html

    @api.model
    def action_open_admin_dashboard(self):
        dashboard_record = self.env['haluc.dashboard'].search([], limit=1)
        if not dashboard_record:
            dashboard_record = self.env['haluc.dashboard'].create({})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Admin Dashboard',
            'res_model': 'haluc.dashboard',
            'res_id': dashboard_record.id,
            'view_mode': 'form',
            'view_id': self.env.ref('haluc_points.haluc_dashboard_form_view').id,
            'target': 'current',
        }
