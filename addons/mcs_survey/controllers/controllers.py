# -*- coding: utf-8 -*-
import werkzeug
import json
import base64
from random import randint
import os
# from docx import

import logging
# from pyPdf.utils import out
from string import join
_logger = logging.getLogger(__name__)

from odoo import http
from odoo.addons.website.controllers.main import Website

from odoo.http import request
from odoo.addons.website.models.website import slug
from odoo.addons.web.controllers.main import serialize_exception,content_disposition

from pprint import pprint
import json
from odoo.api import Environment as env

from odoo.http import Response
import urllib2
from math import ceil

from odoo import fields, http, SUPERUSER_ID
from odoo.tools import ustr

_logger = logging.getLogger(__name__)

class SurveyController(http.Controller):
    @http.route('/page/survey/allsurvey/', auth='public', website=True)
    def daftar_survey_allsurvey(self, **kw):
        Surveys = http.request.env['v.survey.survey']
        return http.request.render('mcs_survey.daftar_survey_all', {
            'surveys': Surveys.sudo().search([('department_id','=',(32,33,34,35)),('public_publish','=',True)])
        })

    @http.route('/page/survey/bidgasbin/', auth='public', website=True)
    def daftar_survey_bidgasbin(self, **kw):
        # print "bidgasbin"
        Surveys = http.request.env['survey.survey']
        return http.request.render('mcs_survey.daftar_survey_bidgasbin', {
            'surveys': Surveys.search([('department_id','=',33),('public_publish','=',True)])
        })
        
    @http.route('/page/survey/bidgassops/', auth='public', website=True)
    def daftar_survey_bidgassops(self, **kw):
        Surveys = http.request.env['v.survey.survey']
        return http.request.render('mcs_survey.daftar_survey_bidgassops', {
            'surveys': Surveys.sudo().search([('department_id','=',32),('public_publish','=',True)])
        })
    
    @http.route('/page/survey/bidrikwastu/', auth='public', website=True)
    def daftar_survey_bidrikwastu(self, **kw):
        Surveys = http.request.env['survey.survey']
        return http.request.render('mcs_survey.daftar_survey_bidrikwastu', {
            'surveys': Surveys.search([('department_id','=',34),('public_publish','=',True)])
        })
        
    @http.route('/page/survey/baglabtekpol/', auth='public', website=True)
    def daftar_survey_baglabtekpol(self, **kw):
        Surveys = http.request.env['survey.survey']
        return http.request.render('mcs_survey.daftar_survey_baglabtekpol', {
            'surveys': Surveys.search([('department_id','=',35),('public_publish','=',True)])
        })

    @http.route('/page/survey/dokinfo/', auth='public', website=True)
    def daftar_survey_dokinfo(self, **kw):
        Surveys = http.request.env['survey.survey']
        return http.request.render('mcs_survey.daftar_survey_dokinfo', {
            'surveys': Surveys.search([('department_id','=',40),('public_publish','=',True)])
        })

    @http.route(['/survey/report/<model("survey.survey"):survey>'],
                type='http', auth='user', website=True)
    def survey_reporting(self, survey, token=None, **post):
        '''Display survey Results & Statistics for given survey.'''
        # result_template = 'report'
        result_template = 'mcs_survey.result'
        current_filters = []
        filter_display_data = []
        filter_finish = False

        if not survey.user_input_ids or not [input_id.id for input_id in survey.user_input_ids if input_id.state != 'new']:
            result_template = 'mcs_survey.no_report'
        if 'finished' in post:
            post.pop('finished')
            filter_finish = True
        if post or filter_finish:
            filter_data = self.get_filter_data(post)
            current_filters = survey.filter_input_ids(filter_data, filter_finish)
            filter_display_data = survey.get_filter_display_data(filter_data)
        return request.render(result_template,
                                      {'survey': survey,
                                       'survey_dict': self.prepare_result_dict(survey, current_filters),
                                       'page_range': self.page_range,
                                       'current_filters': current_filters,
                                       'filter_display_data': filter_display_data,
                                       'filter_finish': filter_finish
                                       })
    def prepare_result_dict(self, survey, current_filters=None):
        """Returns dictionary having values for rendering template"""
        current_filters = current_filters if current_filters else []
        Survey = request.env['survey.survey']
        result = {'page_ids': []}
        for page in survey.page_ids:
            page_dict = {'page': page, 'question_ids': []}
            for question in page.question_ids:
                question_dict = {
                    'question': question,
                    'input_summary': Survey.get_input_summary(question, current_filters),
                    'prepare_result': Survey.prepare_result(question, current_filters),
                    'graph_data': self.get_graph_data(question, current_filters),
                }

                page_dict['question_ids'].append(question_dict)
            result['page_ids'].append(page_dict)
        return result

    def get_filter_data(self, post):
        """Returns data used for filtering the result"""
        filters = []
        for ids in post:
            #if user add some random data in query URI, ignore it
            try:
                row_id, answer_id = ids.split(',')
                filters.append({'row_id': int(row_id), 'answer_id': int(answer_id)})
            except:
                return filters
        return filters

    def page_range(self, total_record, limit):
        total = ceil(total_record / float(limit))
        return range(1, int(total + 1))

    def get_graph_data(self, question, current_filters=None):
        '''Returns formatted data required by graph library on basis of filter'''
        # TODO refactor this terrible method and merge it with prepare_result_dict
        current_filters = current_filters if current_filters else []
        Survey = request.env['survey.survey']
        result = []
        if question.type == 'multiple_choice':
            result.append({'key': ustr(question.question),
                           'values': Survey.prepare_result(question, current_filters)['answers']
                           })
        if question.type == 'simple_choice':
            result = Survey.prepare_result(question, current_filters)['answers']
        if question.type == 'matrix':
            data = Survey.prepare_result(question, current_filters)
            for answer in data['answers']:
                values = []
                for row in data['rows']:
                    values.append({'text': data['rows'].get(row), 'count': data['result'].get((row, answer))})
                result.append({'key': data['answers'].get(answer), 'values': values})
        return json.dumps(result)


