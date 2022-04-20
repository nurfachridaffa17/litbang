# -*- coding: utf-8 -*-
import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare

class AdvanceExpenseLine(models.Model):
    _name = "advance.expense.line"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Advance Expense Line"

    @api.multi
    @api.depends('unit_amount','quantity')
    def _compute_total_line_expense(self):
        for rec in self:
            amount_line = rec.unit_amount * rec.quantity
            rec.total_amount = amount_line

    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids.total_amount')
    def _compute_total_line_expense_unit_sub1(self):
        for rec in self:
            total = 0.0
            for line in rec.advance_expense_line_ids:
                total += line.total_amount
            rec.subtotal1 = total

    @api.multi
    @api.depends('advance_expense_line_ids2', 'advance_expense_line_ids2.total_amount')
    def _compute_total_line_expense_unit_sub2(self):
        for rec in self:
            total = 0.0
            for line in rec.advance_expense_line_ids2:
                total += line.total_amount
            rec.subtotal2 = total

    @api.multi
    @api.depends('advance_expense_line_ids3', 'advance_expense_line_ids3.total_amount')
    def _compute_total_line_expense_unit_sub3(self):
        for rec in self:
            total = 0.0
            for line in rec.advance_expense_line_ids3:
                total += line.total_amount
            rec.subtotal3 = total

    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids2', 'advance_expense_line_ids3', 'advance_expense_line_ids.total_amount')
    def _compute_total_line_expense_unit(self):
        for rec in self:
            rec.unit_amount = 0.0
            total = 0.0
            for line in rec.advance_expense_line_ids:
                total += line.total_amount
            for line in rec.advance_expense_line_ids2:
                total += line.total_amount
            for line in rec.advance_expense_line_ids3:
                total += line.total_amount
            rec.unit_amount = total

    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids2', 'advance_expense_line_ids3', 'advance_expense_line_ids.realisasi_amount')
    def _compute_total_realisasi(self):
        for rec in self:
            rec.total_realisasi = 0.0
            total = 0.0
            for line in rec.advance_expense_line_ids:
                total += line.realisasi_amount
            for line in rec.advance_expense_line_ids2:
                total += line.realisasi_amount
            for line in rec.advance_expense_line_ids3:
                total += line.realisasi_amount
            rec.total_realisasi += total

    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids2', 'advance_expense_line_ids3', 'advance_expense_line_ids.quantity')
    def _compute_total_volume(self):
        for rec in self:
            rec.total_volume = 0.0
            total = 0.0
            for line in rec.advance_expense_line_ids:
                total += line.quantity
            for line in rec.advance_expense_line_ids2:
                total += line.quantity
            for line in rec.advance_expense_line_ids3:
                total += line.quantity
            rec.total_volume += total

    categ_id = fields.Many2one('product.category', string='Category')
    rengar_komponen = fields.Many2one('rengar.komponen', string='Komponen')
    rengar_subkomponen = fields.Many2one('rengar.subkomponen', string='Sub Komponen')
    product_id = fields.Many2one('product.product', string='Expense')
    product_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=False, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env['product.uom'].search([], limit=1, order='id'))
    unit_amount = fields.Float(string='Unit Price', compute='_compute_total_line_expense_unit', store=True, digits=dp.get_precision('Product Price'))
    quantity = fields.Float(required=True,digits=dp.get_precision('Product Unit of Measure'), default=1)
    description = fields.Char(string='Description', required=False)
    total_amount = fields.Float(string='Subtotal', compute='_compute_total_line_expense', digits=dp.get_precision('Account'))
    subtotal1 = fields.Float(string='Subtotal 1', compute='_compute_total_line_expense_unit_sub1', digits=dp.get_precision('Account'))
    subtotal2 = fields.Float(string='Subtotal 2', compute='_compute_total_line_expense_unit_sub2', digits=dp.get_precision('Account'))
    subtotal3 = fields.Float(string='Subtotal 3', compute='_compute_total_line_expense_unit_sub3', digits=dp.get_precision('Account'))
    currency_id = fields.Many2one('res.currency', string='Currency', related = 'advance_line_id.currency_id', readonly=True, store=True)
    expense_line_ids = fields.One2many('hr.expense', 'sheet_id', string='Expense Lines')
    advance_id = fields.Many2one('head.kertas.kerja', string='Nama Program')
    advance_line_id = fields.Many2one('kertas.kerja', string="Detil Program")
    employee_id = fields.Many2one('hr.employee', required=True, readonly=True, string="Personil", default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1), states={'Draft': [('readonly', False)]})
    department_id = fields.Many2one('hr.department', string='Unit Kerja', readonly=True, states={'Draft': [('readonly', False)]})
    advance_expense_line_ids = fields.One2many('advance.expense.line.detail', 'advance_line_id', string='Tahapan 1', track_visibility='onchange')
    advance_expense_line_ids2 = fields.One2many('advance.expense.line.detail2', 'advance_line_id', string='Tahapan 2', track_visibility='onchange')
    advance_expense_line_ids3 = fields.One2many('advance.expense.line.detail3', 'advance_line_id', string='Tahapan 3', track_visibility='onchange')
    total_realisasi = fields.Float(string='Total Realisasi', compute='_compute_total_realisasi', digits=dp.get_precision('Account'))
    total_volume = fields.Float(string='Total Volume', compute='_compute_total_volume', digits=dp.get_precision('Product Unit of Measure'))
    time_volume = fields.Float(string='Volume', digits=dp.get_precision('Product Unit of Measure'))
    note = fields.Char(string="Judul")
    name = fields.Char(string='Number', related='advance_line_id.name', readonly=1)
    reambursment = fields.Boolean(string='Reimbursement', default=False)
    state = fields.Selection([
                                ('Draft','Draft'),
                                ('Confirm','Confirm'),
                                ('Approve','Pengajuan Approve'),
                                ('Reject','Reject'),
                                ('RConfirm','Realisasi Confirm'),
                                ('RApprove','Realisasi Approve'),
                                ('Done','Done')
                            ], string='State', default='Draft', track_visibility='onchange')

    @api.onchange('employee_id', 'employee_id.address_home_id')
    def get_department(self):
        for line in self:
            line.department_id = line.employee_id.department_id.id
            line.job_id = line.employee_id.job_id.id
            line.manager_id = line.employee_id.parent_id.id
            line.partner_id = line.employee_id.address_home_id and line.employee_id.address_home_id.id or False

    def set_to_draft(self):
        for rec in self:
            rec.state = 'Draft'

    def set_to_confirm(self):
        for rec in self:
            for line in rec.advance_expense_line_ids:
                line.state = 'Confirm'
            for line in rec.advance_expense_line_ids2:
                line.state = 'Confirm'
            for line in rec.advance_expense_line_ids3:
                line.state = 'Confirm'
            rec.state = 'Confirm'

    def set_to_reject(self):
        for rec in self:
            rec.state = 'Reject'

    def set_to_approve(self):
        for rec in self:
            rec.state = 'Approve'

    def set_real_confirm(self):
        for rec in self:
            rec.state = 'RConfirm'

    def set_real_approve(self):
        for rec in self:
            rec.state = 'RApprove'

    def set_to_done(self):
        for rec in self:
            rec.state = 'Done'


