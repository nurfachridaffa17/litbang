from odoo import models, fields, api, exceptions, _
from openerp import models, fields, api
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning
import xlwt
import cStringIO
from cStringIO import StringIO
import base64
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.workbook import Workbook

# import selenium.webdriver as webdriver
# import selenium.webdriver.support.ui as ui
# from selenium.webdriver.common.keys import Keys
# from time import sleep
# import string
# from docx import Document
# from docx.shared import Inches
import urllib2
import numpy as np
import collections
import webbrowser
import urllib2


from odoo import models, fields, api
import locale
from dateutil.relativedelta import relativedelta
from openerp import tools
from openerp import api, fields , models, _

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class survey_survey(models.Model):
    _inherit = "survey.survey"


    department_id   = fields.Many2one('hr.department','Department', index=True)
    narasi          = fields.Text('Narasi Admin')
    public_publish  = fields.Boolean('Public Publish', default=True)
    polda_id        = fields.Many2one('survey.polda','Polda', index=True)
    date_start  = fields.Datetime('Waktu Mulai', required=True)
    date_end    = fields.Datetime('Waktu Selesai', required=True)
        
    generate        = fields.Selection([('Sudah', 'Sudah'),('Belum', 'Belum')], string='Generate', default='Belum')
    report_generate_stat  = fields.Char(string='Generate Status', size=4)
    tahun       = fields.Char(string='Tahun', size=4)
    link_sheet_1       = fields.Char(string='Report Sheet 1' )
    link_sheet_2       = fields.Char(string='Report Sheet 2' )
    responden   = fields.Char(string='Responden')
    kelompok    = fields.Char(string='Kelompok')
    data_x      = fields.Binary(string='File', readonly=True)
    
    @api.onchange('date_start')
    def check_date_start_change(self):
        if (self.date_start):
            d_to = datetime.strptime(self.date_start,"%Y-%m-%d %H:%M:%S")            
            y = d_to.year
            self.tahun = y

    @api.multi
    def publish_to_public(self):
        if not self.narasi:
            raise Warning('PERINGATAN...!! Narasi Admin belum diisi');
        else:
            self.public_publish = True

    def act_link(self): 
        ids = self.id
        url = str('http://puslitbang.polri.go.id:8081/brt-api/generate/excell') + "/" +str(ids)
        print('======= URL =========='), url
        link = str(url)
        return{
            'type'      : 'ir.actions.act_url',
            'url'       : link,
            'target'    : 'new'
            }

    @api.multi
    def action_result_survey_admin(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': "Results of the Survey",
            'target': 'self',
            'url': self.with_context(relative_url=True).result_url
        }
        
    # @api.multi
    # def action_result_survey(self):
    #     if not self.narasi:
    #         raise Warning('Narasi Admin belum diisi');
    #     else:
    #         self.ensure_one()
    #         return {
    #             'type': 'ir.actions.act_url',
    #             'name': "Results of the Survey",
    #             'target': 'self',
    #             'url': self.with_context(relative_url=True).result_url
    #         }
    
    @api.multi
    def action_link_mulai_survey(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': "Results of the Survey",
            'target': 'self',
            'url': self.with_context(relative_url=True).public_url
        }
    
    wbf = {}
    @api.multi
    def get_rekap(self):
        id_survey = self.id

        query_where = ' 1=1 '
        if id_survey :
            query_where += " AND a.survey_id = %s" % id_survey

        query = """
            SELECT b.*
            FROM
                survey_page a
            INNER JOIN survey_question b ON b.page_id=a.id
            WHERE %s
        """ % query_where
        self._cr.execute(query)
        val = self._cr.fetchone()
        print(val)
        
        
        return 
    
    @api.multi
    def add_workbook_format(self, workbook):      
        self.wbf['header'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFDB','font_color': '#000000'})
        self.wbf['header'].set_border()

        self.wbf['header_no'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFDB','font_color': '#000000'})
        self.wbf['header_no'].set_border()
        self.wbf['header_no'].set_align('vcenter')
                
        self.wbf['footer'] = workbook.add_format({'align':'left'})
        
        self.wbf['content_datetime'] = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})
        self.wbf['content_datetime'].set_left()
        self.wbf['content_datetime'].set_right()
                
        self.wbf['content_date'] = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        self.wbf['content_date'].set_left()
        self.wbf['content_date'].set_right() 
        
        self.wbf['title_doc'] = workbook.add_format({'bold': 1,'align': 'left'})
        self.wbf['title_doc'].set_font_size(12)
        
        self.wbf['company'] = workbook.add_format({'align': 'left'})
        self.wbf['company'].set_font_size(11)
        self.wbf['company'].set_bold(True)
        
        self.wbf['content'] = workbook.add_format()
        self.wbf['content'].set_left()
        self.wbf['content'].set_right() 
        
        self.wbf['content_float'] = workbook.add_format({'align': 'right','num_format': '#,##0.00'})
        self.wbf['content_float'].set_right() 
        self.wbf['content_float'].set_left()

        self.wbf['content_number'] = workbook.add_format({'align': 'right'})
        self.wbf['content_number'].set_right() 
        self.wbf['content_number'].set_left() 
        self.wbf['content_number'].set_num_format('#,##0')
        
        self.wbf['content_percent'] = workbook.add_format({'align': 'right','num_format': '0.00%'})
        self.wbf['content_percent'].set_right() 
        self.wbf['content_percent'].set_left() 
                
        self.wbf['total_float'] = workbook.add_format({'bold':1,'bg_color': '#FFFFDB','align': 'right','num_format': '#,##0.00'})
        self.wbf['total_float'].set_top()
        self.wbf['total_float'].set_bottom()            
        self.wbf['total_float'].set_left()
        self.wbf['total_float'].set_right()         
        
        self.wbf['total_number'] = workbook.add_format({'align':'right','bg_color': '#FFFFDB','bold':1})
        self.wbf['total_number'].set_top()
        self.wbf['total_number'].set_bottom()            
        self.wbf['total_number'].set_left()
        self.wbf['total_number'].set_right()
        
        self.wbf['total'] = workbook.add_format({'bold':1,'bg_color': '#FFFFDB','align':'center'})
        self.wbf['total'].set_left()
        self.wbf['total'].set_right()
        self.wbf['total'].set_top()
        self.wbf['total'].set_bottom()
        
        self.wbf['header_detail_space'] = workbook.add_format({})
        self.wbf['header_detail_space'].set_left()
        self.wbf['header_detail_space'].set_right()
        self.wbf['header_detail_space'].set_top()
        self.wbf['header_detail_space'].set_bottom()
                
        self.wbf['header_detail'] = workbook.add_format({'bg_color': '#E0FFC2'})
        self.wbf['header_detail'].set_left()
        self.wbf['header_detail'].set_right()
        self.wbf['header_detail'].set_top()
        self.wbf['header_detail'].set_bottom()
                        
        return workbook
    
    @api.multi
    def action_excel_survey_oooooold(self):
        id_survey               = self.id
        judul_survey            = self.title
        print('=================================================================='),id_survey
        self.env.cr.execute("""
                            SELECT b.question as question,b.description as description, b.id as id
                            FROM survey_page a
                            INNER JOIN survey_question b ON b.page_id=a.id
                            WHERE a.survey_id = %s
                            ORDER BY b.page_id,question ASC
                            -- ORDER BY b.page_id,a.id ASC
                            """,(id_survey,))
        vals  = self.env.cr.dictfetchall()


        company_name            = self.env['res.company'].search([], order="id asc", limit=1)

        book                    = xlwt.Workbook()
        sheet1                  = book.add_sheet("Detail Report E-Survey")
        sheet2                  = book.add_sheet("Report E-Survey")
        sheet3                  = book.add_sheet("Log Date History")
        
        font                    = xlwt.Font()
        font.bold               = True
        header                  = xlwt.easyxf('font: bold 1, height 280')
        style                   = xlwt.easyxf('align: wrap yes')
        for x in range(0,41):
            sheet1.col(x).width = 6000
            sheet2.col(x).width = 6000
            sheet3.col(x).width = 6000
        borders                 = xlwt.Borders()
        borders.top             = xlwt.Borders.MEDIUM
        borders.bottom          = xlwt.Borders.MEDIUM
        border_style            = xlwt.XFStyle()  # Create Style
        border_style.borders    = borders
        border_style1           = xlwt.easyxf('font: bold 1')
        border_style1.borders   = borders
        
        # Head
        # sheet1.write(1, 0, company_name.name)
        # sheet1.write(2, 0, 'REKAPITULASI SURVEY')
        # sheet1.write(3, 0, judul_survey)

        sheet1.write(1, 0, company_name.name, header) 
        sheet1.write(2, 0, 'REKAPITULASI SURVEY', header) 
        sheet1.write(3, 0, judul_survey, header) 
        sheet1.write(4, 0, ' ') 
        sheet1.write(5, 0, ' ') 

        

        row       = 6       
        no_urut   = 0       
        for val in vals :
            pertanyaan     = str(val['question']).encode('ascii','ignore').decode('ascii')

            sheet1.write(row, no_urut, pertanyaan, border_style1) 

            query2_where = ' 1=1 '
            if str(val['id']) :
                query2_where += " AND b.question_id = %s" % str(val['id'])
            
            query2 = """
                SELECT b.value_suggested as value_suggested,b.value_text as value_text, c.value as value, b.value_free_text as value_free_text
                FROM survey_user_input a
                INNER JOIN survey_user_input_line b ON b.user_input_id=a.id
                LEFT JOIN survey_label c ON c.id=b.value_suggested
                WHERE %s
                ORDER BY a.id,value_suggested ASC
            """ % query2_where
            #print query2
            self._cr.execute(query2)
            rsj = self._cr.fetchall()
            
            # print '================', rsj

            rows = row + 1
           


            for DT in rsj :
                if DT[0] :
                    value_suggested = str(DT[0])
                else:
                    value_suggested = " "
                if DT[1] :
                    value_text = str(DT[1])
                else:
                    value_text = " "
                if DT[2] :
                    value = str(DT[2])
                else:
                    value = " "
                if DT[3] :
                    value_free_text = str(DT[3])
                else:
                    value_free_text = " "
                #value_text      = str(DT[0])
                #value_suggested = str(DT[1])
                #value           = str(DT[2])
                #value_free_text = str(DT[3])

                print('================ value_text'), value_text
                print('================ value_suggested'), value_suggested
                print('================ value'), value
                print('================ value'), value_free_text
                
                # if(value_text):
                #     jawaban = ' '+ value 
                # else:
                #     jawaban = ' '+ value_suggested
                
                jawaban1    = ' '+ value_text + ' '+ value + ' ' + value_free_text
                #jawaban2    = jawaban1.replace('None', ' ')
                jawaban     = jawaban1.encode('ascii','ignore').decode('ascii')
                # print '=================================================',jawaban
                # print '=================================================',pertanyaan
                sheet1.write(rows, no_urut, jawaban) 
                rows += 1
            no_urut += 1


        sheet2.write(1, 0, company_name.name, header) 
        sheet2.write(2, 0, 'REKAPITULASI SURVEY', header) 
        sheet2.write(3, 0, judul_survey, header) 
        sheet2.write(4, 0, ' ') 
        sheet2.write(5, 0, ' ') 

        row       = 6       
        no_urut   = 0       
        for val in vals :
            pertanyaan     = str(val['question']).encode('ascii','ignore').decode('ascii')

            sheet2.write(row, no_urut, pertanyaan, border_style1) 

            query2_where = ' 1=1 '
            if str(val['id']) :
                query2_where += " AND b.question_id = %s" % str(val['id'])
            
            query2 = """
                SELECT b.value_suggested as value_suggested,b.value_text as value_text, c.value as value, b.value_free_text as value_free_text
                FROM survey_user_input a
                INNER JOIN survey_user_input_line b ON b.user_input_id=a.id
                LEFT JOIN survey_label c ON c.id=b.value_suggested
                WHERE %s
                ORDER BY a.id,value_suggested ASC
            """ % query2_where
            #print query2
            self._cr.execute(query2)
            rsjs = self._cr.fetchall()
            
            # print '================', rsj

            rows = row + 1
           


            for DTs in rsjs :
                value_text      = str(DTs[0])
                value_suggested = str(DTs[1])
                value1          = str(DTs[2])
                value_free_text = str(DTs[3])

                # print '================ value_text', value_text
                # print '================ value_suggested', value_suggested
                # print '================ value', value
                # print '==================================================================-======'
                
                # if(value_text):
                #     jawaban = ' '+ value 
                # else:
                #     jawaban = ' '+ value_suggested
                if(value1 =='None'):
                    value = ''
                else:
                    value  = value1[0:2]
                # value    = value2.replace('', '')

                jwb1    = ' '+ value_suggested.replace('None', ' ') + ' '+ value.replace('None', ' ') + ' ' + value_free_text.replace('None', ' ')
                jwb2    = jwb1.replace(')', ' ')
                jwb     = jwb2.encode('ascii','ignore').decode('ascii')
                # print '================================================= JAWABAN 1',jwb
                # print '=================================================',pertanyaan
                sheet2.write(rows, no_urut, jwb) 
                rows += 1
            no_urut += 1

        
        sheet3.write(1, 0, company_name.name, header) 
        sheet3.write(2, 0, 'Riwayat Tanggal Pengisian Survey', header) 
        sheet3.write(3, 0, judul_survey, header) 
        sheet3.write(4, 0, ' ') 
        sheet3.write(5, 0, ' ') 

        self.env.cr.execute("""
                            SELECT b.question as question,b.description as description, b.id as id
                            FROM survey_page a
                            INNER JOIN survey_question b ON b.page_id=a.id
                            WHERE a.survey_id = %s
                            ORDER BY b.page_id,question ASC
                            LIMIT 1
                            -- ORDER BY b.page_id,a.id ASC
                            """,(id_survey,))
        vals666  = self.env.cr.dictfetchall()

        row       = 6       
        no_urut   = 0       
        for val in vals666 :
            pertanyaan     = str(val['question']).encode('ascii','ignore').decode('ascii')

            sheet3.write(row, no_urut, pertanyaan, border_style1) 

            query2_where = ' 1=1 '
            if str(val['id']) :
                query2_where += " AND b.question_id = %s" % str(val['id'])
            
            query2 = """
                SELECT b.value_suggested as value_suggested,b.value_text as value_text, c.value as value, b.value_free_text as value_free_text, b.date_create as tgl
                FROM survey_user_input a
                INNER JOIN survey_user_input_line b ON b.user_input_id=a.id
                LEFT JOIN survey_label c ON c.id=b.value_suggested
                WHERE %s
                ORDER BY a.id,value_suggested ASC
            """ % query2_where
            #print query2
            self._cr.execute(query2)
            rsjs = self._cr.fetchall()
            
            # print '================', rsj

            rows = row + 1

            for DTs in rsjs :
                value_text      = str(DTs[0])
                value_suggested = str(DTs[1])
                value1          = str(DTs[2])
                value_free_text = str(DTs[3])
                tgl 			= str(DTs[4])

                if(value1 =='None'):
                    value = ''
                else:
                    value  = value1[0:2]
                # value    = value2.replace('', '')

                jwb1    = tgl+' -- '+ value_suggested.replace('None', ' ') + ' '+ value.replace('None', ' ') + ' ' + value_free_text.replace('None', ' ')
                jwb2    = jwb1.replace(')', ' ')
                jwb     = jwb2.encode('ascii','ignore').decode('ascii')
                
                # print '================================================= JAWABAN 1',jwb
                # print '=================================================',pertanyaan
                sheet3.write(rows, no_urut, jwb) 
                rows += 1
            no_urut += 1

            
           
        # sheet1.write(row, 0, ' ') 

        # isi
        # sheet1.write(0, 1, 'ISBT DEHRADUN') 
        # sheet1.write(0, 2, 'SHASTRADHARA') 
        # sheet1.write(0, 3, 'CLEMEN TOWN') 
        # sheet1.write(0, 4, 'RAJPUR ROAD') 
        # sheet1.write(0, 5, 'CLOCK TOWER') 
        sec = str(datetime.now().strftime("%s"))
        # book.save('/home/puslitbang/odoonew/addons_polri/mcs_survey/static/doc/123.xls')
      
        time     = sec.encode('ascii','ignore').decode('ascii')
        judul     = str(self.title).encode('ascii','ignore').decode('ascii')
        
        book.save('/home/puslitbang/odoonew/addons_polri/mcs_survey/static/doc/'+time+'-' + judul+'.xls')
        

        # open(str(self.title)+'.docx', "wb")
        return {
            'type': 'ir.actions.act_url',
            # 'url': '/mcs_survey/static/doc/123.xls',            
            'url': '/mcs_survey/static/doc/'+time+'-' + judul+'.xls',            
            'target': 'new',
        }

    @api.multi
    def reset_report(self):
        self.link_sheet_1 = ''
        self.link_sheet_2 = ''
        self.generate = 'Belum'
        self.env.cr.execute("""DELETE FROM survey_tb_report_excell WHERE survey_id = '%s'""", (int(self.id),))
        self.env.cr.execute("""DELETE FROM survey_tb_report_excell_question WHERE survey_id = '%s'""", (int(self.id),))
        self.env.cr.commit()

    @api.multi
    def report_generate2222(self):
        self.generate = 'Sudah'
        id_survey = self.id
        DTPage = self.env["survey.page"].search([('survey_id','=',self.id)])
        no_urut_soal = 1
        for pg in DTPage :
            DTQuest = self.env["survey.question"].search([('page_id','=',pg.id)])
            for Que in DTQuest :
                # CEK APA DATA SUDAH ADA ATAU BELUM
                CEKDTTB = self.env["survey.tb_report_excell_question"].search([('question_id','=',Que.id),('survey_id','=',id_survey)])
                if CEKDTTB:
                    print('=========================== DATA SUDAH ADA')
                else:
                    self.env['survey.tb_report_excell_question'].create({
                        'question_id'   : Que.id,
                        'pertanyaan'    : Que.question,
                        'no_urut'       : no_urut_soal,
                        'survey_id'     : id_survey
                        })
                    print('=========================== DATA BELUM ADA ==================== NO URUT SOAL'),no_urut_soal 

                    DTResponden = self.env["survey.user_input"].search([('survey_id','=',id_survey)])
                    no_urut   = 0   
                    for Respon in DTResponden :
                        DTJwbanResponden = self.env["survey.user_input_line"].search([('user_input_id','=',Respon.id),('question_id','=',Que.id)])
                        # DTJwbanResponden = self.env["survey.user_input_line"].search([('user_input_id','=',Respon.id),('question_id','=',Que.id),('skipped','=','f')])
                        kolom = 1
                        for DTJwb in DTJwbanResponden :
                            if DTJwb:
                                if DTJwb.value_suggested:
                                    DTIsi_jwb   = self.env["survey.label"].search([('id','=',int(DTJwb.value_suggested))])
                                    jawabansh1  = DTIsi_jwb.value
                                    jawabansh2  = jawabansh1[0:1]
                                    pilihan     = 'Y'

                                else:
                                    jawabansh1  = '-'
                                    jawabansh2  = '-'
                                    pilihan     = 'T'
                                
                                jawaban_sheet1    = ' '+ str(jawabansh1) + ' '+ str(DTJwb.value_text) + ' ' + str(DTJwb.value_free_text)
                                jawaban_sheet2    = ' '+ str(jawabansh2) + ' '+ str(DTJwb.value_text) + ' ' + str(DTJwb.value_free_text)
                                jawaban_sheet1_a           = jawaban_sheet1.replace('False', ' ')
                                jawaban_sheet2_a           = jawaban_sheet2.replace('False', ' ')
                                jawaban_sheet1_fix     = jawaban_sheet1_a.encode('ascii','ignore').decode('ascii')
                                jawaban_sheet2_fix     = jawaban_sheet2_a.encode('ascii','ignore').decode('ascii')

                                self.env['survey.tb_report_excell'].create({
                                                                            'survey_id'         : id_survey,
                                                                            'question_id'       : Que.id,
                                                                            'pertanyaan'        : Que.question,
                                                                            'responden_id'      : Respon.id,
                                                                            'jawaban_sheet1'    : jawaban_sheet1_fix,
                                                                            'jawaban_sheet2'    : jawaban_sheet2_fix,
                                                                            'no_line'           : no_urut,
                                                                            'kolom'             : no_urut_soal,
                                                                            'skipped'           : str(DTJwb.skipped),
                                                                            'jwb_pilihan'       : pilihan
                                                                        }) 
                                kolom += 1

                            else:
                                kolom = no_urut+1
                                tdkjwb = '-'
                                self.env['survey.tb_report_excell'].create({
                                                                            'survey_id'         : id_survey,
                                                                            'question_id'       : Que.id,
                                                                            'pertanyaan'        : Que.question,
                                                                            'responden_id'      : Respon.id,
                                                                            'jawaban_sheet1'    : str(tdkjwb),
                                                                            'jawaban_sheet2'    : str(tdkjwb),
                                                                            'no_line'           : no_urut,
                                                                            'kolom'             : no_urut_soal,
                                                                            'skipped'           : 'f',
                                                                            'jwb_pilihan'       : pilihan
                                                                            }) 
                                kolom += 1

                        no_urut += 1
                    no_urut_soal += 1

    @api.multi
    def report_generate(self):
        self.generate   = 'Sudah'
        id_survey       = self.id
        status 			= str('done')
        DTPage          = self.env["survey.page"].search([('survey_id','=',self.id)])
        for pg in DTPage :
            DTQuest = self.env["survey.question"].search([('page_id','=',pg.id)])
            for Que in DTQuest :
                self.env['survey.tb_report_excell_question'].create({
                        'question_id'   : Que.id,
                        'pertanyaan'    : Que.question,
                        'survey_id'     : id_survey
                        })

                DTResponden = self.env["survey.user_input"].search([('survey_id','=',id_survey)])
                no_urut     = 0   
                for Respon in DTResponden :
                    DTJwbanResponden = self.env["survey.user_input_line"].search([('survey_id','=',id_survey),('user_input_id','=',Respon.id),('question_id','=',Que.id)],limit=1)
                    kolom = 1
                    if DTJwbanResponden:
                        if DTJwbanResponden.value_suggested:
                            DTIsi_jwb   = self.env["survey.label"].search([('id','=',int(DTJwbanResponden.value_suggested))])
                            jawabansh1  = DTIsi_jwb.value
                            jawabansh2  = jawabansh1[0:1]
                        else:
                            jawabansh1  = str(DTJwbanResponden.value_text) + ' ' + str(DTJwbanResponden.value_free_text)
                            jawabansh2  = str(DTJwbanResponden.value_text) + ' ' + str(DTJwbanResponden.value_free_text)
                                
                            jawaban_sheet1_a           = jawabansh1.replace('False', ' ')
                            jawaban_sheet2_a           = jawabansh2.replace('False', ' ')
                            jawaban_sheet1_fix         = jawaban_sheet1_a.encode('ascii','ignore').decode('ascii')
                            jawaban_sheet2_fix         = jawaban_sheet2_a.encode('ascii','ignore').decode('ascii')

                            self.env['survey.tb_report_excell'].create({
                                                                            'survey_id'         : id_survey,
                                                                            'question_id'       : Que.id,
                                                                            'pertanyaan'        : Que.question,
                                                                            'responden_id'      : Respon.id,
                                                                            'jawaban_sheet1'    : jawaban_sheet1_fix,
                                                                            'jawaban_sheet2'    : jawaban_sheet2_fix,
                                                                        }) 
                    else:
                        jawabansh1  = '(Tidak Menjawab)'
                        jawabansh2  = '(Tidak Menjawab)'
                        self.env['survey.tb_report_excell'].create({
                                                                    'survey_id'         : id_survey,
                                                                    'question_id'       : Que.id,
                                                                    'pertanyaan'        : Que.question,
                                                                    'responden_id'      : Respon.id,
                                                                    'jawaban_sheet1'    : str(jawabansh1),
                                                                    'jawaban_sheet2'    : str(jawabansh2),
                                                                    }) 
        self.link_sheet_1 = "http://puslitbang.polri.go.id:8081/brt-api/clean/cetak_excell1/"+str(self.id)
        self.link_sheet_2 = "http://puslitbang.polri.go.id:8081/brt-api/clean/cetak_excell2/"+str(self.id)

    @api.multi
    def cetak_excel_new(self):
        id_survey               = self.id
        judul_survey            = self.title
        company_name            = self.env['res.company'].search([], order="id asc", limit=1)

        book                    = xlwt.Workbook()
        sheet1                  = book.add_sheet("Detail Report E-Survey")
        sheet2                  = book.add_sheet("Report E-Survey")
        
        font                    = xlwt.Font()
        font.bold               = True
        header                  = xlwt.easyxf('font: bold 1, height 280')
        style                   = xlwt.easyxf('align: wrap yes')
        for x in range(0,41):
            sheet1.col(x).width = 6000
            sheet2.col(x).width = 6000
        borders                 = xlwt.Borders()
        borders.top             = xlwt.Borders.MEDIUM
        borders.bottom          = xlwt.Borders.MEDIUM
        border_style            = xlwt.XFStyle()  # Create Style
        border_style.borders    = borders
        border_style1           = xlwt.easyxf('font: bold 1')
        border_style1.borders   = borders
        
        sheet1.write(1, 0, company_name.name, header) 
        sheet1.write(2, 0, 'REKAPITULASI SURVEY', header) 
        sheet1.write(3, 0, judul_survey, header) 
        sheet1.write(4, 0, ' ') 
        sheet1.write(5, 0, ' ')

        rows            = 6
        rowsA           = 7
        no_urut         = 0
        DTPertanyaan    = self.env['survey.tb_report_excell_question'].search([('survey_id', '=', self.id)])
        rowsa           = rows + 1
        for val in DTPertanyaan :
            line        = 0 
            lines        = 7 
            baris       = rowsA +1      
            pertanyaan     = str(val.pertanyaan).encode('ascii','ignore').decode('ascii')

            sheet1.write(6, no_urut, pertanyaan, border_style1) 


            DTJawaban    = self.env['survey.tb_report_excell'].search([('question_id', '=', int(val.question_id)),('kolom', '=', val.no_urut)], order='no_line asc')
            for JW in DTJawaban :
                sheet1.write(lines, no_urut, JW.jawaban_sheet1) 
                lines += 1
            baris += 1
            line += 1
            rowsA += 1
            rows += 1
            no_urut += 1




        sheet2.write(1, 0, company_name.name, header) 
        sheet2.write(2, 0, 'REKAPITULASI SURVEY', header) 
        sheet2.write(3, 0, judul_survey, header) 
        sheet2.write(4, 0, ' ') 
        sheet2.write(5, 0, ' ')

        rows            = 6
        rowsA           = 7
        no_urut         = 0
        DTPertanyaan    = self.env['survey.tb_report_excell_question'].search([('survey_id', '=', self.id)])
        rowsa           = rows + 1
        for val in DTPertanyaan :
            line        = 0 
            lines        = 7 
            baris       = rowsA +1      
            pertanyaan     = str(val.pertanyaan).encode('ascii','ignore').decode('ascii')

            sheet2.write(6, no_urut, pertanyaan, border_style1) 
            # DTResponden    = self.env['survey.user_input'].search([('survey_id', '=', self.id)],order='id asc')
            # for RS in DTResponden :
                # print '=========================================== RESPONDEN ========== ',RS.id
            DTJawaban    = self.env['survey.tb_report_excell'].search([('question_id', '=', int(val.question_id)),('kolom', '=', val.no_urut)], order='no_line asc')
            for JW in DTJawaban :
                # print '=========== Row >',lines,'== kolom >>',no_urut,' ==== ',RS.id,' ======',pertanyaan,'======',JW.jawaban_sheet1
                sheet2.write(lines, no_urut, JW.jawaban_sheet2) 
                lines += 1
            baris += 1
            line += 1
            rowsA += 1
            rows += 1
            no_urut += 1

        
        sec         = str(datetime.now().strftime("%s"))
        time        = sec.encode('ascii','ignore').decode('ascii')
        judul       = str(self.title).encode('ascii','ignore').decode('ascii')
        nama_file   = time+'-' + judul+'.xls'




        # self.env['brt_tb.report'].create({'name':nama_file ,'id_survey':id_survey})
        
        book.save('/home/puslitbang/odoonew/addons_polri/mcs_survey/static/doc/'+nama_file)
        return {
            'type': 'ir.actions.act_url',
            'url': '/mcs_survey/static/doc/'+nama_file,            
            'target': 'new',
        }

    @api.multi
    def action_excel_survey(self):
        id_survey               = self.id
        judul_survey            = self.title
        status_generate         = self.report_generate_stat

        if status_generate  == 'Yes':
            ReportTB    = self.env['brt_tb.report'].search([('id_survey', '=', id_survey)],limit=1)
            file = str(ReportTB.name)

            nama_file     = file.encode('ascii','ignore').decode('ascii')
            print("============"),nama_file
            return {
                'type': 'ir.actions.act_url',
                'url': '/mcs_survey/static/doc/'+nama_file,            
                'target': 'new',
            }
        else:
            index = 1
            print('=================================================================='),id_survey
            #         select header dl
            self.env.cr.execute("""
                                SELECT
                                    "id"
                                FROM
                                    survey_user_input
                                WHERE
                                    survey_id = %s
                                AND "state" = 'done'
                                ORDER BY
                                    "id" ASC
                                """,(id_survey,))
            vals  = self.env.cr.dictfetchall()
            self.report_generate_stat  = 'Yes'
            company_name            = self.env['res.company'].search([], order="id asc", limit=1)

            book                    = xlwt.Workbook()
            sheet1                  = book.add_sheet("Detail Report E-Survey")
            sheet2                  = book.add_sheet("Report E-Survey")
            sheet3                  = book.add_sheet("Log Date History")
            
            font                    = xlwt.Font()
            font.bold               = True
            header                  = xlwt.easyxf('font: bold 1, height 280')
            style                   = xlwt.easyxf('align: wrap yes')
            for x in range(0,41):
                sheet1.col(x).width = 6000
                sheet2.col(x).width = 6000
                sheet3.col(x).width = 6000
            borders                 = xlwt.Borders()
            borders.top             = xlwt.Borders.MEDIUM
            borders.bottom          = xlwt.Borders.MEDIUM
            border_style            = xlwt.XFStyle()  # Create Style
            border_style.borders    = borders
            border_style1           = xlwt.easyxf('font: bold 1')
            border_style1.borders   = borders
            
            sheet1.write(1, 0, company_name.name, header) 
            sheet1.write(2, 0, 'REKAPITULASI SURVEY', header) 
            sheet1.write(3, 0, judul_survey, header) 
            sheet1.write(4, 0, ' ') 
            sheet1.write(5, 0, ' ') 

            row       = 6       
            no_urut   = 0   
            for val in vals :
                no_urut   = 0
                
                self._cr.execute("""
                                    SELECT
                                        x."id",
                                        x.question,
                                        (
                                            SELECT
                                                case
                                                    when (string_agg(y.value_text, ', ' ORDER BY y.question_id) is not NULL) AND (string_agg(y.value_text, ', ' ORDER BY y.question_id) != '') then string_agg(y.value_text, ', ' ORDER BY y.question_id)
                                                    when (string_agg(y.value_free_text, ', ' ORDER BY y.question_id) is not NULL) AND (string_agg(y.value_free_text, ', ' ORDER BY y.question_id) != '') then string_agg(y.value_free_text, ', ' ORDER BY y.question_id)
                                                    when (string_agg(y."value", ', ' ORDER BY y.question_id) is not NULL) AND (string_agg(y."value", ', ' ORDER BY y.question_id) != '') then string_agg(y."value", ', ' ORDER BY y.question_id)
                                                else 
                                                    '-'
                                                end AS nilai
                                            FROM
                                                    vw_survey_user_input y
                                            WHERE
                                                    y.question_id = x."id"
                                            AND y.user_input_id = %s
                                        )
                                    FROM vw_survey_question x
                                    WHERE survey_id = %s
                                    ORDER BY x."id"
                                    """,(val['id'],id_survey))
                rsj  = self.env.cr.dictfetchall()
                value = ""
                print('=========================== Header ==================================='),val['id']
                for DT in rsj :
                    
                    if DT['question'] :
                        pertanyaan = str(DT['question'])
                    else:
                        pertanyaan = " "

                    value = str(DT['nilai'])
                    
                    if index == 1:
                        row       = 6
                        soal      = pertanyaan.encode('ascii','ignore').decode('ascii')

                        sheet1.write(row, no_urut, soal, border_style1)
                        rows = row + 1 
                        if no_urut ==0:
                            # jawaban1    = str(val['id'])+'-'+value
                            jawaban1    = value
                        else:
                            jawaban1    = value

                        jawaban     = jawaban1.encode('ascii','ignore').decode('ascii')
                        sheet1.write(rows, no_urut, jawaban)
                    else:
                        if no_urut ==0:
                            jawaban1    = str(val['id'])+'-'+value
                        else:
                            jawaban1    = value

                        jawaban     = jawaban1.encode('ascii','ignore').decode('ascii')
                        sheet1.write(rows, no_urut, jawaban)
                        
                    no_urut += 1
                    # print '=========================== Done Cetak no_urut ==============================',no_urut
                    print('=========================== Done Cetak rows =============================='),rows
                    
                rows += 1
                index += 1
            
            sec = str(datetime.now().strftime("%s"))
            time     = sec.encode('ascii','ignore').decode('ascii')
            judul     = str(self.title).encode('ascii','ignore').decode('ascii')
            nama_file = time+'-' + judul+'.xls'

            self.env['brt_tb.report'].create({'name':nama_file ,'id_survey':id_survey})
            
            book.save('/home/puslitbang/odoonew/addons_polri/mcs_survey/static/doc/'+nama_file)
            return {
                'type': 'ir.actions.act_url',
                # 'url': '/mcs_survey/static/doc/123.xls',            
                'url': '/mcs_survey/static/doc/'+nama_file,            
                'target': 'new',
            }

    @api.multi
    def action_excel_survey_old(self):
        id_survey = self.id
        judul_survey = self.title

        query_where = ' 1=1 '
        if id_survey :
            query_where += " AND a.survey_id = %s" % id_survey

        query = """
            SELECT b.question,b.description,b.id
            FROM
                survey_page a
            INNER JOIN survey_question b ON b.page_id=a.id
            WHERE %s
            ORDER BY page_id,id
        """ % query_where
        self._cr.execute(query)
        vals = self._cr.fetchall()
        
        fp = StringIO()
        workbook = xlsxwriter.Workbook(fp)        
        workbook = self.add_workbook_format(workbook)
        wbf=self.wbf
        
        company_name = self.env['res.company'].search([], order="id asc", limit=1).name
        filename = judul_survey+'.xlsx'  
         
        #WKS 1
        worksheet = workbook.add_worksheet(judul_survey)
        # sheet2      = workbook.add_sheet(judul_survey)
        # Write some simple text.
        worksheet.write('A1', company_name , wbf['company'])
        worksheet.write('A2', 'REKAPITULASI SURVEY' , wbf['company'])
        worksheet.write('A3', judul_survey , wbf['company'])
         
        # Write some data headers.
        worksheet.write('A5', 'NO.', wbf['header'])
        #worksheet.write('B5', 'Nama Responden', wbf['header'])
        
        #listaz=list(string.ascii_uppercase)
        listaz=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
        # Menampilkan pertanyaan
        i = 1       
        for val in vals :
            kolom = listaz[i] + '5'             
            pertanyaan = ''
            if (val[0]):
                pertanyaan += str(val[0])
            
            if (val[1]):
                pertanyaan += ' '+str(val[1])
            
            question_id = val[2]
        #             print question_id
            #print pertanyaan
            #if (i==0):
            #    worksheet.write(kolom, 'No. ', wbf['header'])
            #else:
            worksheet.write(kolom, pertanyaan, wbf['header'])
            
            
            # Query jawaban
            query2_where = ' 1=1 '
            if question_id :
                query2_where += " AND b.question_id = %s" % question_id
            
            query2 = """
                SELECT b.value_text,b.value_suggested,c.value
                FROM
                    survey_user_input a
                INNER JOIN survey_user_input_line b ON b.user_input_id=a.id
                LEFT JOIN survey_label c ON c.id=b.value_suggested
                WHERE %s
            """ % query2_where
            #print query2
            self._cr.execute(query2)
            rsj = self._cr.fetchall()
            
            # Menampilkan pertanyaan
            row = 6
            no_urut = 1
            for rj in rsj :
                cell_jwb = listaz[i]+str(row)
                jwb = ''
                # jawaban text
                if (rj[0]):
                    jwb += str(rj[0])
                
                # jawaban pilihan ganda 1 jawaban
                if (rj[1]):
                    jwb += str(rj[2]) 
                    
                #if (i==0):
                cell_nourut = 'A'+str(row)
                worksheet.write(cell_nourut, no_urut , wbf['content_number'])
                #else:
                worksheet.write(cell_jwb, jwb , wbf['content'])                
                
                row += 1   
                no_urut += 1         
                              
                       
            i += 1
        workbook.close()
        out=base64.encodestring(fp.getvalue())
        self.write({'data_x':out})
        fp.close()

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=survey.survey&field=data_x&id=%s&filename=%s'%(self.id,filename),            
            'target': 'new',
        }
    
    @api.multi
    def action_survey_report(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': "Survey Results",
            'target': 'self',
            'url': self.report_url
        }
    
