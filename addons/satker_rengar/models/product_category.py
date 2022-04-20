# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, Warning
from odoo import models, fields, api, _

class product_category(models.Model):
    _inherit = 'product.category'

    code            = fields.Char(string='Code', required=True)

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            tit = "[%s] %s" % (record.code, record.name)
            res.append((record.id, tit))
        return res