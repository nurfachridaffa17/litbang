from odoo import models, fields, api, _


class ShareLink(models.Model):
    _inherit = 'survey.survey'

    @api.multi
    def send_msg(self):
        message = self.short_link
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_message': message }
                }
