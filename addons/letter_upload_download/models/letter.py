from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
    
class Letter(models.Model):
    _name = "letter"
    _rec_name = "ltr_type"

    ltr_type = fields.Char(string='Letter Type')
    document = fields.Binary(string='Document')
    document_name = fields.Char(string='Document Name')
 
class HR(models.Model):
    _inherit = "hr.employee"

    letter = fields.Many2one("letter", string="Surat")
    
    @api.multi
    def download(self):
        path = "/web/binary/download_document?"
        model = "letter"
        letter_id = self.letter.id
        filename = self.letter.document_name

        url = path + "model={}&id={}&filename={}".format(
            model, letter_id, filename)

        return {
            'type' : 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            'tag': 'reload',
        }