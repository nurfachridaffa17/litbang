from odoo import api, fields, models, _
import requests
from urlparse import urljoin
from odoo.addons.website.models.website import slug
import json

class ShortLink(models.Model):
    _inherit = 'survey.survey'

    short_link = fields.Char("Short Link Bitly", copy=False)

    @api.multi
    def get_short_link(self):
        headers = {
            'Authorization': "Bearer 5ee973c184fbf07736927dfb3fc0d99305b69f07",
            'Content-Type': 'application/json',
        }

        base_url = '/' if self.env.context.get('relative_url') else self.env['ir.config_parameter'].get_param('web.base.url')
        for survey in self:
            survey.public_url = urljoin(base_url, "survey/start/%s" % (slug(survey)))
        data = { "long_url": survey.public_url, "domain": "bit.ly", "group_guid": "Bl2hezAlUlU" }

        # the URL you want to shorten
        # make the POST request to get shortened URL for `url`
        try:
            shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", data=json.dumps(data), headers=headers)
            if shorten_res.status_code == 200:
                # if response is OK, get the shortened URL
                self.short_link = shorten_res.json().get("link")
        except requests.exceptions.ConnectionError:
            shorten_res.status_code = "Connection refused"
