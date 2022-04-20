from odoo import models, fields, api, tools, _

class VSurveyLabel(models.Model):
    _name = 'v.survey.label'
    _auto = False

    question_id = fields.Many2one('survey.question', string='Question', ondelete='cascade')
    question_id_2 = fields.Many2one('survey.question', string='Question 2', ondelete='cascade')
    value = fields.Char('Suggested value', translate=True, readonly=True)
    quizz_mark = fields.Float('Score for this choice', help="A positive score indicates a correct choice; a negative or null score indicates a wrong answer")
    survey_id = fields.Many2one('survey.survey', string='Survey', ondelete='cascade', readonly=True)
    page_id = fields.Many2one(related='question_id.page_id', readonly=True)

    def _select(self):
        select_str = """
                SELECT 
                    a.id as id,
                    a.quizz_mark as quizz_mark,
                    a.value as value,
                    a.question_id as question_id,
                    a.question_id_2 as question_id_2,
                    b.page_id as page_id,
                    c.survey_id as survey_id
                FROM
                    survey_label as a
                LEFT JOIN 
                    survey_question as b on b.id = a.question_id
                LEFT JOIN 
                    survey_page as c on c.id = b.page_id
                ORDER BY id 
            """
        return select_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._select()))