class AdvanceExpenseLineDetail(models.Model):
    _name = "advance.expense.line.detail"
    _description = "Advance Expense Line Detail"
    _order = 'detail1 asc, detail2 asc, detail3 asc'

    @api.multi
    @api.depends('unit_amount','quantity')
    def _compute_total_line_expense(self):
        for rec in self:
            amount_line = rec.unit_amount * rec.quantity
            rec.total_amount = amount_line

    product_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=False, default=lambda self: self.env['product.uom'].search([], limit=1, order='id'))
    unit_amount = fields.Float(string='Unit Price',required=True,digits=dp.get_precision('Product Price'))
    quantity = fields.Float(required=True,digits=dp.get_precision('Product Unit of Measure'), default=1)
    detail1 = fields.Many2one(string='Detail Header', comodel_name='rengar.detail1', required=False)
    detail2 = fields.Many2one(string='Sub Detail Header', comodel_name='rengar.detail2', required=False)
    detail3 = fields.Many2one(string='Detail', comodel_name='rengar.detail3', required=False)
    total_amount = fields.Float(string='Subtotal', compute='_compute_total_line_expense', digits=dp.get_precision('Account'))
    advance_line_id = fields.Many2one('advance.expense.line', string="Expense Line")
    realisasi_amount = fields.Float(string='Realisasi', digits=dp.get_precision('Product Price'))
    revised = fields.Float(string="Revised")
    uraian = fields.Char(string="Uraian")
    state = fields.Selection([('Draft','Draft'),('Confirm','Confirm'),('Approve','Approve'),('Reject','Reject'),('Done','Done')], string='State', default='Draft')

    def set_to_draft(self):
        for rec in self:
            rec.state = 'Draft'

    def set_to_confirm(self):
        for rec in self:
            rec.state = 'Confirm'

    def set_to_reject(self):
        for rec in self:
            rec.state = 'Reject'
            rec.revised = rec.total_amount

    def set_to_done(self):
        for rec in self:
            rec.state = 'Done'


