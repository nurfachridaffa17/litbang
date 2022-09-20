from odoo import  models, fields, api, _
from urlparse import urljoin
import requests
import json
from odoo.exceptions import ValidationError
import datetime


class short_tracker_wizard(models.TransientModel):
    _name = 'short.link.tracker.wizard'
    _description = 'wizard untuk short link'

    survey_id = fields.Many2one(
        'survey.survey',
        string='Survey'
        )

    token = fields.Char(
        required=True,
        string="Judul Survey"
        )
    
    expiration_date = fields.Date(
        default=lambda self: datetime.date.today() + datetime.timedelta(days=7)
    )   

    
    @api.multi
    def get_short_link_tracker_wizard(self, data_url):
        lst = ['/', '>', '<', ' ', ';', ':', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '?', ',', '.', '[', ']', '{', '}']

        if not any(x in lst for x in list(self.token)):
            headers = {
                'access_token':'access_token_6c1ec5c1531a921f86160c766960d8fd2b892870',
                'Content-Type':'application/x-www-form-urlencoded',
                'charset':'utf-8'
            }
            data = { 
                "long_url": self.survey_id.public_url, 
                "token": self.token,
                "expiration_date" : self.expiration_date
            }
            try:
                shorten_res = requests.post("http://192.168.7.1:8097/api/survey/short_link", data=data, headers=headers)
                if shorten_res.status_code == 200:
                    data_url = shorten_res.json().get("data")
            except requests.exceptions.ConnectionError:
                shorten_res.status_code = "Connection refused"
            same_data = self.env['url.shorter'].search([('token', '=', self.token)], limit=1)
            if same_data:
                raise ValidationError("Token is already exist")
            self.survey_id.write({
                'short_link_tracker' : data_url['short_url']
            })
            return True
        else:
            raise ValidationError("There is symbols in custom link like <, !, &, -, _, ?, {, )")

                
        
        


    