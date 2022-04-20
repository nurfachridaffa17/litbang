from odoo import models, fields, api, _

class product_material(models.Model):
    _name = "product.material"
    _inherit = ['mail.thread']

    name = fields.Char('Nama Material', index=True, required=True, translate=True)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the product without removing it.")
    image = fields.Binary("Image", attachment=True, help="This field holds the image used as image for the product, limited to 1024x1024px.")
    categ_id = fields.Many2one('pdu.subkategori', 'Kategori', required=True, help="Select category for the current product")
    vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", required=True)
    hasil_uji = fields.Selection([('Lulus','Lulus'),('Tidak Lulus','Tidak Lulus')], string='Hasil Uji', required=False)
    nilai_uji = fields.Integer('Nilai Akhir', required=False)
    pengujian_ids = fields.One2many(comodel_name='pdu.pengujian', inverse_name='product_id', string='Sertifikat', readonly=True)
    no_sertifikat = fields.Char('No. Sertifikat', required=False)
    masa_sertifikat = fields.Date('Masa Sertifikat', required=False)
    merk = fields.Char('Merk', required=False)
    type = fields.Char('Type', required=False)
    dimensi = fields.Char('Dimensi', required=False)
    fitur = fields.Char('Fitur', required=False)
    tahun_pembuatan = fields.Char('Tahun Pembuatan', required=False)
    country = fields.Many2one(string='Negara Asal', comodel_name='res.country', required=False)
    description = fields.Html('Deskripsi Material', required=False)