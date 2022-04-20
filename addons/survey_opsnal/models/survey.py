from urlparse import urljoin
from odoo import api, fields, models, _
from odoo.addons.website.models.website import slug

class SurveyOpsnal(models.Model):
    _inherit = 'survey.survey'

    jenis_penelitian_id = fields.Many2one('survey.jenispenelitian', 'Jenis Penelitian', index=True)
    polda_id = fields.Many2one('survey.polda','Polda', index=True)
    polres_id = fields.Many2one('survey.polres', 'Polres', domain="[('polda_id', '=?', polda_id)]", index=True)
    tot_comp_survey = fields.Integer("Number of completed surveys", compute="_compute_survey_statistic", store=False)
    public_url = fields.Char("Public link", compute="_compute_survey_url", store=True)
    result_url = fields.Char("Results link", compute="_compute_survey_url", store=True)
    triwulan = fields.Selection([('Triwulan I','Triwulan I'), ('Triwulan II', 'Triwulan II'), ('Triwulan III', 'Triwulan III'), ('Triwulan IV', 'Triwulan IV')])

    @api.depends('title')
    def _compute_survey_url(self):
        base_url = '/' if self.env.context.get('relative_url') else self.env['ir.config_parameter'].get_param('web.base.url')
        for survey in self:
            survey.public_url = urljoin(base_url, "survey/start/%s" % (slug(survey)))
            survey.print_url = urljoin(base_url, "survey/print/%s" % (slug(survey)))
            survey.result_url = urljoin(base_url, "survey/results/%s" % (slug(survey)))
            survey.public_url_html = '<a href="%s">%s</a>' % (survey.public_url, _("Click here to start survey"))

class jenis_penelitian(models.Model):
    _name = 'survey.jenispenelitian'

    name = fields.Char("Jenis Penelitian")
    department_id = fields.Many2one("hr.department", 'Bidbag')

class survey_polda(models.Model):
    _inherit = "survey.polda"

    polres_ids = fields.One2many('survey.polres', 'polda_id')

class survey_polres(models.Model):
    _name = "survey.polres"
    _rec_name = "name"

    name = fields.Char('Polres')
    polda_id = fields.Many2one('survey.polda', 'Polda')

class surveyQuestion(models.Model):
    _inherit = 'survey.question'

    column_nb = fields.Selection(selection_add=[
        ('1', '8')
        ])
    # These options refer to col-xx-[12|6|4|3|2] classes in Bootstrap

class survey_user_input_line(models.Model):
    _inherit = "survey.user_input_line"

    page_id = fields.Many2one(related='question_id.page_id', string="Page", store=True)

