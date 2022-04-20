from pyecharts import Radar
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class survey_survey(models.Model):
    _inherit = "survey.survey"

    @api.multi
    def download_excel(self):
        radar = Radar("Radar Chart", "A year's precipitation and evaporation",width=700,height=450)
        radar_data1 = [[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]]
        radar_data2 = [[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]]
        schema = [ 
            ("Jan", 5), ("Feb",10), ("Mar", 10),
            ("Apr", 50), ("May", 50), ("Jun", 200),
            ("Jul", 200), ("Aug", 200), ("Sep", 50),
            ("Oct", 50), ("Nov", 10), ("Dec", 5)
        ]
        radar.config(schema)
        radar.add("Precipitation",radar_data1)
        radar.add("Evaporation",radar_data2,item_color="#1C86EE")
        url = radar.render("Chart.html")

        return {
            'type': 'ir.actions.act_url',
            'url': '/'+url,            
            'target': 'new',
        }