# -*- coding: utf-8 -*-
from odoo import http

# class Tnde(http.Controller):
#     @http.route('/tnde/tnde/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnde/tnde/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnde.listing', {
#             'root': '/tnde/tnde',
#             'objects': http.request.env['tnde.tnde'].search([]),
#         })

#     @http.route('/tnde/tnde/objects/<model("tnde.tnde"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnde.object', {
#             'object': obj
#         })