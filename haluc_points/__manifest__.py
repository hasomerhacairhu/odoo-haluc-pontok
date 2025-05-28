{
    'name': "Háluc Points Management",
    'summary': """
        Module to track and manage Háluc Points for Hasomer Hacair madrichim.
    """,
    'description': """
        This module allows logging point transactions (additions and spending),
        calculates current point balances per madrich, displays points in the
        madrich’s profile, and restricts editing access.
    """,
    'author': "Hasomer Hacair Magyarország", # Please replace with actual author
    'website': "somer.hu", # Please replace
    'category': 'Uncategorized', # Or a more specific category like 'HR' or 'Customizations'
    'version': '1.0',
    'depends': ['base', 'mail', 'portal'], # Added portal dependency
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml', # Added security.xml
        'data/mail_template_data.xml',
        'data/demo_data.xml',
        'views/point_transaction_views.xml',
        'views/partner_views.xml',
        'views/portal_templates.xml',
        'views/dashboard_views.xml',  # Added dashboard views
        'views/mass_point_wizard_views.xml',  # Added mass point wizard views
    ],
    'assets': {
        'web.assets_backend': [
            'haluc_points/static/src/js/haluc_chart_widget.js',
            'haluc_points/static/src/xml/haluc_chart_widget.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js', # Added Chart.js
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}