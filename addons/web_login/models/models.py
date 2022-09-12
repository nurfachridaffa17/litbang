from odoo import models,fields,api

class api_coba(models.Model):
    _name = "api.coba"

    login = fields.Char("Login", copy=False)