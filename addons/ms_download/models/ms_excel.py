import xlwt
from xlwt import Workbook 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class survey_survey(models.Model):
    _inherit = "survey.survey"

    @api.multi
    def download_excel(self):
        wb = Workbook()
        sheet = wb.add_sheet("Details", cell_overwrite_ok=True)
        header_font = xlwt.Font()
        header_font.name = 'Arial'
        header_font.bold = True
        header_style = xlwt.XFStyle()
        header_style.font = header_font

        id_survey = self.id

        self.env.cr.execute("""
                                SELECT row_number() OVER (ORDER BY sequence, question_id) as id, * from
                                (SELECT DISTINCT a.value_suggested_row, c.type, c.id as question_id, 
                                c.sequence, c.question, b.value
                                from survey_user_input_line a
                                LEFT JOIN survey_label b on b.id = a.value_suggested_row 
                                LEFT JOIN survey_question c on c.id = a.question_id
                                where survey_id = %s
                                ORDER BY sequence, question_id) as quest
                            """,(int(id_survey),))
        question_query = self.env.cr.dictfetchall()
        question_id = [x['id'] for x in question_query]
            
        col = 0
        for x in question_query:
            q1 = str(x['question'])
            q2 = str(x['value'])
            if str(x['type']) == 'matrix':
                # value = str(x['question']).encode('ascii','ignore').decode('ascii')+" ["+str(x['value'])+"]"
                value = q1 +" ["+ q2 +"]"
            else:
                value = q1
            sheet.write(0, question_id[col]-1, value, header_style) 
            col += 1

        self.env.cr.execute("""
                                WITH survey as (  
                                    WITH cte_survey AS ( 
                                    SELECT 
                                    user_input_id,
                                    sequence, 
                                    question_id,
                                    type,
                                    matrix_subtype,
                                    question,
                                    matrix_question_id,
                                    matrix_questions,
                                    COALESCE(value_text, value_free_text, value_date::text, value_number::text, value) AS all_value
                                    FROM(
                                    SELECT 
                                    a.id, 
                                    a.user_input_id,
                                    d.sequence,
                                    d.id as question_id, 
                                    d.type,
                                    d.matrix_subtype,
                                    d.question, 
                                    a.value_suggested_row,
                                    c.id as matrix_question_id,
                                    c.value as matrix_questions, 
                                    a.value_suggested,
                                    b.value,
                                    a.value_text, 
                                    a.value_free_text,
                                    a.value_date,
                                    a.value_number
                                    FROM survey_user_input_line a 
                                    LEFT JOIN survey_label b on b.id = a.value_suggested
                                    LEFT JOIN survey_label c on c.id = a.value_suggested_row
                                    LEFT JOIN survey_question d on d.id = a.question_id
                                    LEFT JOIN survey_user_input e on e.id = a.user_input_id
                                    WHERE a.survey_id = %s
                                    AND e.state = 'done') as TempTable)
                                        SELECT
                                        *
                                        FROM cte_survey 
                                        WHERE (matrix_subtype != 'multiple')
                                        AND type != 'multiple_choice'

                                        UNION

                                        SELECT
                                        user_input_id,
                                        sequence,
                                        question_id,
                                        type,
                                        matrix_subtype,
                                        question,
                                        matrix_question_id,
                                        matrix_questions,
                                        STRING_AGG(all_value, ',')
                                        FROM cte_survey
                                        WHERE type = 'matrix'
                                        AND matrix_subtype = 'multiple'
                                        GROUP BY user_input_id, sequence, question_id, type, question, matrix_subtype,
                                        question,
                                        matrix_question_id,
                                        matrix_questions)
                                , survey2 as (
                                    WITH cte_survey2 AS ( 
                                    SELECT 
                                    user_input_id, 
                                    sequence,
                                    question_id,
                                    type,
                                    matrix_subtype,
                                    question,
                                    matrix_question_id,
                                    matrix_questions,
                                    COALESCE(value_text, value_free_text, value_date::text, value_number::text, value) AS all_value
                                    FROM(
                                    SELECT 
                                    a.id, 
                                    a.user_input_id,
                                    d.sequence,
                                    d.id as question_id, 
                                    d.type,
                                    d.matrix_subtype,
                                    d.question, 
                                    a.value_suggested_row,
                                    c.id as matrix_question_id,
                                    c.value as matrix_questions, 
                                    a.value_suggested,
                                    b.value,
                                    a.value_text, 
                                    a.value_free_text,
                                    a.value_date,
                                    a.value_number
                                    FROM survey_user_input_line a 
                                    LEFT JOIN survey_label b on b.id = a.value_suggested
                                    LEFT JOIN survey_label c on c.id = a.value_suggested_row
                                    LEFT JOIN survey_question d on d.id = a.question_id
                                    LEFT JOIN survey_user_input e on e.id = a.user_input_id
                                    WHERE a.survey_id = %s
                                    AND e.state = 'done') as TempTable2)
                                    
                                    SELECT
                                    *
                                    FROM cte_survey2 
                                    WHERE (matrix_subtype != 'multiple')
                                    AND type != 'multiple_choice'

                                    UNION

                                    SELECT
                                    user_input_id,
                                    sequence,
                                    question_id,
                                    type,
                                    matrix_subtype,
                                    question,
                                    matrix_question_id,
                                    matrix_questions,
                                    STRING_AGG(all_value, ',')
                                    FROM cte_survey2
                                    WHERE type = 'multiple_choice'
                                    GROUP BY user_input_id, sequence, question_id, type, question, matrix_subtype,
                                    question,
                                    matrix_question_id,
                                    matrix_questions ) 

                                SELECT DENSE_RANK() OVER (ORDER BY sequence,question_id, matrix_question_id) as id, * from(
                                SELECT * FROM survey2
                                UNION
                                SELECT * FROM survey
                                ORDER BY question_id, matrix_question_id, user_input_id) as united_table
                             """,(int(id_survey),int(id_survey)))
        answer_query = self.env.cr.dictfetchall()

        idx_answer = [x['id'] for x in answer_query]
        row = 1
        for x in answer_query:
            col = int(x['id'])
            counter = idx_answer.count(col)
            value = str(x['all_value'])
            sheet.write(row, col-1, value) 
            if row < counter:
                row += 1
            else:
                row = 1
            
        wb.save('/home/sippol/odoo/custom-addons/ms_download/static/doc/SurveyResult.xls')
        return {
            'type': 'ir.actions.act_url',
            'url': '/ms_download/static/doc/SurveyResult.xls',            
            'target': 'new',
        }
