# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BtAssetLocation(models.Model):   
    _name = "bt.asset.location"
    _description = "Asset Location" 
    
    name = fields.Char(string='Name', required=True)
    asset_ids = fields.One2many('asset.asset','property_stock_asset', string='Assets')
    default_scrap = fields.Boolean('Scrap')
    
 