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
        'views/point_transaction_views.xml',
        'views/partner_views.xml',
        'views/portal_templates.xml', # Added portal templates
        'data/demo_data.xml', # To be added in Step 7
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}