class survey_polda(models.Model):
    _name = "survey.polda"

    name = fields.Char('Name')

class brt_tb_report(models.Model):
    _name = "brt_tb.report"

    name         = fields.Char('Nama File')
    id_survey    = fields.Many2one('survey.survey','Survey')

class survey_user_input(models.Model):
    _inherit = 'survey.user_input'

    internal_note  = fields.Char(string='Internal Note')
    ref            = fields.Char(string='Ref')
    jumlah_jawaban = fields.Char(string='Jumlah Jawaban', compute='compute_jumlah_jawaban', store=False)
    cek_jawaban    = fields.Boolean(string='Cek Jawaban', compute='compute_cek_jawaban', default=False, store=True)
    no_tab         = fields.Char(string='Nomor Tab', compute='compute_no_tab')
    
    @api.multi
    @api.depends('user_input_line_ids')
    def compute_jumlah_jawaban(self):
        for x in self:
            i=0
            for z in x.user_input_line_ids:
                i += 1
            x.jumlah_jawaban = "%s" % i

    @api.multi
    @api.depends('ref','jumlah_jawaban')
    def compute_cek_jawaban(self):
        for x in self:
            if x.ref == x.jumlah_jawaban:
                x.cek_jawaban = True
            else:
                x.cek_jawaban = False
  
    @api.multi
    @api.depends('email')
    def compute_no_tab(self):
        for x in self:
            tab = self.env['survey.data_tab'].search([('no_imei','=',x.email)], limit=1)
            if tab:
                x.no_tab = tab.no_tab
              
