#############################################################
#                                                                                    
#  Module Name: rikwastu                                                                            
#  Created On: 2018-08-07 11:27                                                                        
#  File Name: D:/MyData/Erwin/Odoo/odoo10_litbang/custom_addons/sim_rikwastu/models/pelaksanaan.py                                                                                
#  Author: Matrica-User                                                                                
#                                                                                                                         
#############################################################
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
#from datetime import timedelta

class pelaksanaan(models.Model):
    # ____________ ORM disini ____________ 
    _name = 'rikwastu.pelaksanaan'    #(nama model/ Id model)
    #_inherit='model.inherited'  
    #_inherits='model1,model2'
    _description ='model pelaksanaan'
    #_order ='name asc'  
    #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
    # ____________ field-field mulai disini ____________ 
    name = fields.Char(string="Judul Kajian", required=True)  #(name=special field representasi model)
    deskripsi = fields.Text()
    active = fields.Boolean(string="Aktif?", default=True)  #(active=special field Kalau active=False -> data tidak muncul) 
    
    thn = fields.Char(string='Tahun') # option: size=40, translate=False)
    
    langkah_kerja_ids = fields.One2many(comodel_name='rikwastu.langkah_kerja', string="Langkah Kerja", 
            inverse_name='parent_id', ondelete='cascade')
    
    parent_id = fields.Many2one(comodel_name='rikwastu.perencanaan_tahunan',
            string="Perencanaan", ondelete='set null', index=True) 
    
    parent_final_id = fields.Many2one(comodel_name='rikwastu.finalisasi',
            string="Finalisasi", ondelete='set null', index=True) 
    
    prov_id = fields.Many2one(comodel_name='res.country.state',
            string="Provinsi", ondelete='set null', index=True, domain=[('country_id','=', 101)]) 
    
    kota_id = fields.Many2one(comodel_name='vit.kota',
            string="Kota/Kab.", ondelete='set null', index=True, domain=[]) 
    
    tim_internal_ids = fields.Many2many(comodel_name='hr.employee',string="Personil Internal", 
                                ondelete='set null',context={},domain=[],)
 
    tim_eksternal_ids = fields.Many2many(comodel_name='res.partner',string="Personil Eksternal", 
                                ondelete='set null',context={},domain=[('supplier','=',True)],)
    
    lap_sementara = fields.Binary(string='File Laporan Sementara')
    file_name = fields.Char(string='filename') # option: size=40, translate=False)
    
    dok_lap_sementara = fields.Html(string='Laporan Sementara') 
    
    
    
    # ____________ api method disini ____________ 
    @api.multi
    def validasi_pelaksanaan(self):
        # then open the form
        return {
            'type':'ir.actions.act_window',
            'name':self.name,
            'view_type':'form',
            'view_mode':'tree,form',
            'domain': [('parent_id','=',self.id)],
            'res_model':'rikwastu.langkah_kerja',
#             'context': {'search_default_filter_belum_terkirim':1},
#             'context': {'default_surat_tugas_id':self.id},
#             'res_id':self.id,
            'target':'new',
        }
        
        
    @api.multi
    def laporan_sementara(self):
        form_id = self.env.ref('sim_rikwastu.pelaksanaan_upload_view_form_id')
        print form_id.id
        # then open the form
        return {
            'type':'ir.actions.act_window',
            'name':self.name,
            'view_type':'form',
            'view_mode':'form',
#             'domain': [('surat_tugas_id','=',self.id)],
            'res_model':'rikwastu.pelaksanaan',
#             'context': {'default_surat_tugas_id':self.surat_tugas_id.id, 'default_lhp_id':self.id, 'default_create_by_id':self.create_by_id.id},
            'view_id' : form_id.id,
            'res_id':self.id,
            'target':'new',
        }
        
    @api.multi
    def view_perencanaan(self):
        form_id = self.env.ref('sim_rikwastu.tahapperencanaan_lihat_view_tree_id')
        print form_id.id
        
        return {
            'type':'ir.actions.act_window',
            'name':self.name,
            'view_type':'form',
            'view_mode':'tree,form',
            'domain': [('program','=',self.parent_id.menyusun_perencanaan_id.id)],
#             'domain': [('surat_tugas_id','=',self.id)],
            'res_model':'tahapperencanaan',
#             'context': {'default_surat_tugas_id':self.surat_tugas_id.id, 'default_lhp_id':self.id, 'default_create_by_id':self.create_by_id.id},
#             'view_id' : form_id.id,
            'res_id':self.id,
            'target':'new',
        }
        

class langkah_kerja(models.Model):
    # ____________ ORM disini ____________ 
    _name = 'rikwastu.langkah_kerja'    #(nama model/ Id model)
    #_inherit='model.inherited'  
    #_inherits='model1,model2'
    _description ='model langkah_kerja'
    #_order ='name asc'  
    #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
    # ____________ field-field mulai disini ____________ 
    name = fields.Char(string="Nama", required=True)  #(name=special field representasi model)
    active = fields.Boolean(string="Aktif?", default=True)  #(active=special field Kalau active=False -> data tidak muncul) 
    
    parent_id = fields.Many2one(comodel_name='rikwastu.pelaksanaan',
            string="parent", ondelete='set null', index=True) 
    
    
    tgl_mulai = fields.Date(string='Tanggal Mulai',default=fields.Date.today) 
    tgl_akhir = fields.Date(string='Tanggal Akhir',default=fields.Date.today) 
    
    status_pekerjaan = fields.Selection(string='Status',selection=[
            ('proses', 'Proses'), ('terkendala', 'Terkendala'), ('selesai', 'Selesai')
            ], default='proses')
    
    keterangan = fields.Text(string='Keterangan') # option: translate=True
    
    
    dok_pendukung_ids = fields.Many2many('ir.attachment', 'class_ir_attachment_dok_pendukung_rel', 'class_dok_pendukung_id', 'attachment_dok_pendukung_id', 'Dokumen Pendukung')
    
    
    
    # ____________ api method disini ____________ 
    

    
