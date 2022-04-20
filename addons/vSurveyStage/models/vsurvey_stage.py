from odoo import models, fields, api, tools, _

class VSurveyStage(models.Model):
    _name = 'v.survey.stage'
    _auto = False

    bidbag = fields.Char('Bid/Bag', readonly=True)
    title = fields.Char('Title', readonly=True, index=True)
    stage = fields.Char('Stage', readonly=True, index=True)
    public_publish = fields.Boolean('Public Publish', readonly=True)
    active = fields.Boolean('Active', readonly=True)

    def _select(self):
        select_str = """
                SELECT 
                    a.id as id,
                    c.name as bidbag,
                    a.title as title,
                    b.name as stage,
                    a.public_publish as public_publish,
                    a.active as active
                FROM
                    survey_survey as a
                LEFT JOIN 
                    survey_stage as b on b.id = a.stage_id
                LEFT JOIN 
                    hr_department as c on c.id = a.department_id
                ORDER BY id 
            """
        return select_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._select()))