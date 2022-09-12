from odoo import  models, fields, api, _
from urlparse import urljoin
import requests
import json
from odoo.exceptions import ValidationError

from odoo.addons.website.models.website import slug


class short_tracker_wizard(models.TransientModel):
    _name = 'short.link.tracker.wizard'
    _description = 'wizard untuk short link'

    short_link_tracker = fields.Char('Short Link Tracker', copy=False)
    survey_public_url = fields.Char("Public link", compute="_compute_survey_url")

    def _compute_survey_url(self):
        """ Computes a public URL for the survey """
        base_url = '/' if self.env.context.get('relative_url') else self.env['ir.config_parameter'].get_param('web.base.url')
        for survey in self:
            survey.survey_public_url = urljoin(base_url, "survey/start/%s" % (slug(survey)))
    
    @api.multi
    def get_short_link_tracker_wizard(self):
        headers = {
                'access_token':'access_token_6c1ec5c1531a921f86160c766960d8fd2b892870',
                'Content-Type':'application/x-www-form-urlencoded',
                'charset':'utf-8'
        }

        base_url = '/' if self.env.context.get('relative_url') else self.env['ir.config_parameter'].get_param('web.base.url')
        for survey in self:
            survey.survey_public_url = urljoin(base_url, "survey/start/%s" % (slug(survey)))
        data = { 
            "title": survey.survey_public_url, 
            "url": survey.survey_public_url
        }

        # the URL you want to shorten
        # make the POST request to get shortened URL for `url`
        try:
            shorten_res = requests.post("http://192.168.35.7:8097/api/survey/short_link", data=data, headers=headers)
            if shorten_res.status_code == 200:
                # if response is OK, get the shortened URL
                # self.short_link_tracker = shorten_res.json().get("short_url")
                data_url = shorten_res.json().get("data")
                # self.short_link_tracker = data_url['short_url']
        except requests.exceptions.ConnectionError:
            shorten_res.status_code = "Connection refused"
        self.ensure_one()
        self.short_link_tracker = data_url['short_url']
        return {
            "type": "ir.actions.do_nothing",
        }
        
        


    