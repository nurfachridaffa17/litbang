# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import except_orm, Warning, RedirectWarning
from datetime import date, datetime, timedelta
import time

class eliteratur(models.Model):
    _name               = 'eliteratur'  # nama model  
    _description        = 'E-Literatur'

    #@api.model
    #def _get_this_year(self):
        #return fields.datetime.today().year

    @api.model
    def _get_this_bahasa(self):
    	return self.env['res.country'].search([('name','ilike','Indonesia')],limit=1).id

    name                = fields.Char(string="Judul", required=True)  
    url_file            = fields.Char(string="URL File", required=True)  
    author              = fields.Char(string="Author")
    edisi               = fields.Char(string="Edisi")
    no_panggil          = fields.Char(string="No. Panggil")
    isbn_issn           = fields.Selection([('ISBN','ISBN'),('ISSN','ISSN')],string="ISBN / ISSN")
    topic_id            = fields.Many2one('eliteratur.kategori', 'Topic', required=True)
    klasifikasi         = fields.Char(string="Klasifikasi")
    judul_seri          = fields.Char(string="Judul Seri")
    bahasa_id           = fields.Many2one('res.country','Bahasa', default=_get_this_bahasa)
    penerbit            = fields.Char(string="Penerbit")
    tahun_terbit        = fields.Char(string="Tahun Terbit")
    tempat_terbit_id    = fields.Many2one('vit.kota','Tempat Terbit')
    deskripsi           = fields.Text(string="Deskripsi", required=False)
    image               = fields.Binary(string="Image", required=False)


class eliteratur_kategori(models.Model):
    _name               = 'eliteratur.kategori'  # nama model  
    _description        = 'Kategori'

    name                = fields.Char(string="Kategori", required=True)     
    active              = fields.Boolean(string="Active", default=True)   
    	
   