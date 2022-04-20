from odoo import models, fields, api, tools, _

class VSurveySurvey(models.Model):
    _name = 'v.survey.survey'
    _auto = False

    title = fields.Char('Title', index=True)
    page_ids = fields.One2many('survey.page', 'survey_id', string='Pages', copy=True)
    user_input_ids = fields.One2many('survey.user_input', 'survey_id', readonly=True)
    stage_id = fields.Many2one('survey.stage', readonly=True, index=True)
    description = fields.Html("Description", readonly=True, index=True)
    date_start = fields.Datetime('Waktu Mulai', readonly=True)
    date_end = fields.Datetime('Waktu Selesai', readonly=True)
    department_id = fields.Many2one('hr.department', readonly=True)
    responden = fields.Char('Responden', readonly=True)
    jenis_penelitian_id = fields.Many2one('survey.jenispenelitian', readonly=True)
    polda_id = fields.Many2one('survey.polda', readonly=True, index=True)
    polres_id = fields.Many2one('survey.polres', readonly=True, index=True)
    fungsi = fields.Many2one("fungsi", readonly=True, index=True)
    tahun = fields.Char('Tahun', readonly=True)
    tot_comp_survey = fields.Integer("Number of completed surveys", readonly=True)
    narasi = fields.Text('Narasi Admin', readonly=True)
    public_publish = fields.Boolean('Public Publish', readonly=True)
    public_url = fields.Char("Public link", readonly=True)
    result_url = fields.Char("Results link", readonly=True)
    triwulan = fields.Selection([('Triwulan I','Triwulan I'), ('Triwulan II', 'Triwulan II'), ('Triwulan III', 'Triwulan III'), ('Triwulan IV', 'Triwulan IV')], readonly=True)
    active = fields.Boolean("Active", default=True)

    def _select(self):
        select_str = """
            SELECT a.id,
    a.title,
    a.stage_id,
    a.description,
    a.date_start,
    a.date_end,
    a.department_id,
    a.responden,
    a.jenis_penelitian_id,
    a.polda_id,
    a.polres_id,
    a.fungsi,
    a.tahun,
    a.narasi,
    a.public_publish,
    a.public_url,
    a.result_url,
    a.triwulan,
    a.active,
    count(b.id) AS tot_comp_survey
   FROM survey_survey a
     LEFT JOIN survey_user_input b ON b.survey_id = a.id
   where b.state::text = 'done'::text and tahun = '2022'
  GROUP BY a.id, a.title, a.stage_id, a.description, a.date_start, a.date_end, a.department_id, a.responden, a.jenis_penelitian_id, a.polda_id, a.polres_id, a.fungsi, a.tahun, a.narasi, a.public_publish, a.public_url, a.result_url, a.triwulan, a.active
            """
        return select_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._select()))