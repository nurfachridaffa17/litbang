from odoo import models, fields, api, tools, _

class VSuratKeluar(models.Model):
    _name = 'v.surat.keluar'
    _auto = False

    jenis_surat     = fields.Many2one(comodel_name='tnde.m_pengaturan_master_surat', string="Jenis Surat", readonly=True,)
    perihal         = fields.Char(string="Perihal", readonly=True)
    kd_klasifikasi  = fields.Many2one(comodel_name='kode_tersier', string="Pilih Kode", readonly=True)
    tgl_surat       = fields.Date(string="Tgl Surat", readonly=True)  
    kepada          = fields.Char(string="Kepada", readonly=True)
    konseptor       = fields.Char(string="Konseptor / Pemeriksa", readonly=True)
    penandatangan   = fields.Char(string="Penandatangan", readonly=True)
    lampiran_srt_msk= fields.Char(string="Lampiran Surat Masuk", readonly=True)
    tindakan        = fields.Selection([('Biasa', 'Biasa'),('Cepat', 'Cepat')], string='Tindakan /Respon', default='Biasa', readonly=True)
    state           = fields.Selection([('Buat Surat', 'Buat Surat'),('Draft', 'Draft'),('ACC Konseptor', 'ACC Konseptor'),('ACC TAUD', 'ACC TAUD'),('ACC Sespus', 'ACC Sespus'),('ACC KAPUSLITBANG', 'ACC KAPUSLITBANG'),('Selesai', 'Selesai')], string='State', default='Buat Surat', readonly=True)
    
    def _select(self):
        select_str = """
            SELECT 
                a.id, 
                a.jenis_surat AS jenis_surat, 
                a.state AS state, 
                a.name AS perihal,  
                a.tgl_surat AS tgl_surat, 
                a.kd_klasifikasi AS kd_klasifikasi,
                a.kepada AS kepada, 
                c.name_related AS konseptor, 
                d.name_related AS penandatangan,
                a.tindakan AS tindakan,
                f.name as lampiran_srt_msk
                
                FROM 
                    surat_keluar as a
                LEFT JOIN
                    hr_employee_surat_keluar_rel as b on b.surat_keluar_id = a.id
                LEFT JOIN
                    hr_employee as c on c.id = b.hr_employee_id
                LEFT JOIN
                    hr_employee as d on d.id = a.penandatangan
                LEFT JOIN
                    surat_keluar_surat_masuk_fix_rel as e on e.surat_keluar_id = a.id
                LEFT JOIN
                    surat_masuk_fix as f on f.id = e.surat_masuk_fix_id
            """
        return select_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._select()))