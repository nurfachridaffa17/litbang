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
    
    # @api.multi
    # def get_short_link_tracker(self):
    #     headers = {
    #             'access_token':'access_token_6c1ec5c1531a921f86160c766960d8fd2b892870',
    #             'Content-Type':'application/x-www-form-urlencoded',
    #             'charset':'utf-8'
    #     }

    #     base_url = '/' if self.env.context.get('relative_url') else self.env['ir.config_parameter'].get_param('web.base.url')
    #     for survey in self:
    #         survey.public_url = urljoin(base_url, "survey/start/%s" % (slug(survey)))
    #     data = { 
    #         "title": survey.public_url, 
    #         "url": survey.public_url
    #     }

    #     # the URL you want to shorten
    #     # make the POST request to get shortened URL for `url`
    #     try:
    #         shorten_res = requests.post("http://192.168.35.7:8097/api/survey/short_link", data=data, headers=headers)
    #         if shorten_res.status_code == 200:
    #             # if response is OK, get the shortened URL
    #             # self.short_link_tracker = shorten_res.json().get("short_url")
    #             data_url = shorten_res.json().get("data")
    #             self.short_link_tracker = data_url['short_url']

    #     except requests.exceptions.ConnectionError:
    #         shorten_res.status_code = "Connection refused"


    