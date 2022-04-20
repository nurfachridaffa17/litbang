from odoo import models, fields, api, _
from datetime import datetime

class pdu_pengujian(models.Model):
    _name = "pdu.pengujian"
    _inherit = ['mail.thread']
    _description = "Pelaksanaan Pengujian"

    name = fields.Char(string='No Sertifikat Uji', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    no_surat = fields.Many2one(comodel_name='pdu.pengajuan', string='No. Surat', readonly=False, required=False)
    ketua = fields.Many2one(string='Ketua TIM', comodel_name='hr.employee', required=False)
    date = fields.Datetime('Tanggal Uji Coba', copy=False, default=datetime.now())
    tempat = fields.Char('Tempat Uji Coba')
    product_id = fields.Many2one('product.material', string='Nama Material', ondelete='restrict', required=True)
    alat_uji = fields.Char(string='Alat Uji SST')
    nilai_bkp = fields.Float('Nilai Bidang Konstruksi dan Perlengkapan')
    nilai_bk = fields.Float('Nilai Bidang Kemampuan')
    nilai_bkk = fields.Float('Nilai Bidang Kelancaran Kerja')
    attach_file = fields.Binary('Sertifikat')
    attach_name = fields.Char('Sertifikat Name')
    nilai_akhir = fields.Float('Nilai Akhir', compute='get_nilai', store=True)
    status_ujian = fields.Selection([('Lulus','Lulus'),('Tidak Lulus','Tidak Lulus')], 'Status Ujian')
    notes = fields.Text('Catatan')
    state = fields.Selection([
                        ('draft', 'Pengujian'),
                        ('process', 'Proses'),
                        ('done', 'Selesai'),
                    ], string='Status', readonly=True, copy=False, store=True, default='draft')

    @api.depends('nilai_bkp','nilai_bk','nilai_bkk')
    def get_nilai(self):
        self.nilai_akhir = (self.nilai_bkp + self.nilai_bk + self.nilai_bkk) / 3

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pdu.pengujian') or _('New')

        result = super(pdu_pengujian, self).create(vals)
        return result

    def selesai(self):
        self.state = 'done'