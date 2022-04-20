# -*- coding: utf-8 -*-
{
    'name': "sim_rikwastu",

    'summary': """ - """,

    'description': """ - """,

    'author': "Puslitbang ",
    'website': "http://puslitbang.polri.go.id ",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/rikwastu_menu.xml',
        'views/perencanaan_views.xml',
        'views/master_flow_views.xml',
        'views/pelaksanaan_views.xml',
        'views/langkah_kerja_views.xml',
        'views/views.xml',
        'views/templates.xml',
#         'views/menu.xml',
        'views/master_data/template_surat.xml',
        'views/program/program.xml',
        'views/program/tahapperencanaan.xml',
        'views/finalisai_views.xml',
        'views/dokumen_finalisai_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}