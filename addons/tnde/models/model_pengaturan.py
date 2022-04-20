from odoo import models, fields, api, exceptions

class m_pengaturan_master_surat(models.Model):
    _name = 'tnde.m_pengaturan_master_surat'  
    _description = 'model m_pengaturan_master_surat'
    
    name = fields.Char(string="Jenis Surat", required=True)  
    versi = fields.Char(string='Versi') 
    kode_surat = fields.Char(string='Kode Surat')  
    template = fields.Html(string='Template Surat') 
    format_nomor = fields.Char(string='Format Nomor Surat') 
    active = fields.Boolean(string="Aktif?", default=True) 
    

