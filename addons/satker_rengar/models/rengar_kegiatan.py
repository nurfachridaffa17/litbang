# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, Warning
from odoo import models, fields, api, _

class rengar_kegiatan(models.Model):
    _name = 'rengar.kegiatan'

    name            = fields.Char(string='Uraian', required=True)
    code            = fields.Char(string='Code', required=True)

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            tit = "%s %s" % (record.code, record.name)
            res.append((record.id, tit))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            args = ['|',('name', operator, name),('code', operator, name)] + args
        record = self.search(args, limit=limit)
        return record.name_get()