from odoo import _, api, fields, models
from urlparse import urljoin
import requests
import json
from odoo.exceptions import ValidationError

from odoo.addons.website.models.website import slug


class linkUrlTracker(models.Model):
    _inherit = 'link.tracker'

    short_url = fields.Char(string='Tracked URL', compute='_compute_short_url')
    code = fields.Char(string='Short URL code', compute='_compute_code')

    @api.one
    def _compute_code(self):
        record = self.env['link.tracker.code'].search([('link_id', '=', self.id)], limit=1, order='id DESC')
        self.code = record.code

    @api.one
    @api.depends('code')
    def _compute_short_url(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        self.short_url = urljoin(base_url, '/r/%(code)s' % {'code': self.code})

class SurveyShortLink(models.Model):
    _inherit = 'survey.survey'

    short_link_tracker = fields.Char('Short Link Tracker', copy=False)

    def action_done_show_wizard(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Short Link Message'),
                'res_model': 'short.link.tracker.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                }


    