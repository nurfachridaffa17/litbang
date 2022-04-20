from odoo import models, fields, api, exceptions

class kategori(models.Model):
    _name = 'tnde.kategori'   
    _description = 'Model Kategori'
    
    name = fields.Char(string="Nama Kategori", required=True)
