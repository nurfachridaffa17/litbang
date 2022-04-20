from odoo import models, fields, api, tools, _

class VPDUPengajuan(models.Model):
    _name = 'v.pdu.pengajuan'
    _auto = False

    id_pengajuan    = fields.Integer(string="ID Produk Material", readonly=True)
    date            = fields.Datetime('Tanggal Surat', readonly=True) 
    nomor_pengajuan = fields.Char(string='Nomor Pengajuan', readonly=True)
    vendor          = fields.Char(string="Vendor", readonly=True)
    status          = fields.Selection([
                        ('draft', 'Pengajuan'),
                        ('sent', 'Disposisi'),
                        ('sprin', 'Surat Perintah'),
                        ('undangan', 'Surat Undangan'),
                        ('pinjam', 'Surat Pinjam Fasilitas'),
                        ('ujian', 'Pengujian'),
                        ('berita', 'Berita Acara'),
                        ('laporan', 'Laporan Uji'),
                        ('sertifikat', 'Sertifikat'),
                        ('pemberitahuan', 'Pemberitahuan'),
                        ('nota', 'Nota Dinas'),
                        ('selesai', 'Selesai')
                    ], string='Status', readonly=True)
    nama_pengaju    = fields.Many2one(comodel_name='res.users',string='Nama Pengaju', readonly=True)
    nama_material   = fields.Char(string='Nama Material', readonly=True)
    merk            = fields.Char(string='Merk', readonly=True)
    tipe            = fields.Char(string='Tipe', readonly=True)
    negara_asal     = fields.Char(string='Negara Asal', readonly=True)
    kategori        = fields.Many2one(comodel_name='pdu.subkategori',string='Kategori', readonly=True)

    def _select(self):
        select_str = """
            SELECT 
                    a.id as id,
                    b.id as id_pengajuan,
                    b.name as nomor_pengajuan,
                    b.date as date,
                    c.name as vendor,
                    b.state as status,
                    b.create_uid as nama_pengaju,
                    a.name as nama_material,
                    a.categ_id as kategori,
                    a.merk as merk,
                    a.type as tipe,
                    a.country as negara_asal
                    
                FROM
                    product_material as a
                LEFT JOIN 
                    pdu_pengajuan_product_material_rel as d on d.product_material_id = a.id
                LEFT JOIN 
                    pdu_pengajuan as b on b.id = d.pdu_pengajuan_id 
                LEFT JOIN 
                    res_partner as c on c.id = b.partner_id
                ORDER BY id  
            """
        return select_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._select()))