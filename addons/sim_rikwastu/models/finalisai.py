#############################################################
#                                                                                    
#  Module Name: rikwastu                                                                            
#  Created On: 2018-08-07 21:26                                                                        
#  File Name: D:/MyData/Erwin/Odoo/odoo10_litbang/custom_addons/sim_rikwastu/models/finalisai.py                                                                                
#  Author: Matrica-User                                                                                
#                                                                                                                         
#############################################################
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
#from datetime import timedelta

class finalisasi(models.Model):
    # ____________ ORM disini ____________ 
    _name = 'rikwastu.finalisasi'    #(nama model/ Id model)
    #_inherit='model.inherited'  
    #_inherits='model1,model2'
    _description ='model finalisasi'
    #_order ='name asc'  
    #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
    # ____________ field-field mulai disini ____________ 
#     _order          = 'id desc'  # Menampilkan List Data DESC / ASC
    perencanaan_id = fields.Many2one(comodel_name='rikwastu.perencanaan_tahunan',
            string="Perencanaan", ondelete='set null', index=True) 
    
    pelaksanaan_ids = fields.One2many(comodel_name='rikwastu.pelaksanaan', string="Timeline Pelaksanaan", 
            inverse_name='parent_final_id', ondelete='cascade')
    
    berkas_final_ids = fields.One2many(comodel_name='rikwastu.berkas_finalisasi', string="Berkas Final", 
            inverse_name='parent_id', ondelete='cascade')
    
    
    name = fields.Char(string="Judul Penelitian", required=True)  #(name=special field representasi model)
    deskripsi = fields.Text()
    
    draf_laporan_akhir = fields.Html(string='Draft Laporan Akhir')
    draft_lap_akhir = fields.Binary(string='File Draft Laporan Akhir')
    file_name = fields.Char(string='filename') # option: size=40, translate=False)
    
    active = fields.Boolean(string="Aktif?", default=True)  #(active=special field Kalau active=False -> data tidak muncul) 
    
    personil_internal_ids = fields.Many2many(comodel_name='hr.employee',string="Seluruh Personil Internal", 
                                ondelete='set null',context={},domain=[],)
  
    personil_eksternal_ids = fields.Many2many(comodel_name='res.partner',string="Seluruh Personil Eksternal", 
                                ondelete='set null',context={},domain=[('supplier','=',True)],)
    
    per_internal_ids = fields.Many2many(related='perencanaan_id.personil_internal_ids',string="Seluruh Personil Internal", 
                                ondelete='set null',context={},domain=[],)
  
    per_eksternal_ids = fields.Many2many(related='perencanaan_id.personil_eksternal_ids',string="Seluruh Personil Eksternal", 
                                ondelete='set null',context={},domain=[('supplier','=',True)],)
    
    # ___Field Special Kanban_____
    # ___field Wajib: warna kartu, kolom pengelompokkan kartu
    color = fields.Integer('Color Index', default=5)
    #       buat model kanban-stagenya untuk comodel field stage_id
    @api.model
    def _get_default_stage(self):
         
        stage_id = self.env['rikwastu.master_flow'].search([('step_id.name','=','Finalisasi'),('urutan','=',1)])
         
        return stage_id
    
    stage_id = fields.Many2one(comodel_name='rikwastu.master_flow', group_expand='_read_all_stage_ids',default=_get_default_stage) 
    # ___field Optional: avatar/foto incharge, priority (bintang), state (merah, kuning, hijau) 
    incharge_id = fields.Many2one(comodel_name='res.partner',
            string="Penanggung Jawab", ondelete='set null', index=True) # Avatar di kanban 
    priority = fields.Selection(   # di viewnya widget priority (tanda bintang2) 
        [('0', 'Low'),  
         ('1', 'Normal'),  
         ('2', 'High')], 
        'Priority', default='1') 
    state = fields.Selection(  # di viewnya pakai widget kanban_state_selection
        [('normal', 'In Progress'), 
         ('blocked', 'Blocked'), 
         ('done', 'Ready for next stage')], 
          'Kanban State', default='normal') 
          
    @api.model
    def _read_all_stage_ids(self,stages,domain,order):
        stage_ids = self.env['rikwastu.master_flow'].search([('step_id.name','=','Finalisasi')])
        return stage_ids
    
    @api.multi
    def action_done(self):
        urutan_stage_sekarang = self.stage_id.urutan
        stage_berikut = self.env['rikwastu.master_flow'].search(['&', ('urutan', '=', urutan_stage_sekarang + 1), ('step_id.name','=','Finalisasi')])
        
        
            
        if stage_berikut.id:
            self.stage_id_wil = stage_berikut.id
            self.stage_id = stage_berikut.id
            self.state = 'done'
            self.color = 4
        
    
        return {
            'name':'Next Step',
            'view_type':'kanban',
            'view_mode':'kanban,form',
            'res_model':'rikwastu.finalisasi',
            'type':'ir.actions.act_window',
#             'domain': [('id', '=', self.id)],
#                 'context':{"search_default_unattended_tickets":0},
#             'view_id' : form_id.id,
#             'res_id':self.id,
            'target':'current',
        }
    
    @api.multi
    def create_draft(self):

        return {
            'type':'ir.actions.act_window',
            'name':'Membuat berkas',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'rikwastu.finalisasi',
#             'context': {'default_parent_id':self.id},
            'res_id':self.id,
            'target':'new',
        }
    
    @api.multi
    def create_berkas(self):

        return {
            'type':'ir.actions.act_window',
            'name':'Membuat berkas',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'rikwastu.berkas_finalisasi',
            'context': {'default_parent_id':self.id},

            'target':'new',
        }
        
    
    @api.multi
    def view_berkas(self):

        return {
            'type':'ir.actions.act_window',
            'name':'Tampilkan berkas',
            'view_type':'form',
            'view_mode':'tree',
            'res_model':'rikwastu.berkas_finalisasi',
#             'context': {'default_parent_id':self.id},
            'domain': [('parent_id','=',self.id)],
            'target':'new',
        }

