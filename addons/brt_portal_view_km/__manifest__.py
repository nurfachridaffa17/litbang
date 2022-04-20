# -*- coding: utf-8 -*-
{
    'name': "BRT Journal Portal",
    'summary': """Show Journal Inportal Website Odoo""",
    'description': """Show Journal Inportal Website Odoo""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        # 'muk_dms',
    ],
    
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        # 'views/jurnal.xml',
        'views/backend/jurnal.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}