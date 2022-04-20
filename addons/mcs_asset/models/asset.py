# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models
from odoo import tools

STATE_COLOR_SELECTION = [
    ('0', 'Red'),
    ('1', 'Green'),
    ('2', 'Blue'),
    ('3', 'Yellow'),
    ('4', 'Magenta'),
    ('5', 'Cyan'),
    ('6', 'Black'),
    ('7', 'White'),
    ('8', 'Orange'),
    ('9', 'SkyBlue')
]

class asset_state(models.Model):
    """ 
    Model for asset states.
    """
    _name = 'asset.state'
    _description = 'State of Asset'
    _order = "sequence"
    name                = fields.Char('State', size=64, required=True, translate=True)
    sequence            = fields.Integer('Sequence', help="Used to order states.", default=1)
    state_color         = fields.Selection(STATE_COLOR_SELECTION, 'State Color')

    def change_color(self):
        color = int(self.state_color) + 1
        if (color>9): color = 0
        return self.write({'state_color': str(color)})


class asset_category(models.Model):
    _description = 'Asset Tags'
    _name = 'asset.category'
 
    @api.multi
    def name_get(self):
        res = []
        for record in self:
            tit = "[%s] %s" % (record.code, record.name)
            res.append((record.id, tit))
        return res
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            args = ['|',('code', operator, name),('name', operator, name)] + args
        categories = self.search(args, limit=limit)
        return categories.name_get() 
       
    code        = fields.Char(string='Kode Kategori', required=True, translate=True)
    name        = fields.Char('Nama Kategori', required=True, translate=True)
    parent_id   = fields.Many2one('asset.category', string="Parent", translate=True)
    asset_ids   = fields.Many2many('asset.asset', id1='category_id', id2='asset_id', string='Asset')


       
class asset_asset(models.Model):
    """
    Assets
    """
    _name = 'asset.asset'
    _description = 'Asset'
    _inherit = ['mail.thread']

    def _read_group_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        access_rights_uid = access_rights_uid or self.uid
        stage_obj = self.env['asset.state']
        order = stage_obj._order
        # lame hack to allow reverting search, should just work in the trivial case
        if read_group_order == 'stage_id desc':
            order = "%s desc" % order
        search_domain = []
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(search_domain, order=order, access_rights_uid=access_rights_uid)
        result = stage_obj.name_get(access_rights_uid, stage_ids)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))
        return result, {}    

    @api.model
    def _default_state(self):
        return self.env['asset.state'].search(
            [('name', '=', 'Baik'),('sequence', '=', 1)],limit=1)
        
    name                    = fields.Char('Nama Aset', size=64, required=True, translate=True)
    maintenance_state_id    = fields.Many2one('asset.state', 'State',default=_default_state)
    maintenance_state_color = fields.Selection(related='maintenance_state_id.state_color', selection=STATE_COLOR_SELECTION, string="Color", readonly=True)
    property_stock_asset    = fields.Many2one('bt.asset.location', "Lokasi Aset", domain=[('default_scrap', '=', False)])
    user_id                 = fields.Many2one('res.users', 'Penanggung Jawab', track_visibility='onchange')
    active                  = fields.Boolean('Active', default=True)
    asset_number            = fields.Char('Nomor Aset', size=64,required=True)
    note                    = fields.Text('Catatan')
    vendor_id               = fields.Many2one('res.partner', 'Supplier')
    asset_detail_ids        = fields.One2many('asset.detail','aset_id',ondelete='cascade')
    jenis                   = fields.Selection(string='Jenis', selection=[
                            ('R-4', 'R-4'),
                            ('R-2', 'R-2')])

    image                   = fields.Binary("Image")
    image_small             = fields.Binary("Small-sized image")
    image_medium            = fields.Binary("Medium-sized image")
    category_ids            = fields.Many2one(comodel_name='asset.category', required=True,string='Kategori')
    qty                     = fields.Integer(string='Kuantitas',compute='count_models')
    uom                     = fields.Many2one(comodel_name='product.uom',string='Satuan')    
    nilai                   = fields.Float(compute='compute_nilai', string='Nilai Aset')


    @api.depends('asset_detail_ids')
    def compute_nilai(self):
        for rec in self:
            for res in rec.asset_detail_ids:
                rec.nilai += res.harga_perolehan

    @api.depends('asset_detail_ids')
    def count_models(self):
        for data in self:
            kuantitas = len(data.asset_detail_ids)
            data.qty = kuantitas
    
 
    @api.multi
    def name_get(self):
        res = []
        for record in self:
            tit = "[%s] %s" % (record.asset_number, record.name)
            res.append((record.id, tit))
        return res
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            args = ['|',('asset_number', operator, name),('name', operator, name)] + args
        categories = self.search(args, limit=limit)
        return categories.name_get()   
    
    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(asset_asset, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(asset_asset, self).write(vals)

class asset_detail(models.Model):
    _name = 'asset.detail'
    _description = 'Asset Detail'
    
    aset_id                 = fields.Many2one(comodel_name='asset.asset')
    model                   = fields.Char('Merk/Type', size=64,required=True)
    tgl_perolehan           = fields.Date('Tanggal Perolehan', size=4)
    nopol                   = fields.Char('No Polisi')
    pemegang                = fields.Char('Pemegang')
    no_mesin                = fields.Char('No Mesin')
    serial                  = fields.Char('No Rangka')    
    maintenance_state_id    = fields.Many2one('asset.state', 'State',required=True)
    
    nup                     = fields.Integer(string='Nup')
    harga_perolehan         = fields.Float(string='Harga Perolehan')
    sumber_dana             = fields.Char(string='Sumber Dana')


