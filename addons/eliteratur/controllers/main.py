# -*- coding: utf-8 -*-
from odoo import http

class eliteratur(http.Controller):

    @http.route('/eliteratur', auth='public', website=True)
    def eliteratur(self, data={},**kw):
        nilai       = '8'
        # DTeliteratur  = http.request.env['muk_dms.file']
        DTeliteratur    = http.request.env['eliteratur']
        DTkategori    = http.request.env['eliteratur.kategori']
        return http.request.render('eliteratur.eliteratur', {
            'objects':  DTeliteratur.sudo().search([]),
            'kategori':  DTkategori.sudo().search([('active','=',True)]),
        })

       
    @http.route('/eliteratur/kategori/data/<id>', auth='public', website=True)
    def list_kategori(self, id, **kw):
        # DETAILeliteratur  = http.request.env['muk_dms.file']
        DTkategori    = http.request.env['eliteratur.kategori']
        DETAILeliteratur    = http.request.env['eliteratur']
        return http.request.render('eliteratur.eliteratur', {
            'objects':  DETAILeliteratur.sudo().search([('topic_id.id','=',id)]),
            'kategori':  DTkategori.sudo().search([('active','=',True)]),
        })

    @http.route('/eliteratur/data/<id>', auth='public', website=True)
    def list(self, id, **kw):
        # DETAILeliteratur  = http.request.env['muk_dms.file']
        DETAILeliteratur    = http.request.env['eliteratur']
        return http.request.render('eliteratur.detail_eliteratur', {
            'deteliteratur':  DETAILeliteratur.sudo().search([('id','=',id)]),
        })