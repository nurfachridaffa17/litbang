from openerp import models, fields, api
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class survey_inovasi_rekayasa_teknologi(models.Model):
    _name = "survey.inovasi.rekayasa.teknologi"
    _description = "Inovasi dan Rekayasa Teknologi"
    _rec_name	= 'name'

    name = fields.Char('Name')
    spesifikasi_teknis = fields.Text('Spesifikasi Teknis')
    foto = fields.Binary('Photo')