# -*- coding: utf-8 -*-

import time
import odoo.addons.decimal_precision as dp

from odoo.exceptions import UserError, Warning
from odoo import models, fields, api, _
from odoo.tools import float_compare, float_is_zero
import datetime

class HeadKertasKerja(models.Model):
    _name = 'head.kertas.kerja'
    _description = "Head Kertas Kerja"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    # _order = 'id desc'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            tit = "[%s] %s" % (record.tahun_anggaran, record.rengar_program.display_name)
            res.append((record.id, tit))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        args = args or []
        if name:
            args = ['|',('rengar_program', operator, name),('tahun_anggaran', operator, name)] + args
        record = self.search(args, limit=limit)
        return record.name_get()

    @api.model
    def get_currency(self):
        return self.env.user.company_id.currency_id
        
    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids.total_amount_expense')
    def _compute_total_amount_expense(self):
        for rec in self:
            rec.total_amount_expense = 0.0
            for line in rec.advance_expense_line_ids:
                rec.total_amount_expense += line.total_amount_expense

    @api.multi
    @api.depends('advance_expense_line_ids', 'advance_expense_line_ids.total_realisasi')
    def _compute_total_realisasi(self):
        for rec in self:
            rec.total_realisasi = 0.0
            rec.sisa_realisasi = 0.0
            rec.persen_sisa = 0.0
            for line in rec.advance_expense_line_ids:
                rec.total_realisasi += line.total_realisasi
            rec.sisa_realisasi = rec.total_amount_expense - rec.total_realisasi
            if rec.total_realisasi:
                rec.persen_realisasi = rec.total_realisasi * 100 / rec.total_amount_expense
            if rec.sisa_realisasi:
                rec.persen_sisa = rec.sisa_realisasi * 100 / rec.total_amount_expense

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
    employee_id = fields.Many2one('hr.employee', required=True, readonly=True, string="Personil",default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1), states={'draft': [('readonly', False)]})
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
    department_id = fields.Many2one('hr.department', string='Department', readonly=True, states={'draft': [('readonly', False)]})
    job_id = fields.Many2one('hr.job', string='Job Title', readonly=True, states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Mata Uang', default=get_currency, required=True, readonly=True, states={'draft': [('readonly', False)]})
    comment = fields.Text(string='Comment')
    total_amount_expense = fields.Float(string='Pagu', compute='_compute_total_amount_expense', digits=dp.get_precision('Account'))
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Requested User', readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id, string='Company', readonly=True)
    reason_for_advance = fields.Text(string='Nama Program', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(selection=[
                        ('draft', 'RENBUT'), \
                        ('confirm', 'INDIKATIF'), \
                        ('approved_hr_manager', 'PAGU ANGARAN'),\
                        ('paid', 'ALOKASI ANGGARAN'),\
                        ('done', 'SELESAI'),\
                        ('cancel', 'BATAL'),\
                        ('reject', 'TOLAK')],string='State', \
                        readonly=True, default='draft', \
                        track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Employee Partner')
    journal_id = fields.Many2one('account.journal', string='Payment Method')
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True)
    paid_in_currency = fields.Many2one('res.currency', string='Paid in Currency',compute='_compute_paid_currency')
    account_id = fields.Many2one('account.account', string='Asset Account')
    
    move_id = fields.Many2one('account.move', string = 'Journal Entry', readonly=True)
    advance_expense_line_ids = fields.One2many('kertas.kerja', 'advance_id', string='Kertas Kerja', copy=True)
    paid_amount = fields.Float(compute=_compute_payed_amount, string='Paid Amount', store=True, digits=dp.get_precision('Account'))
    is_paid = fields.Boolean(string='Is Paid')
    rengar_program = fields.Many2one('rengar.program', string = 'Nama Program', required=True)
    tahun_anggaran = fields.Selection([(unicode(num), str(num)) for num in range(2010, int(datetime.datetime.now().year)+3 )], string='Tahun Anggaran', required=True)
    total_realisasi = fields.Float(string='Total Realisasi', store=True, compute='_compute_total_realisasi', digits=dp.get_precision('Account'))
    sisa_realisasi = fields.Float(string='Sisa', store=True, compute='_compute_total_realisasi', digits=dp.get_precision('Account'))
    persen_realisasi = fields.Float(string='Realisasi (%)', store=True, compute='_compute_total_realisasi', digits=dp.get_precision('Account'))
    persen_sisa = fields.Float(string='Sisa (%)', store=True, compute='_compute_total_realisasi', digits=dp.get_precision('Account'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('head.kertas.kerja') or _('New')

        result = super(HeadKertasKerja, self).create(vals)
        return result

    @api.multi
    def view_line(self, context):
        return {
            'domain'    : [('advance_id','=', self.id)],
            'name'      : 'Action',
            'view_type' : 'form',
            'view_mode' : 'tree,form',
            'res_model' : 'kertas.kerja',
            'type'      : 'ir.actions.act_window',
            'context'   : context,
        }

    @api.onchange('employee_id', 'employee_id.address_home_id')
    def get_department(self):
        for line in self:
            line.department_id = line.employee_id.department_id.id
            line.job_id = line.employee_id.job_id.id
            line.manager_id = line.employee_id.parent_id.id
            line.partner_id = line.employee_id.address_home_id and line.employee_id.address_home_id.id or False

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

    @api.multi
    def request_set(self):
        self.state = 'draft'
    
    @api.multi
    def exit_cancel(self):
        self.state = 'cancel'
        
    @api.multi
    def get_confirm(self, vals):
        if not self.advance_expense_line_ids:
           raise Warning(_('Please add some advance expense lines.'))
        else:
            # self.name = self.env['ir.sequence'].next_by_code('kertas.kerja')
            self.state = 'confirm'
            self.confirm_date = time.strftime('%Y-%m-%d')
            self.confirm_by_id = self.env.user.id
   
    @api.multi
    def get_apprv_hr_manager(self):
        self.state = 'approved_hr_manager'
        self.hr_validate_date = time.strftime('%Y-%m-%d')
        self.hr_manager_by_id = self.env.user.id

    @api.multi
    def get_paid(self):
        self.state = 'paid'

    @api.multi
    def get_done(self):
        self.state = 'done'

    @api.multi
    def get_reject(self):
        self.state = 'reject'

    @api.multi
    def create_project(self):
        # self.state = 'done'
        data = self.env['project.project']
        line = self.env['project.task']
        vals = {
            # 'pengajuan_id'  : self.id,
            'name'          : self.rengar_kegiatan,
        }
        data_ids = data.create(vals)

        for row in self.advance_expense_line_ids:
            line_vals = {
                'name'          : row.description,
                'project_id'    : data_ids.id,
            }
            line.create(line_vals)

    @api.multi
    def action_sheet_move_advance(self):
        created_moves = self.env['account.move']
        prec = self.env['decimal.precision'].precision_get('Account')
        if not self.journal_id:
                raise UserError(_("No Credit account found for the Journal, please configure one.") % (self.journal_id))
        if not self.journal_id:
                raise UserError(_("No Debit account found for the account, please configure one.") % (self.account_id))
        for line in self:
#             category_id = line.asset_id.category_id
            adv_exp_date = fields.Date.context_today(self)
            company_currency = line.company_id.currency_id
            current_currency = line.currency_id
            amount = current_currency.compute(line.total_amount_expense, company_currency)
            ref = line.name 
            move_line_debit = {
                'name': ref,
                'account_id': line.journal_id.default_credit_account_id.id,
                'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'journal_id': line.journal_id.id,
                'partner_id': line.partner_id.id,
#                 'analytic_account_id': category_id.account_analytic_id.id if category_id.type == 'sale' else False,
                'currency_id': company_currency != current_currency and current_currency.id or False,
                'amount_currency': company_currency != current_currency and - 1.0 * line.total_amount_expense or 0.0,
            }
            move_line_credit = {
                'name': ref,
                'account_id': line.account_id.id,
                'credit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'debit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'journal_id': line.journal_id.id,
                'partner_id': line.partner_id.id,
#                 'analytic_account_id': category_id.account_analytic_id.id if category_id.type == 'purchase' else False,
                'currency_id': company_currency != current_currency and current_currency.id or False,
                'amount_currency': company_currency != current_currency and line.total_amount_expense or 0.0,
            }
            move_vals = {
                'ref': line.name,
                'date': adv_exp_date or False,
                'journal_id': line.journal_id.id,
                'narration':line.reason_for_advance,
                'line_ids': [(0, 0, move_line_debit), (0, 0, move_line_credit)],
            }
            move = self.env['account.move'].create(move_vals)
            line.write({'move_id': move.id, 
                        'move_check': True, 
                        'state':'paid', 
                        'account_validate_date':time.strftime('%Y-%m-%d'),
                        'account_by_id':line.env.user.id,
                        'is_paid':True})
            created_moves |= move

#         if post_move and created_moves:
#             created_moves.filtered(lambda m: any(m.asset_depreciation_ids.mapped('asset_id.category_id.open_asset'))).post()
        return [x.id for x in created_moves]
    
    @api.multi
    def show_journal(self):
        action = self.env.ref('account.action_move_line_form')
        res = action.read()[0]
        res['domain'] = str([('id','=',self.move_id.id)])
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