class AdvanceExpenseLineDetail2(models.Model):
    _name = "advance.expense.line.detail2"
    _description = "Advance Expense Line Detail"
    _order = 'detail1 asc, detail2 asc, detail3 asc'

    @api.multi
    @api.depends('unit_amount','quantity')
    def _compute_total_line_expense(self):
        for rec in self:
            amount_line = rec.unit_amount * rec.quantity
            rec.total_amount = amount_line

    product_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=False, default=lambda self: self.env['product.uom'].search([], limit=1, order='id'))
    unit_amount = fields.Float(string='Unit Price',required=True,digits=dp.get_precision('Product Price'))
    quantity = fields.Float(required=True,digits=dp.get_precision('Product Unit of Measure'), default=1)
    detail1 = fields.Many2one(string='Detail Header', comodel_name='rengar.detail1', required=False)
    detail2 = fields.Many2one(string='Sub Detail Header', comodel_name='rengar.detail2', required=False)
    detail3 = fields.Many2one(string='Detail', comodel_name='rengar.detail3', required=False)
    total_amount = fields.Float(string='Subtotal', compute='_compute_total_line_expense', digits=dp.get_precision('Account'))
    advance_line_id = fields.Many2one('advance.expense.line', string="Expense Line")
    realisasi_amount = fields.Float(string='Realisasi', digits=dp.get_precision('Product Price'))
    revised = fields.Float(string="Revised")
    uraian = fields.Char(string="Uraian")
    state = fields.Selection([('Draft','Draft'),('Confirm','Confirm'),('Approve','Approve'),('Reject','Reject'),('Done','Done')], string='State', default='Draft')

    def set_to_draft(self):
        for rec in self:
            rec.state = 'Draft'

    def set_to_confirm(self):
        for rec in self:
            rec.state = 'Confirm'

    def set_to_reject(self):
        for rec in self:
            rec.state = 'Reject'
            rec.revised = rec.total_amount

    def set_to_done(self):
        for rec in self:
            rec.state = 'Done'


class AdvanceExpenseLineDetail3(models.Model):
    _name = "advance.expense.line.detail3"
    _description = "Advance Expense Line Detail"
    _order = 'detail1 asc, detail2 asc, detail3 asc'

    @api.multi
    @api.depends('unit_amount','quantity')
    def _compute_total_line_expense(self):
        for rec in self:
            amount_line = rec.unit_amount * rec.quantity
            rec.total_amount = amount_line

    product_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=False, default=lambda self: self.env['product.uom'].search([], limit=1, order='id'))
    unit_amount = fields.Float(string='Unit Price',required=True,digits=dp.get_precision('Product Price'))
    quantity = fields.Float(required=True,digits=dp.get_precision('Product Unit of Measure'), default=1)
    detail1 = fields.Many2one(string='Detail Header', comodel_name='rengar.detail1', required=False)
    detail2 = fields.Many2one(string='Sub Detail Header', comodel_name='rengar.detail2', required=False)
    detail3 = fields.Many2one(string='Detail', comodel_name='rengar.detail3', required=False)
    total_amount = fields.Float(string='Subtotal', compute='_compute_total_line_expense', digits=dp.get_precision('Account'))
    advance_line_id = fields.Many2one('advance.expense.line', string="Expense Line")
    realisasi_amount = fields.Float(string='Realisasi', digits=dp.get_precision('Product Price'))
    revised = fields.Float(string="Revised")
    uraian = fields.Char(string="Uraian")
    state = fields.Selection([('Draft','Draft'),('Confirm','Confirm'),('Approve','Approve'),('Reject','Reject'),('Done','Done')], string='State', default='Draft')

    def set_to_draft(self):
        for rec in self:
            rec.state = 'Draft'

    def set_to_confirm(self):
        for rec in self:
            rec.state = 'Confirm'

    def set_to_reject(self):
        for rec in self:
            rec.state = 'Reject'
            rec.revised = rec.total_amount

    def set_to_done(self):
        for rec in self:
            rec.state = 'Done'
