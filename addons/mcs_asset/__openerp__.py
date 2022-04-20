# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets',
    'version': '1.10',
    'summary': 'Asset Management',
    'description': """
Managing Assets in Odoo.
===========================
Support following feature:
    * Location for Asset
    * Assign Asset to employee
    * Track warranty information
    * Custom states of Asset
    * States of Asset for different team: Finance, Warehouse, Manufacture, Maintenance and Accounting
    * Drag&Drop manage states of Asset
    * Asset Tags
    * Search by main fields
    """,
    'author': 'Susi',
    'website': 'http://matrica.co.id',
    'category': 'New Module',
    'sequence': 0,
    'depends': ['stock','base','mail'],
#    'demo': ['demo/asset_demo.xml'],
    'data': [
        'security/res_groups.xml',

        'views/asset_view.xml',
        'data/asset_data.xml',
        'views/asset.xml',
        'views/asset_move_view.xml',
        'views/res_partner.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: