# -*- coding: utf-8 -*-
from odoo import http

# class SimRikwastu(http.Controller):
#     @http.route('/sim_rikwastu/sim_rikwastu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sim_rikwastu/sim_rikwastu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sim_rikwastu.listing', {
#             'root': '/sim_rikwastu/sim_rikwastu',
#             'objects': http.request.env['sim_rikwastu.sim_rikwastu'].search([]),
#         })

#     @http.route('/sim_rikwastu/sim_rikwastu/objects/<model("sim_rikwastu.sim_rikwastu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sim_rikwastu.object', {
#             'object': obj
#         })