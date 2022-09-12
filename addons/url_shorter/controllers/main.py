# -*- coding: utf-8 -*-
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from odoo import http, fields


class UrlShorterController(http.Controller):
    
    @http.route('/s/<string:token>', type='http', auth='public')
    def shorter(self, token, **kw):
        # Needs sudo to be able to read and write due to ir.rule
        UrlShort = http.request.env['url.shorter'].sudo()
        UrlRedirect = http.request.env['url.shorter.redirect'].sudo()
        short = UrlShort.search([('token', '=', token), ('active', '=', True)], limit=1)
        if short:
            UrlRedirect.create({
                'url_shorter_id': short.id,
                'accessed': fields.datetime.now(),
                'source_ip': http.request.httprequest.environ['REMOTE_ADDR']
            })
            return redirect(short.long_url)
        else:
            raise NotFound()
