# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, Warning
from odoo import models, fields, api, _

class rengar_detail2(models.Model):
    _name = 'rengar.detail2'
    
    name            = fields.Char(string='Uraian', required=True)
    account_id      = fields.Many2one(comodel_name='account.account', string='MAK')