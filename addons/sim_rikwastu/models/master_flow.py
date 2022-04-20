#############################################################
#                                                                                    
#  Module Name: rikwastu                                                                            
#  Created On: 2018-08-06 13:17                                                                        
#  File Name: D:/MyData/Erwin/Odoo/odoo10_litbang/custom_addons/sim_rikwastu/models/master_flow.py                                                                                
#  Author: Matrica-User                                                                                
#                                                                                                                         
#############################################################
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
#from datetime import timedelta

class master_flow(models.Model):
    # ____________ ORM disini ____________ 
    _name = 'rikwastu.master_flow'    #(nama model/ Id model)
    #_inherit='model.inherited'  
    #_inherits='model1,model2'
    _description ='model master_flow'
    _order ='urutan asc'  
    #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
    # ____________ field-field mulai disini ____________ 
    name = fields.Char(string="Nama", required=True)  #(name=special field representasi model)
    deskripsi = fields.Text()
    urutan = fields.Integer(string='Urutan Flow')
    active = fields.Boolean(string="Aktif?", default=True)  #(active=special field Kalau active=False -> data tidak muncul)
    step_id = fields.Many2one(comodel_name='rikwastu.master_flow_step',
            string="Tahapan", ondelete='set null', index=True) 
    
    next_step = fields.Boolean(string='Pindah Tahapan Berikut')
    
    
    
    # ____________ api method disini ____________ 

class master_flow_step(models.Model):
    # ____________ ORM disini ____________ 
    _name = 'rikwastu.master_flow_step'    #(nama model/ Id model)
    #_inherit='model.inherited'  
    #_inherits='model1,model2'
    _description ='model master_flow_step'
    #_order ='name asc'  
    #_rec_name="field_pengganti_name" #(overide field name sbg representatif model)
    # ____________ field-field mulai disini ____________ 
    name = fields.Char(string="Nama", required=True)  #(name=special field representasi model)
    deskripsi = fields.Text()
    active = fields.Boolean(string="Aktif?", default=True)  #(active=special field Kalau active=False -> data tidak muncul) 
    # ____________ api method disini ____________ 
    

