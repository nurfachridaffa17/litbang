from odoo import api, fields, models, _

class Fungsi(models.Model):
    _name = "fungsi"
    _rec_name = "name"

    name = fields.Char("Fungsi")

class Survey(models.Model):
    _inherit = "survey.survey"

    fungsi = fields.Many2one("fungsi", "Fungsi")
