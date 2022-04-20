# -*- coding: utf-8 -*-
from odoo import http
import json

class PDUController(http.Controller):
    @http.route('/pdu/pdu_api', type="http", methods=['get'], auth="public", website=True)
    def pdu_api(self, **get):
        if (get['username'] == "product") and (get['password'] == 'Iz3BwiHGwU1SjTBnnmIa1A=='):
            token = 1
        else:
            token = 0

        data_skpd = http.request.env['product.material'].sudo().search([])
        ids = []
        for dt in data_skpd:
            ids.append({
                'id'    : dt.id,
                'name'  : dt.name,
                'active'  : dt.active,
                'categ_id'  : dt.categ_id.name,
                'vendor_id'  : dt.vendor_id.name,
                'hasil_uji'  : dt.hasil_uji,
                'nilai_uji'  : dt.nilai_uji,
                'no_sertifikat'  : dt.no_sertifikat,
                'masa_sertifikat'  : dt.masa_sertifikat,
                'merk'  : dt.merk,
                'type'  : dt.type,
                'dimensi'  : dt.dimensi,
                'fitur'  : dt.fitur,
                'tahun_pembuatan'  : dt.tahun_pembuatan,
                'country'  : dt.country.name,
                'description'  : dt.description,
                'image'  : dt.image,
            })

        if token:
            return json.dumps({'result':'success', 'data': ids})
        else:
            return json.dumps({'result':'failed'})