# -*- coding: utf-8 -*-
import string
import random
import datetime

try:
    from geoip import geolite2
    geolite2.lookup('127.0.0.1') # Check if lookup is available
except (ImportError, RuntimeError):
    geolite2 = False

from odoo import models, api, fields


class UrlShorter(models.Model):
    _name = 'url.shorter'
    _sql_constraints = [
        ('token_uniq', 'unique(token)', 'Token must be unique!')
        ]

    name = fields.Char()

    token = fields.Char(
        required=True,
        default=lambda self: self._generate_token()
        )

    long_url = fields.Char(
        required=True,
        string='Long URL'
        )

    short_url = fields.Char(
        compute='_compute_short_url',
        string='Short URL'
        )

    redirect_number = fields.Integer(
        string='Redirects',
        compute='_compute_redirect_number'
        )

    redirect_ids = fields.One2many(
        comodel_name='url.shorter.redirect',
        inverse_name='url_shorter_id'
    )

    active = fields.Boolean(
        default=True
        )

    expiration_date = fields.Date(
        default=lambda self: datetime.date.today() + datetime.timedelta(days=7)
    )

    @api.multi
    @api.depends('token')
    def _compute_short_url(self):
        """Creates short url based on token"""
        SysParameters = self.env['ir.config_parameter']
        base_url = SysParameters.search([('key', '=', 'web.base.url')], limit=1).value
        for record in self:
            record.short_url = '%s/s/%s' % (base_url, record.token)

    @api.multi
    @api.depends('redirect_ids')
    def _compute_redirect_number(self):
        """Computes number of redirects"""
        for record in self:
            record.redirect_number = len(record.redirect_ids)

    @api.onchange('token')
    def _onchange_token(self):
        if not self.token:
            self.token = self._generate_token()

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = vals['token']
        return super(UrlShorter, self).create(vals)

    @api.multi
    def write(self, vals):
        super(UrlShorter, self).write(vals)
        for record in self:
            if len(record.name) == 0:
                record.write({'name': record.token})
        return True

    @api.multi
    def action_new_token(self):
        for record in self:
            record.write({
                'token': self._generate_token()
                })
        return True

    @api.multi
    def toggle_active(self):
        for record in self:
            record.write({
                'active': not record.active,
            })
        return True

    @api.multi
    def renew(self):
        return self.write({
            'expiration_date': datetime.datetime.now() + datetime.timedelta(days=7),
            'active': True
            })

    @api.model
    def archive_expired(self):
        today = fields.date.today()
        self.search([('expiration_date', '<', today), ('active', '=', True)]).write({'active': False})
        return True


    def _generate_token(self):
        domain = []
        if self.token:
            domain = [('token', '!=', self.token)]
        while True:
            token = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            if self.search_count([('token', '=', token)] + domain) == 0:
                break
        return token

class Redirects(models.Model):
    _name = 'url.shorter.redirect'
    _order = 'accessed desc'

    url_shorter_id = fields.Many2one(
        comodel_name='url.shorter',
        string='Shorted URL',
        readonly=True
    )

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Source country',
        readonly=True
    )

    source_ip = fields.Char(
        readonly=True
    )

    accessed = fields.Datetime(
        readonly=True
    )

    @api.multi
    def map_ip(self):
        if geolite2:
            for record in self:
                match = geolite2.lookup(record.source_ip)
                if match:
                    country = self.env['res.country'].search([('code', '=', match.country)], limit=1)
                    if country:
                        record.write({'country_id': country.id})
