from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class LaporanBahanBaku(models.Model):
    _name = 'v.survey.user.input.lines'
    _auto = False

    survey_id = fields.Many2one(related='user_input_id.survey_id', readonly=True, index=True)
    page_id = fields.Many2one(related='question_id.page_id', readonly=True, index=True)
    date_create = fields.Datetime('Create Date', readonly=True)
    answer_type = fields.Selection([
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('free_text', 'Free Text'),
        ('suggestion', 'Suggestion')], readonly=True)
    value_text = fields.Char(readonly=True)
    user_input_id = fields.Many2one('survey.user_input', readonly=True, index=True)
    question_id = fields.Many2one('survey.question', readonly=True, index=True)
    value_number = fields.Float(readonly=True)
    value_date = fields.Datetime(readonly=True)
    value_free_text = fields.Text(readonly=True)
    value_suggested = fields.Many2one('survey.label', readonly=True)
    value_suggested_row = fields.Many2one('survey.label', readonly=True)
    quizz_mark = fields.Float(readonly=True)
    state = fields.Selection([
        ('new', 'Not started yet'),
        ('skip', 'Partially completed'),
        ('done', 'Completed')], readonly=True)
    value = fields.Char('Suggested value', translate=True, required=True)
    jenis_penelitian_id = fields.Many2one('survey.jenispenelitian', 'Jenis Penelitian')
    tahun = fields.Char(string='Tahun', size=4)

    def _select(self):
        select_str = """
            SELECT 
                a.id, 
                a.survey_id AS survey_id,
                a.page_id AS page_id,
                a.date_create AS date_create,
                a.answer_type AS answer_type,
                a.value_text AS value_text,
                a.user_input_id AS user_input_id,
                a.question_id AS question_id,
                a.value_number AS value_number,
                a.value_date AS value_date,
                a.value_free_text AS value_free_text,
                a.value_suggested AS value_suggested,
                c.value as value,
                a.value_suggested_row AS value_suggested_row,
                a.quizz_mark AS quizz_mark,
                b.state AS state,
                d.jenis_penelitian_id as jenis_penelitian_id,
                d.tahun as tahun
            """
        return select_str

    def _from(self):
        from_str = """ 
            FROM 
                survey_user_input_line a
            LEFT JOIN survey_user_input b on b.id = a.user_input_id
            LEFT JOIN survey_label c on c.id = a.value_suggested
            LEFT JOIN survey_survey d  on d.id = a.survey_id
            WHERE b.state = 'done'
            """
        return from_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as ( %s %s )""" % (self._table, self._select(), self._from()))