# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp

class HrExpense(models.Model):
    _inherit = "hr.expense"
    
    @api.depends('advance_expense_id', 'advance_expense_id.total_amount')
    def _compute_advance_expense_id(self):
        for rec in self:
            amount = 0.0
            amount = rec.advance_expense_id.total_amount
            rec.advance_amount = amount
    
    advance_expense_id = fields.Many2one(
        'advance.expense.line', 
        string='Expense Advance', 
        copy=False
    )
    advance_amount = fields.Float(
        string='Advance Amount', 
        compute='_compute_advance_expense_id', 
        store=True
    )
    advance_currency_id = fields.Many2one(
        'res.currency', 
        string='Expense Advance Currency', 
        related='advance_expense_id.currency_id',
        store=True,
    )
    advance_expense_line_ids = fields.One2many('hr.expense.detail', 'advance_line_id', string='HR Expense Detail', copy=False)
    
    @api.multi
    def submit_expenses(self): # Override Odoo method.
        result = super(HrExpense, self).submit_expenses()
        for rec in self:
            if rec.advance_expense_id:
                rec.advance_expense_id.reambursment = True
        return result
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


class expense_detail(models.Model):
    _name = "hr.expense.detail"
    _description = "HR Expense Detail"

    @api.multi
    @api.depends('unit_amount','quantity')
    def _compute_total_line_expense(self):
        for rec in self:
            amount_line = rec.unit_amount * rec.quantity
            rec.total_amount = amount_line

    product_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=True, default=lambda self: self.env['product.uom'].search([], limit=1, order='id'))
    unit_amount = fields.Float(string='Unit Price',required=True,digits=dp.get_precision('Product Price'))
    quantity = fields.Float(required=True,digits=dp.get_precision('Product Unit of Measure'), default=1)
    description = fields.Char(string='Description', required=True)
    total_amount = fields.Float(string='Subtotal', compute='_compute_total_line_expense', digits=dp.get_precision('Account'))
    advance_line_id = fields.Many2one('hr.expense', string="Expense")
