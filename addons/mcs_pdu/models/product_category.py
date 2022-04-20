from odoo import models, fields, api, _

class pdu_kategori(models.Model):
    _name = "pdu.kategori"

    code = fields.Char('Kode Kategori', index=True, required=True, translate=True)
    name = fields.Char('Nama Kategori', index=True, required=True, translate=True)

class pdu_subkategori(models.Model):
    _name = "pdu.subkategori"

    name = fields.Char('Sub Kategori', index=True, required=True, translate=True)
    kategori_id = fields.Many2one(comodel_name='pdu.kategori', string='Kategori', required=True)