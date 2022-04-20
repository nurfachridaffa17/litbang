# -*- coding: utf-8 -*-
{
    'name': 'Web Extend Database Manager Layout',
    'summary': 'Web Extend Database Manager Layout',
    'author': 'ERP Team Shollu Phillein Technology',
    'website': 'https://www.solu.co.id',
    'category': 'web',
    'version': '10',
    'depends': [
        'web'
    ],
    'data': [
        'views/web_template.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'qweb': [
        'static/src/xml/dashboard_setting.xml',
        'static/src/xml/user_menu_dropdown.xml'
    ],
    'installable': True,
    'auto_install': False,
}
