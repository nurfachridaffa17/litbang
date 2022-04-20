from openerp import models, fields, api, _
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning


class surat_keluar(models.Model):
    _inherit = "surat_keluar"

    pengajuan_id    = fields.Many2one(comodel_name='pdu.pengajuan', string="Pengajuan ID", readonly=True)


class pdu_pengajuan(models.Model):
    _name = "pdu.pengajuan"
    _inherit = ['mail.thread']
    _description = "Pengajuan PDU"

    name            = fields.Char(string='Nomor Pengajuan', required=True, copy=False, readonly=True, track_visibility='onchange', index=True, default=lambda self: _('New'))
    ref             = fields.Many2one(comodel_name="surat_masuk_fix", string='Nomor Surat', required=True, track_visibility='always')
    date            = fields.Datetime('Tanggal Surat', copy=False, required=True, default=datetime.now(), track_visibility='onchange')
    partner_id      = fields.Many2one(comodel_name='res.partner', string="Vendor", required=True, track_visibility='always')
    product_ids     = fields.Many2many(comodel_name='product.material', string='Material', track_visibility='onchange')
    surat_ids       = fields.One2many(comodel_name='surat_keluar', inverse_name='pengajuan_id', string='Surat', track_visibility='onchange')
    # disposisi_ids   = fields.One2many(comodel_name='surat.masuk.disposisi', inverse_name='parent_id', related='ref.disposisi_ids', string='Lembar Disposisi', track_visibility='onchange')
    ujian_ids       = fields.One2many(comodel_name='pdu.pengujian', inverse_name='no_surat', string='Pengujian', track_visibility='onchange')
    state           = fields.Selection([
                        ('draft', 'Pengajuan'),
                        ('Disposisi', 'Disposisi'),
                        ('Surat Perintah', 'Surat Perintah'),
                        ('Surat Undangan', 'Surat Undangan'),
                        ('Surat Pinjam Fasilitas', 'Surat Pinjam Fasilitas'),
                        ('Pengujian', 'Pengujian'),
                        ('Berita Acara', 'Berita Acara'),
                        ('Laporan Uji', 'Laporan Uji'),
                        ('sertifikat', 'Sertifikat'),
                        ('pemberitahuan', 'Pemberitahuan'),
                        ('Nota Dinas', 'Nota Dinas'),
                        ('selesai', 'Selesai')
                    ], string='Status', readonly=True, copy=False, store=True, default='draft', track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pdu.pengajuan') or _('New')

        result = super(pdu_pengajuan, self).create(vals)
        return result

    @api.multi
    def create_disposisi(self):
        self.state = 'Disposisi'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'LD')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Permohonan Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def create_sprin(self):
        self.state = 'Surat Perintah'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'SPRIN')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Surat Perintah Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def create_undangan(self):
        self.state = 'Surat Undangan'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'UD')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Surat Undangan Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def create_pinjam(self):
        self.state = 'Surat Pinjam Fasilitas'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'FS')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Surat Pinjam Fasilitas untuk melakukan Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def create_ujian(self):
        self.state = 'Pengujian'
        data = self.env['pdu.pengujian']
        for row in self.product_ids:
            vals = {
                'no_surat'      : self.id,
                'date'          : datetime.now(),
                'product_id'    : row.id,
            }
            data_ids = data.create(vals)

    @api.multi
    def create_berita(self):
        self.state = 'Berita Acara'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'BA')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Berita Acara Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def create_laporan(self):
        self.state = 'Laporan Uji'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'LAP')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Laporan Hasil Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def create_sertifikat(self):
        self.state = 'sertifikat'

    @api.multi
    def create_pemberitahuan(self):
        self.state = 'pemberitahuan'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'PMV')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Pemberitahuan Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def create_nota(self):
        self.state = 'Nota Dinas'
        surat_id = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat', '=', 'NDPDU')])
        data = self.env['surat_keluar']
        vals = {
            'pengajuan_id'  : self.id,
            'name'          : 'Nota Dinas Uji Coba',
            'tgl_surat'     : datetime.now(),
            'jenis_surat'   : surat_id.id,
            'keterangan'    : surat_id.template,
        }
        data_ids = data.create(vals)

        # Get Surat views
        form_view = self.env.ref('tnde.surat_keluar_view_form_id')
        tree_view = self.env.ref('tnde.surat_keluar_view_tree_id')
        return {
            'name': _('Surat Keluar'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'surat_keluar',
            'res_id': data_ids.id,
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
                (tree_view.id, 'tree'),
            ],
        }

    @api.multi
    def selesai(self):
        self.state = 'selesai'