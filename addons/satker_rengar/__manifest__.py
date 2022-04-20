# -*- coding: utf-8 -*-

{
    'name': 'Perencanaan, Anggaran dan Realisasi - Satker',
    'version': '1.0',
    'license': 'Other proprietary',
    'category': 'Human Resources',
    'summary': 'Perencanaan, Anggaran dan Realisasi - Satuan Kerja',
    'description': """
        Kertas Kerja Requests:
        Expense Advance Request - Employee
        """,
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.jpg'],
    'author': 'Matrica Consulting Services., Ibrahim',
    'website': 'www.matrica.co.id',
    'depends': ['hr_expense'],
    'data': [
             'data/expense_sequence_data.xml',
             'data/groups.xml',
             'security/satker_rengar_security.xml',
             'security/ir.model.access.csv',
             'views/head_kertas_kerja.xml',
             'views/head_kertas_kerja_realisasi.xml',
             'views/kertas_kerja.xml',
             'views/hr_expense.xml',
             'views/product_category.xml',
             'views/advance_expense_sheet.xml',
             'views/advance_expense_line.xml',
             'views/advance_expense_line_realisasi.xml',
             'views/rengar_program.xml',
             'views/rengar_kegiatan.xml',
             'views/rengar_output.xml',
             'views/rengar_suboutput.xml',
             'views/rengar_komponen.xml',
             'views/rengar_subkomponen.xml',
             'views/rengar_detail1.xml',
             'views/rengar_detail2.xml',
             'views/rengar_detail3.xml',
             'views/menu_view.xml',
             'report/kertas_kerja_report.xml',
             'report/head_kertas_kerja_report.xml',
             'report/advance_expense_line_report.xml',
             'views/head_kertas_kerja_inherit.xml',
             'wizard/print_xlsx_wizard.xml',
            ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
