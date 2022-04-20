# -*- coding: utf-8 -*-
{
    'name': "E-Literatur",

    'summary': """Show E-Literatur Inportal Website Odoo""",

    'description': """
       Show E-Literatur Inportal Website Odoo
    """,

    'author': 'Ryan - Matrica Consulting',
    'depends': ['base','vit_kelurahan'],
    'website': 'http://www.matrica.co.id',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        'views/eliteratur.xml',
        'views/backend/eliteratur.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}