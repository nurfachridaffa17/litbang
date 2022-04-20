#############################################################
#                                                                                    
#  Module Name: rikwastu                                                                            
#  Created On: 2018-08-06 10:46                                                                        
#  File Name: D:/MyData/Erwin/Odoo/odoo10_litbang/custom_addons/sim_rikwastu/models/perencanaan_tahunan.py                                                                                
#  Author: Matrica-User                                                                                
#                                                                                                                         
#############################################################
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
#from datetime import timedelta

class perencanaan_tahunan(models.Model):
    # ____________ ORM disini ____________ 
    _name = 'rikwastu.perencanaan_tahunan'    #(nama model/ Id model)
    _inherit = ['mail.thread', 'ir.needaction_mixin']  
    #_inherit='model.inherited'  
    #_inherits='model1,model2'
    _description ='model perencanaan_tahunan'
    #_order ='name asc'  
    #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
    # ____________ field-field mulai disini ____________ 
    menyusun_perencanaan_id = fields.Many2one(comodel_name='program',
            string="Perencanaan", ondelete='set null', index=True) 
    
    perencanaan_ids = fields.One2many(related='menyusun_perencanaan_id.perencanaan_ids', string="Tahapan Perencanaan", 
            inverse_name='parent_id', ondelete='cascade')
    
    thn = fields.Char(string='Tahun') # option: size=40, translate=False)

    name = fields.Char(string="Judul Penelitian", required=True)  #(name=special field representasi model)
    deskripsi = fields.Text()
    active = fields.Boolean(string="Aktif?", default=True)  #(active=special field Kalau active=False -> data tidak muncul) 
    personil_internal_ids = fields.Many2many(comodel_name='hr.employee',string="Seluruh Personil Internal", 
                                ondelete='set null',context={},domain=[],)
 
    personil_eksternal_ids = fields.Many2many(comodel_name='res.partner',string="Seluruh Personil Eksternal", 
                                ondelete='set null',context={},domain=[('supplier','=',True)],)
    
    pelaksanaan_ids = fields.One2many(comodel_name='rikwastu.pelaksanaan', string="Timeline Pelaksanaan", 
            inverse_name='parent_id', ondelete='cascade')
    
    
    lama_durasi = fields.Char(string='Durasi') # option: size=40, translate=False)
    
    satuan_durasi = fields.Selection(string='Satuan',selection=[
            ('hari', 'Hari'), ('bulan', 'Bulan'), ('tahun', 'Tahun')
            ], default='tahun')
            # untuk inherit -> selection_add=[('a', 'A'),('b', 'B')]
            # bisa juga pakai fungsi selection='a_function_name'
    
    # ___Field Special Kanban_____
    # ___field Wajib: warna kartu, kolom pengelompokkan kartu
    color = fields.Integer('Color Index', default=5)
    #       buat model kanban-stagenya untuk comodel field stage_id
    @api.model
    def _get_default_stage(self):
         
        stage_id = self.env['rikwastu.master_flow'].search([('step_id.name','=','Perencanaan'),('urutan','=',1)])
         
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
        stage_ids = self.env['rikwastu.master_flow'].search([('step_id.name','=','Perencanaan')])
        return stage_ids
          
    # ____________ api method disini ____________ 
    @api.multi
    def action_done(self):
        urutan_stage_sekarang = self.stage_id.urutan
        stage_berikut = self.env['rikwastu.master_flow'].search(['&', ('urutan', '=', urutan_stage_sekarang + 1), ('step_id.name','=','Perencanaan')])
        stage_pertama_final = self.env['rikwastu.master_flow'].search(['&', ('urutan', '=', 1), ('step_id.name','=','Finalisasi')])
        if stage_berikut.next_step:
#             sebelum insert cek dulu data sudah ada tau belum
            cari_data = self.env['rikwastu.finalisasi'].search([('perencanaan_id', '=', self.id)])
            if cari_data:
#                 update data ke final
#                 self.env.cr.execute(""" UPDATE rikwastu_finalisasi SET 
#                                             pelaksanaan_ids = %s, name = '%s', 
#                                             color = 0, stage_id = %s, 
#                                             state = 'normal'
#                                             WHERE perencanaan_id = %s""", (self.pelaksanaan_ids,self.name,stage_pertama_final.id,self.id))    
#                 self.env.cr.commit()
                cari_data.write({
                    'pelaksanaan_ids' : self.pelaksanaan_ids,
                    'name' : self.name,
                    'color' : 0,
                    'stage_id' : stage_pertama_final.id,
                    'state' : 'normal',
                })
                self.env.cr.commit()
                
                final = cari_data
                
                
            else :
#                 insert data ke final
                final = self.env['rikwastu.finalisasi'].create({
                    'perencanaan_id': self.id,
                    'pelaksanaan_ids' : self.pelaksanaan_ids,
                    'name' : self.name,
                    'color' : 0,
                    'stage_id' : stage_pertama_final.id,
                    'state' : 'normal',
                })
                self.env.cr.commit()
            
            self.env.cr.execute(""" UPDATE rikwastu_pelaksanaan SET parent_final_id = %s WHERE parent_id = %s""", (final.id,self.id))    
            self.env.cr.commit()
            
            if stage_berikut.id:
                self.stage_id_wil = stage_berikut.id
                self.stage_id = stage_berikut.id
                self.state = 'done'
                self.color = 4
        else :
            if stage_berikut.id:
                self.stage_id_wil = stage_berikut.id
                self.stage_id = stage_berikut.id
                self.state = 'normal'
                self.color = 5
        
        form_id = self.env.ref('sim_rikwastu.perencanaan_tahunan_view_kanban_id')
        print form_id.id
    
        return {
            'name':'Memantau Surat Tugas',
            'view_type':'kanban',
            'view_mode':'kanban,form',
            'res_model':'rikwastu.perencanaan_tahunan',
            'type':'ir.actions.act_window',
#             'domain': [('id', '=', self.id)],
#                 'context':{"search_default_unattended_tickets":0},
#             'view_id' : form_id.id,
#             'res_id':self.id,
            'target':'current',
        }
        
    @api.multi
    def create_berkas(self):
        form_id = self.env.ref('sim_rikwastu.finalisasi_view_form_id')
        print form_id.id
    
        
        return {
            'type':'ir.actions.act_window',
            'name':self.name,
            'view_type':'form',
            'view_mode':'form',
#             'domain': [('parent_id','=',self.id)],
            'res_model':'rikwastu.finalisasi',
#             'context': {'search_default_filter_belum_terkirim':1},
            'context': {'default_perencanaan_id':self.id},
#             'res_id':self.id,
            'view_id' : form_id.id,
            'target':'current',
        }
    
    class kegiatan_sunlaphir(models.Model):
        # ____________ ORM disini ____________ 
        _name = 'rikwastu.kegiatan_sunlaphir'    #(nama model/ Id model)
        #_inherit='model.inherited'  
        #_inherits='model1,model2'
        _description ='model kegiatan_sunlaphir'
        #_order ='name asc'  
        #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
        # ____________ field-field mulai disini ____________ 
        name = fields.Char(string="Nama", required=True)  #(name=special field representasi model)
        deskripsi = fields.Text()
        active = fields.Boolean(string="Aktif?", default=True)  #(active=special field Kalau active=False -> data tidak muncul) 
        # ____________ api method disini ____________ 
        

    
