from openerp import models, fields, api
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class survey_ujicoba(models.Model):
    _name = "survey.ujicoba"
    _description = "Survey Uji Coba"
    _rec_name	= 'name'


    name 				= fields.Char('Nama')

    tanggal_uji			= fields.Date('Tanggal Uji')
    nomor_laporan		= fields.Char('No Laporan')
    nomor_sertifikat_uji 	= fields.Char('Nomor Sertifikat Uji')
    foto_product		= fields.Binary('Foto Product')
    
    document            = fields.Many2many('ir.attachment','class_ir_attachment_ujicoba_rel','class_ujicoba_id','attachment_ujicoba_id','Attachment')
    category_id			= fields.Selection([('persenjataan','Persenjataan'),
    										('transportasi','Transportasi'),
    										('material_khusus','Material Khusus'),
    										('elektronika_ti','Elektronika dan TI')],'Category')

    # kendaraan_type		= fields.Selection([('dua','Roda Dua'),
    # 										('tiga','Roda Tiga'),
    # 										'Type'])
    kendaraan_type		= fields.Selection([('rodadua','Roda Dua'),
    										('rodatiga','Roda Tiga')],'Type')
    persenjataan_type	= fields.Selection([('genggam','Genggam'),
    										('panjang','Panjang'),
    										('serbu','Serbu'),
    										('others','Lain-Lain')], 'Type')

    material_type		= fields.Selection([('optik','Optik'),
    										('rompi','Rompi'),
    										('helm','Helm'),
    										('tameng','Tameng'),
    										('sepatu','Sepatu'),
    										('others','Lain-Lain')],'Type')

    elektronika_ti_type	= fields.Selection([('sistem_informasi','Sistem Informasi')],'Type')
