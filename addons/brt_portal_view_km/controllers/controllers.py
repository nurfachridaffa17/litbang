# -*- coding: utf-8 -*-
from odoo import http

class BrtPortalViewKm(http.Controller):
    @http.route('/jurnal', auth='public', website=True)
    def jurnal(self, data={},**kw):
       	nilai 		= '8'
        # DTJurnal 	= http.request.env['muk_dms.file']
        DTJurnal 	= http.request.env['jurnal']
        return http.request.render('brt_portal_view_km.jurnal', {
            'objects':  DTJurnal.sudo().search([]),
        })
       

    @http.route('/jurnal/data/<id>', auth='public', website=True)
    def list(self, id, **kw):
        # DETAILJurnal 	= http.request.env['muk_dms.file']
        DETAILJurnal 	= http.request.env['jurnal']
        return http.request.render('brt_portal_view_km.detail_jurnal', {
            'detjurnal':  DETAILJurnal.sudo().search([('id','=',id)]),
        })

#     @http.route('/brt_portal_view_km/brt_portal_view_km/objects/<model("brt_portal_view_km.brt_portal_view_km"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('brt_portal_view_km.object', {
#             'object': obj
#         })