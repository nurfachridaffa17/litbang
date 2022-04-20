# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class CustomDashboard(models.Model):
    _name = "custom.dashboard"
    _description = "Custom Dashboard"

    @api.one
    def _get_count(self):
        column1_count = self.env['pdu.pengajuan'].search(
            [('state', '=', 'draft')])
        column2_count = self.env['pdu.disposisi'].search(
            [('state', '=', 'draft')])
        column3_count = self.env['pdu.sprin'].search(
            [('state', '=', 'draft')])
        column4_count = self.env['pdu.undangan'].search(
            [('state', '=', 'draft')])
        column5_count = self.env['pdu.pengujian'].search(
            [('state', '=', 'draft')])
        column6_count = self.env['pdu.berita.acara'].search(
            [('state', '=', 'draft')])
 
        self.column1_count = len(column1_count)
        self.column2_count = len(column2_count)
        self.column3_count = len(column3_count)
        self.column4_count = len(column4_count)
        self.column5_count = len(column5_count)
        self.column6_count = len(column6_count)
 
    color = fields.Integer(string='Color Index')
    name = fields.Char(string="Name")
    column1_count = fields.Integer(compute='_get_count')
    column2_count = fields.Integer(compute='_get_count')
    column3_count = fields.Integer(compute='_get_count')
    column4_count = fields.Integer(compute='_get_count')
    column5_count = fields.Integer(compute='_get_count')
    column6_count = fields.Integer(compute='_get_count')


    def view_column1(self):
        action = self.env.ref('mcs_pdu.action_pdu_pengajuan')
        result = action.read()[0]
        result['domain'] = [('state', '=', 'draft')]
        return result

    def view_column2(self):
        action = self.env.ref('mcs_pdu.action_pdu_disposisi')
        result = action.read()[0]
        result['domain'] = [('state', '=', 'draft')]
        return result

    def view_column3(self):
        action = self.env.ref('mcs_pdu.action_pdu_sprin')
        result = action.read()[0]
        result['domain'] = [('state', '=', 'draft')]
        return result

    def view_column4(self):
        action = self.env.ref('mcs_pdu.action_pdu_undangan')
        result = action.read()[0]
        result['domain'] = [('state', '=', 'draft')]
        return result

    def view_column5(self):
        action = self.env.ref('mcs_pdu.action_pdu_pengujian')
        result = action.read()[0]
        result['domain'] = [('state', '=', 'draft')]
        return result

    def view_column6(self):
        action = self.env.ref('mcs_pdu.action_pdu_berita')
        result = action.read()[0]
        result['domain'] = [('state', '=', 'draft')]
        return result