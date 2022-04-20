from odoo import models, fields, api, exceptions
import datetime
import time
from Tkconstants import LEFT
from datetime import date


class program(models.Model):
    _name           = 'program'  # nama model  
    _description    = 'Model program' 
    
    _order          = 'id, id desc'  # Menampilkan List Data DESC / ASC
    
    name            = fields.Char(string="Judul Penelitian", required=True)
    objek           = fields.Char(string="Object Penelitian", required=True)
    divisi          = fields.Many2one('hr.department',string="Satker/Fungsi", required=True)
    # divisi          = fields.Many2one('hr.department',string="Satker/Fungsi", domain=[('parent_id','in','BID RIKWASTU')] , required=True)
    thn             = fields.Selection([('2018', '2018'),('2019', '2019')], string='Tahun', default='2018')
    ket             = fields.Text(string="Keterangan", required=False)
    state           = fields.Selection([('Proses', 'Proses'),('Done', 'Done')], string='Status', default='Proses')
    state_tahapan   = fields.Selection([('Tahap Perencanaan', 'Tahap Perencanaan'),('Tahap Pelaksanaan', 'Tahap Pelaksanaan'),('Tahap Akhir', 'Tahap Akhir')], string='Tahapan', default='Tahap Perencanaan')
    perencanaan_ids = fields.One2many(comodel_name='tahapperencanaan', string="Tahap Perencanaan", inverse_name='program', ondelete='cascade')
    
    @api.multi
    def confirm(self):
        stage_pertama_pelaksanaan = self.env['rikwastu.master_flow'].search(['&', ('urutan', '=', 1), ('step_id.name','=','Perencanaan')])
        final = self.env['rikwastu.perencanaan_tahunan'].create({
                    'menyusun_perencanaan_id': self.id,
                    'name' : self.name,
                    'color' : 5,
                    'stage_id' : stage_pertama_pelaksanaan.id,
                    'state' : 'normal',
                    'thn' : self.thn,
                })
        self.env.cr.commit()
        
        self.env.cr.execute(""" UPDATE program SET state_tahapan = 'Tahap Pelaksanaan' WHERE id = %s""", (self.id,))    
        self.env.cr.commit()
        
        self.state='Done'
    


class template(models.Model):
    # ____________ ORM disini ____________ 
    _name           = 'template'    #(nama model/ Id model)
    _description    = 'Model Template Surat'
    
    name            = fields.Char(string="Jenis Surat", required=True)  #(name=special field representasi model)
    kode_surat      = fields.Char(string='Kode Surat') # option: size=40, translate=False) 
    template        = fields.Html(string='Template Surat') 
    format_nomor    = fields.Char(string='Format Nomor Surat') # option: size=40, translate=False)
    # ____________ api method disini ____________ 



class tujuansrt(models.Model):
    # ____________ ORM disini ____________ 
    _name           = 'tujuansrt'    #(nama model/ Id model)
    _description    = 'Model Tujuan Surat'
    
    name            = fields.Char(string="Nama", required=True)  #(name=special field representasi model)
    singkatan       = fields.Char(string="singkatan", required=True)  #(name=special field representasi model)
    alamat          = fields.Text(string='Alamat') # option: size=40, translate=False) 
  

class kegiatan(models.Model):
    # ____________ ORM disini ____________ 
    _name           = 'kegiatan'    #(nama model/ Id model)
    _description    = 'Model Step Kegiatan'
    
    name            = fields.Char(string="Nama Step", required=True)  #(name=special field representasi model)


class tahapperencanaan(models.Model):
    _name           = 'tahapperencanaan'  # nama model  
    _description    = 'Model Perencanaan' 
    
    # _inherit        = ['mail.thread', 'ir.needaction_mixin'] #untuk Notif Jumlah Surat Yang belum Dibaca
    
    _order          = 'id, id desc'  # Menampilkan List Data DESC / ASC
    
    name            = fields.Char(string="Perihal", required=True)
    program         = fields.Many2one('program', string="Judul Penelitian", required=True)
    step            = fields.Many2one('kegiatan', string="Step Kegiatan", required=True)
    kepada          = fields.Many2one(comodel_name='tujuansrt', string="Kepada", required=True)
    jenis_surat     = fields.Many2one(comodel_name='template', string="Jenis Surat", required=True)
    scan_surat      = fields.Binary(string="Lampiran")
    lampiran        = fields.Char("lampiran")
    keterangan      = fields.Text("Keterangan")
    state           = fields.Selection([('Proses', 'Proses'), ('Disetujui', 'Disetujui'),('Selesai', 'Selesai')], string='State', default='Proses')
    
    @api.onchange('jenis_surat')
    def _onchange_keterangan(self):
        # Contoh set auto-changing field
        surat_template = self.env['template'].search([('id','=',self.jenis_surat.id)])
        print "onnnnchangeeee"
        str_surat_template = surat_template.template
#         str_surat_pi = str_surat_pi.replace("{nip_dalnis}",str(self.dalnis_id.nip))
#         str_surat_pi = str_surat_pi.replace("{anggota_tim}",temp_tim)
        self.keterangan = str_surat_template

    @api.multi
    def approve(self):
        self.state='Selesai'