class SSP_JSON():
    def data_output(self, columns, data):
#         pprint(data)
        out = []
          
        i = 0             
        while i < len(data):
            row = []
               
            j = 0             
            while j < len(columns):
                column = columns[j]
                #masukan kolom2
#                 pprint(data[i][column['db']])
                row.insert(column['dt'], data[i][column['db']])    
                j = j + 1
                
            #masukan baris2
            out.append(row)
            i = i + 1
         
#         return "total = " + str(len(columns))
#         pprint(out)
#         return data[1]['first_name']
        return out
    
    def limit(self, requesttt, columns):
        limit = '1000'

        if (requesttt['start'] and requesttt['length'] != -1):
            limit = " LIMIT " + str(int(requesttt['length'])) + " OFFSET " + str(int(requesttt['start'])) 

        return limit
    
    def order(self, requesttt, columns):
        order = ''
#         pprint(requesttt['order'])
        if (requesttt.get('order', False) and len(requesttt.get('order'))):
            orderBy = []
            dtColumns = self.pluck(columns, 'dt')
#             pprint(dtColumns)
            i = 0
#             pprint(len(requesttt.get('order')))
#             exit(0)
            while i < len(requesttt.get('order')):
                # Convert the column index into the column data property
                columnIdx = int(requesttt.get('order')[i]['column'])
                
                requestColumn = requesttt.get('columns')[columnIdx]
#                 pprint(requestColumn['data'])
                
                columnIdx = dtColumns.index(requestColumn['data'])
                        
                column = columns[columnIdx]
#                 pprint(columnIdx)
                
                
                if (requestColumn['orderable'] == True):
#                     pprint(requesttt.get('order')[i]['dir'])
                    if (requesttt.get('order')[i]['dir'] == 'asc'):
                        dire = 'ASC'
                    else:
                        dire = 'DESC'

                    orderBy.append(column['db'] + ' ' + dire)
                
                i = i + 1
                
#             pprint(orderBy)
            j_orderby = ', '.join(orderBy)
            order = 'ORDER BY ' + j_orderby 
#             pprint(order)
#             exit(0)

        return order
    
    
    def filter(self, requesttt, columns, bindings):
        globalSearch = []
        columnSearch = []
        dtColumns = self.pluck(columns, 'dt')

        if (requesttt['search'] and requesttt['search']['value'] != ''):
            stri = requesttt['search']['value']

            i = 0
            while i < len(requesttt['columns']):
                requestColumn = requesttt['columns'][i]
                columnIdx = dtColumns.index(requestColumn['data'])
                        
                column = columns[columnIdx]

                if (requestColumn['searchable'] == True):
#                     binding = self.bind(bindings, '%' + stri + '%', PDO::PARAM_STR)
                    # binding = self.bindi(bindings, '%' + stri + '%', '')
                    binding = "'%" + stri + "%'"
                    globalSearch.append("" + column['db'] + " LIKE " + binding)
                
                i = i + 1

        # Individual column filtering
        if (requesttt['columns']):
            i = 0
            while i < len(requesttt['columns']):
                requestColumn = requesttt['columns'][i]
                columnIdx = dtColumns.index(requestColumn['data'])
                
                column = columns[columnIdx]

                stri = requestColumn['search']['value']

                if (requestColumn['searchable'] == True and stri != ''):
