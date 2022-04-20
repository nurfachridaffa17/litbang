# -*- coding: utf-8 -*-

from odoo import models, fields, api

class jurnal(models.Model):
    _name               = 'jurnal'  # nama model  
    _description        = 'Model Jurnal Publik'

    name                = fields.Char(string="Judul", required=True)  
    url_file            = fields.Char(string="URL File", required=False)  
    ket                 = fields.Text(string="Deskripsi", required=False) 
    	
   