class survey_data_tab(models.Model):
    _name = 'survey.data_tab'
    _rec_name = 'no_imei'
    
    no_imei = fields.Char(string='IMEI')
    no_tab = fields.Char(string='Nomor Tab')
    no_sn = fields.Char(string='Serial Number')
    no_koper = fields.Char(string='Nomor Koper')
    ref = fields.Char(string='Ref')
    internal_note = fields.Char(string='Internal Note')


class brt_tb_survey_report_excell(models.Model):
    _name = 'survey.tb_report_excell'
    
    survey_id = fields.Char(string='ID Survey')
    pertanyaan = fields.Char(string='pertanyaan')
    question_id = fields.Char(string='ID Question')
    responden_id = fields.Char(string='ID Responden')
    jawaban_sheet1 = fields.Char(string='Jawaban Sheet 1 ')
    jawaban_sheet2 = fields.Char(string='Jawaban Sheet 2 ')

class brt_tb_survey_report_excell_question(models.Model):
    _name = 'survey.tb_report_excell_question'
    
    question_id = fields.Many2one('survey.question', string="ID Question")
    pertanyaan = fields.Char(string='pertanyaan')
    survey_id = fields.Many2one('survey.survey', string="ID Survey")
    no_urut = fields.Integer(string='No Urut Soal')