class berkas_finalisasi(models.Model):
    # ____________ ORM disini ____________ 
    _name = 'rikwastu.berkas_finalisasi'    #(nama model/ Id model)
    #_inherit='model.inherited'  
    #_inherits='model1,model2'
    _description ='model berkas_finalisasi'
    #_order ='name asc'  
    #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
    # ____________ field-field mulai disini ____________ 
    _order          = 'id, id desc'  # Menampilkan List Data DESC / ASC
    
    name            = fields.Char(string="Perihal", required=True)
    program         = fields.Many2one('program', string="Nama program", required=True)
    step            = fields.Many2one('kegiatan', string="Step Kegiatan", required=True)
    kepada          = fields.Many2one(comodel_name='tujuansrt', string="Kepada", required=True)
    jenis_surat     = fields.Many2one(comodel_name='template', string="Jenis Surat", required=True)
    perencanaan_id = fields.Many2one(comodel_name='rikwastu.perencanaan_tahunan',
            string="Perencanaan", ondelete='set null', index=True) 
    
    parent_id = fields.Many2one(comodel_name='rikwastu.finalisasi',
            string="parent", ondelete='set null', index=True) 
    
    
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
        
    # ___Field Special Kanban_____
    # ___field Wajib: warna kartu, kolom pengelompokkan kartu
    color = fields.Integer('Color Index', default=5)
    #       buat model kanban-stagenya untuk comodel field stage_id
    @api.model
    def _get_default_stage(self):
         
        stage_id = self.env['rikwastu.master_flow'].search([('step_id.name','=','Finalisasi'),('urutan','=',1)])
         
        return stage_id
    
    stage_id = fields.Many2one(comodel_name='rikwastu.master_flow', group_expand='_read_all_stage_ids',default=_get_default_stage) 
    # ___field Optional: avatar/foto incharge, priority (bintang), state (merah, kuning, hijau) 
    incharge_id = fields.Many2one(comodel_name='res.partner',
            string="Penanggung Jawab", ondelete='set null', index=True) # Avatar di kanban 
    priority = fields.Selection(   # di viewnya widget priority (tanda bintang2) 
        [('0', 'Low'),  
         ('1', 'Normal'),  
         ('2', 'High')], 
        'Priority', default='1') 
    state = fields.Selection(  # di viewnya pakai widget kanban_state_selection
        [('normal', 'In Progress'), 
         ('blocked', 'Blocked'), 
         ('done', 'Ready for next stage')], 
          'Kanban State', default='normal') 
          
    @api.model
    def _read_all_stage_ids(self,stages,domain,order):
        stage_ids = self.env['rikwastu.master_flow'].search([('step_id.name','=','Finalisasi')])
        return stage_ids
          
    # ____________ api method disini ____________ 
    @api.multi
    def action_done(self):
        urutan_stage_sekarang = self.stage_id.urutan
        stage_berikut = self.env['rikwastu.master_flow'].search(['&', ('urutan', '=', urutan_stage_sekarang + 1), ('step_id.name','=','Finalisasi')])
        if stage_berikut.id:
            self.stage_id_wil = stage_berikut.id
            self.stage_id = stage_berikut.id
            self.state = 'done'
            self.color = 4
        
    
        return {
            'name':'Memantau Surat Tugas',
            'view_type':'kanban',
            'view_mode':'kanban,form',
            'res_model':'rikwastu.finalisasi',
            'type':'ir.actions.act_window',
#             'domain': [('id', '=', self.id)],
#                 'context':{"search_default_unattended_tickets":0},
#             'view_id' : form_id.id,
#             'res_id':self.id,
            'target':'current',
        }
        