#                     binding = self.bind(bindings, '%' + str + '%', PDO::PARAM_STR)
                    # binding = self.bindi(bindings, '%' + stri + '%', '')
                    binding = "'%" + stri + "%'"
                    columnSearch.append("" + column['db'] + " LIKE " + binding)
                    
                i = i + 1

        # Combine the filters into a single string
        where = ''

        if (len(globalSearch)):
            where = '(' + ' OR '.join(globalSearch) + ')'
        

        if (len(columnSearch)):
            if (where == ''):
                where = ' AND '.join(columnSearch)
            else:
                where = where + ' AND ' + ' AND '.join(columnSearch)
        

        if (where != ''):
            where = 'WHERE ' + where

        return where
    
    
    def simple(self, requesttt, table, primaryKey, columns):
        bindings = []
        
        
        # Build the SQL query string from the request
        limit = self.limit(requesttt, columns)
        order = self.order(requesttt, columns)
        where = self.filter(requesttt, columns, bindings)
        
        cr, uid, context = request.cr, request.uid, request.context

        # Main query to actually get the data
        sql = "SELECT " + ", ".join(self.pluck(columns, 'db')) + " FROM "+ table +" " + where + order + limit
        # print sql
        idp = context.get('id',[])
        cr.execute(sql, (idp))
        data = cr.dictfetchall()        

        # print_r(data)exit

        # Data set length after filtering
        sql = "SELECT COUNT("+primaryKey+") FROM  " + table + " " + where
        cr.execute(sql, (idp))
        resFilterLength = cr.fetchall()
        recordsFiltered = resFilterLength[0][0]

        # Total data set length
        sql = "SELECT COUNT(" + primaryKey + ") FROM " + table + " "
        cr.execute(sql, (idp))
        resTotalLength = cr.fetchall()
        recordsTotal = resTotalLength[0][0]

        #
             # Output
        #
        if (requesttt['draw']):
            draw = int(requesttt['draw'])
        else:
            draw = 0
               
        return {
            "draw" : draw,
            "recordsTotal" : int(recordsTotal),
            "recordsFiltered" : int(recordsFiltered),
            "data" : self.data_output(columns, data),
        }
    
    def complex(self, requesttt, table, primaryKey, columns, whereResult = None, whereAll = None):
        bindings = []

        localWhereResult = []
        localWhereAll = []
        whereAllSql = ''

        # Build the SQL query string from the request
        limit = self.limit(requesttt, columns)
        order = self.order(requesttt, columns)
        where = self.filter(requesttt, columns, bindings)

        whereResult = self._flatten(whereResult)
        whereAll = self._flatten(whereAll)

        if (whereResult):
            if (where):
                where = where + ' AND ' + whereResult 
            else:
                where = 'WHERE ' + whereResult
        

        if (whereAll):
            if (where):
                where = where + ' AND ' + whereAll 
            else:
                where = 'WHERE ' + whereAll

            whereAllSql = 'WHERE ' + whereAll
            
        cr, uid, context = request.cr, request.uid, request.context
        idp = context.get('id',[])
        
        # Main query to actually get the data
        sql = "SELECT `" + "`, `".join(self.pluck(columns, 'db')) + "` FROM `" + table + "` " + where + order + limit
        cr.execute(sql, (idp))
        data = cr.fetchall() 
        
        # Data set length after filtering
        sql = "SELECT COUNT(`"+primaryKey+"`) FROM  `" + table + "`" + where
        cr.execute(sql, (idp))
        resFilterLength = cr.fetchall()
        recordsFiltered = resFilterLength[0][0]
        
        # Total data set length
        sql = "SELECT COUNT(`" + primaryKey + "`) FROM `" + table + "`"
        cr.execute(sql, (idp))
        resTotalLength = cr.fetchall()
        recordsTotal = resTotalLength[0][0]

        #/*
             #* Output
        #*/
        if (requesttt['draw']):
            draw = int(requesttt['draw'])
        else:
            draw = 0
               
        return {
            "draw" : draw,
            "recordsTotal" : int(recordsTotal),
            "recordsFiltered" : int(recordsFiltered),
            "data" : self.data_output(columns, data),
        }
        

    # def fatal(self, msg):
    #     print json.dumps({"error" : msg})

    #     exit(0)

    
    def bindi(self, a, val, tipe):
        key = ':binding_' + len(a)

        a.append({'key' : key, 'val' : val,'type' : tipe})

        return key
    
    
    def pluck(self, a, prop):
        out = []

        i = 0
        while i < len(a):
            out.append(a[i][prop])
            
            i = i + 1
        
        return out
    
    
    def _flatten(self, a, joini = ' AND '):
        if (a is not None):
            return ''
        elif (a and isinstance(a, list)):
            return join(joini, a)
        
        return a
    
    
class Binary(http.Controller):
    @http.route('/web/binary/download_document', type='http', auth="public")
    @serialize_exception
    def download_document(self,model,field,id,filename=None, **kw):
        Survey = http.request.env[model]
        res = Survey.search([('id','=',id)])[0]
        filecontent = base64.b64decode(res.data_x)
        
        if not filecontent:
            return request.not_found()
        else:
            return http.request.make_response(filecontent,
                    [('Content-Type', 'application/octet-stream'),
                     ('Content-Disposition', content_disposition(filename))])
                        