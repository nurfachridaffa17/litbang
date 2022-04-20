# -*- coding: utf-8 -*-
{
    'name'          : "TNDE ",
    'summary'       : """
        Tata Naskah Dinas Elektronik""",
    'description'   : """
        Fungsi dari modul Manajemen tnde ini adalah:
           1. Fungsi pertama
           2. Fungsi kedua
           3. Fungsi ketiga
    """,
    'author'        : "Brata",
    'website'       : "http://www.-.co.id",
	'application'   : False,
    'category'      : 'Uncategorized',
    'version'       : '0.1',
    'depends': ['base','hr'],
    'data': [
        'security/res_group.xml',
        'security/ir.model.access.csv',
        'views/report/lembar_disposisi.xml',
        'views/report/lembar_disposisi_blank.xml',
        'views/pengaturan/kategori_views.xml',
        'data/kategori.xml',
        'data/template_mail_acc_konseptor.xml',
        'data/template_mail_acc_taud.xml',
        'data/template_mail_acc_sespus.xml',
        'data/template_mail_acc_kapus.xml',
        'data/template_mail_surat_masuk.xml',
        'data/template_mail_disposisi.xml',
        'data/template_mail_internal.xml',
        'data/template_mail_tujuan_internal.xml',
        'views/templates.xml',
        'views/menu_transaksi.xml',
        'views/views.xml',
        'views/transaksi/surat_masuk_new.xml',
        'views/transaksi/popup_disposisi_surat_masuk.xml',
        'views/transaksi/surat_keluar.xml',
        'views/transaksi/surat_internal.xml',
        'views/pengaturan/crud_pengaturan_asal_surat.xml',
        'views/pengaturan/kode_klasifikasi.xml',
        'views/pengaturan/kode_primer.xml',
        'views/pengaturan/kode_sekunder.xml',
        'views/pengaturan/kode_tersier.xml',
        'views/pengaturan/bidbag.xml',
        # 'views/inherit_css_backend.xml',
        
    ],
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}