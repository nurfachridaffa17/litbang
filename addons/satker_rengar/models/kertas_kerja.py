# -*- coding: utf-8 -*-

import time
import odoo.addons.decimal_precision as dp

from odoo.exceptions import UserError, Warning
from odoo import models, fields, api, _
from odoo.tools import float_compare, float_is_zero

class KertasKerja(models.Model):
    _name = 'kertas.kerja'
    _description = "Kertas Kerja"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = 'sequence, rengar_kegiatan_code asc, code_output asc, code_suboutput asc, rengar_komponen_code asc, rengar_subkomponen_code asc'
    # _rec_name = 'code_output'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            row1 = record.code_output or ''
            row2 = record.code_suboutput or ''
            row3 = record.rengar_komponen.display_name or ''
            row4 = record.rengar_subkomponen.display_name or ''
            tit = "%s/%s/%s/%s" % (row1, row2, row3, row4)
            res.append((record.id, tit))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        args = args or []
        if name:
            args = [
                '|','|','|',
                ('code_output', operator, name),
                ('code_suboutput', operator, name),
                ('rengar_komponen', operator, name),
                ('rengar_subkomponen', operator, name),
            ] + args
        record = self.search(args, limit=limit)
        return record.name_get()

    @api.model
    def get_currency(self):
        return self.env.user.company_id.currency_id

    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids.total_amount')
    def _compute_total_amount_expense(self):
        for rec in self:
            rec.total_amount_expense = 0.0
            for line in rec.advance_expense_line_ids:
                rec.total_amount_expense += line.total_amount

    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids.total_realisasi')
    def _compute_total_realisasi(self):
        for rec in self:
            rec.total_realisasi = 0.0
            for line in rec.advance_expense_line_ids:
                rec.total_realisasi += line.total_realisasi

    @api.multi
    @api.depends('journal_id', 'currency_id','comment')
    def _compute_paid_currency(self):
        for rec in self:
            if not rec.journal_id.currency_id:
                rec.paid_in_currency = rec.company_id.currency_id.id
            else:  
                rec.paid_in_currency = rec.journal_id.currency_id

    @api.multi
    @api.depends('move_id', 'move_id.amount')
    def _compute_payed_amount(self):
        for rec in self:
            rec.paid_amount = rec.move_id.amount

    name = fields.Char(
        string='Number',
        default='New',
        readonly=True,
        copy=False,
    )
    employee_id = fields.Many2one('hr.employee', required=True, readonly=True, string="Karyawan",default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1), states={'draft': [('readonly', False)]})
    request_date = fields.Date(string='Requested Date', default=fields.Date.today(), readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date(string='Confirmed Date', \
                        readonly=True, copy=False)
    
    hr_validate_date = fields.Date(string='Approved Date', \
                        readonly=True, copy=False)
    account_validate_date = fields.Date(string='Paid Date', \
                        readonly=True, copy=False)
    confirm_by_id = fields.Many2one('res.users', string='Confirmed By', readonly=True, copy=False)
    hr_manager_by_id = fields.Many2one('res.users', string='Approved By', readonly=True, copy=False)
    account_by_id = fields.Many2one('res.users', string='Paid By', readonly=True, copy=False)
    department_id = fields.Many2one('hr.department', string='Unit Kerja')
    department_ids = fields.Many2many('hr.department', string='Unit Kerja')
    job_id = fields.Many2one('hr.job', string='Job Title', readonly=True, states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Mata Uang', default=get_currency, required=True, readonly=True, states={'draft': [('readonly', False)]})
    comment = fields.Text(string='Comment')
    total_amount_expense = fields.Float(string='Pagu', compute='_compute_total_amount_expense', digits=dp.get_precision('Account'))
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Requested User', readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id, string='Company', readonly=True)
    reason_for_advance = fields.Text(string='Nama Program', readonly=True, states={'draft': [('readonly', False)]})
    advance_id = fields.Many2one('head.kertas.kerja', string='Advance ID')
    state = fields.Selection(related='advance_id.state')
    partner_id = fields.Many2one('res.partner', string='Employee Partner')
    journal_id = fields.Many2one('account.journal', string='Payment Method')
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True)
    paid_in_currency = fields.Many2one('res.currency', string='Paid in Currency',compute='_compute_paid_currency')
    account_id = fields.Many2one('account.account', string='Asset Account')

    move_id = fields.Many2one('account.move', string = 'Journal Entry', readonly=True)
    advance_expense_line_ids = fields.One2many('advance.expense.line', 'advance_line_id', string='Advance Expenses Lines', copy=False)
    paid_amount = fields.Float(compute=_compute_payed_amount, string='Paid Amount', store=True, digits=dp.get_precision('Account'))
    is_paid = fields.Boolean(string='Is Paid')
    rengar_kegiatan = fields.Many2one('rengar.kegiatan', string = 'Nama Kegiatan', required=True)
    rengar_kegiatan_code = fields.Char(related='rengar_kegiatan.code', string='Code Kegiatan', store=True)
    rengar_output = fields.Many2one('rengar.output', string = 'Nama Output', required=True)
    code_output = fields.Char(string='Code Output', compute='get_code_output', store=True)
    rengar_suboutput = fields.Many2one('rengar.suboutput', string = 'Nama Sub Output', required=False)
    code_suboutput = fields.Char(string='Code Sub Output', compute='get_code_suboutput', store=True)
    rengar_komponen = fields.Many2one('rengar.komponen', string = 'Komponen', required=False)
    rengar_komponen_code = fields.Char(related='rengar_komponen.code', string='Code Kegiatan', store=True)
    rengar_subkomponen = fields.Many2one('rengar.subkomponen', string = 'Sub Komponen', required=False)
    rengar_subkomponen_code = fields.Char(related='rengar_subkomponen.code', string='Code Kegiatan', store=True)
    total_realisasi = fields.Float(string='Total Realisasi', compute='_compute_total_realisasi', digits=dp.get_precision('Account'))
    sequence = fields.Integer()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('kertas.kerja') or _('New')

        result = super(KertasKerja, self).create(vals)
        return result

    @api.multi
    def view_line(self, context):
        return {
            'domain'    : [('advance_line_id','=', self.id)],
            'name'      : 'Action',
            'view_type' : 'form',
            'view_mode' : 'tree,form',
            'res_model' : 'advance.expense.line',
            'type'      : 'ir.actions.act_window',
            'context'   : context,
        }

    @api.depends('rengar_kegiatan','rengar_output')
    def get_code_output(self):
        for row in self:
            if row.rengar_output:
                row.code_output = "%s.%s %s" % (row.rengar_kegiatan.code, row.rengar_output.code, row.rengar_output.name)

    @api.depends('rengar_kegiatan', 'rengar_output','rengar_suboutput')
    def get_code_suboutput(self):
        for row in self:
            if row.rengar_suboutput:
                row.code_suboutput = "%s.%s.%s %s" % (row.rengar_kegiatan.code, row.rengar_output.code,  row.rengar_suboutput.code, row.rengar_suboutput.name)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: