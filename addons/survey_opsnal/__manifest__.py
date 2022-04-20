{
    'name': 'Survey Opsnal',
    'version': '0.1.0',
    'description': 'Survey Bidgasopsnal',
    'author': 'Bari Azhari',
    'website': '',
    'category': 'Survey',
    'depends': [
        'base', 'hr', 'survey'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_views.xml',
        'views/survey_template.xml',
    ],

    'auto_install': False,
    'installable': True,
}