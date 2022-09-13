from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyShortLink(models.Model):
    _inherit = 'survey.survey'

    short_link_tracker = fields.Char('Short Link', copy=False)

    def action_done_show_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Short Link Message'),
            'res_model': 'short.link.tracker.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'default_survey_id': self.id}
                }


    