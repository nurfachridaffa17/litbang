"""Part of odoo. See LICENSE file for full copyright and licensing details."""

import functools
import logging
import requests

from odoo import http
from odoo.addons.restful.common import (
    extract_arguments,
    invalid_response,
    valid_response,
)
from odoo.http import request

_logger = logging.getLogger(__name__)


def validate_token(func):
    """."""

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        access_token = request.httprequest.headers.get("access_token")
        if not access_token:
            return invalid_response(
                "access_token_not_found", "missing access token in request header", 401
            )
        access_token_data = (
            request.env["api.access_token"]
            .sudo()
            .search([("token", "=", access_token)], order="id DESC", limit=1)
        )

        if (
            access_token_data.find_one_or_create_token(
                user_id=access_token_data.user_id.id
            )
            != access_token
        ):
            return invalid_response(
                "access_token", "token seems to have expired or invalid", 401
            )

        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)

    return wrap


_routes = ["/api/<model>", "/api/<model>/<id>", "/api/<model>/<id>/<action>"]


class APIController(http.Controller):
    """."""

    def __init__(self):
        self._model = "ir.model"

    ################################################## SURVEYS ##########################################################

    @validate_token
    @http.route("/api/survey.survey", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'page_ids', 'stage_id', 'description', 'responden', 'date_start', 
                        'tot_comp_survey', 'date_end']

        custDomain = [("active", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))

            if id:
                domain = [("id", "=", int(id))]
                data = (request.env[_model.model].sudo().search_read(
                    domain = domain,
                    fields = fields,
                    offset = offset,
                    limit = limit,
                    order = order
                ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.polda", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_polda(self, id=None, **payload):
        model = "survey.polda"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'name', 'polres_ids']

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )
        
    @validate_token
    @http.route("/api/survey.polres", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_polres(self, id=None, **payload):
        model = "survey.polres"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'name', 'polda_id']

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.fungsi", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_fungsi(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'page_ids', 'stage_id', 'description', 'user_input_ids', 
                        'responden', 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'triwulan']
        custDomain = [
            ("department_id", "=", 32),
            ("polres_id", "=", int(payload["polres_id"])),
            ("active", "=", "1")
        ]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain 
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )
    

    @validate_token
    @http.route("/api/survey.fungsi_triwulan", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_fungsi_triwulan(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'page_ids', 'stage_id', 'description', 'user_input_ids', 
                        'responden', 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'triwulan']
        custDomain = [
            ("department_id", "=", 32),
            ("polres_id", "=", int(payload["polres_id"])),
            ("triwulan", "=", payload["triwulan"]),
            ("active", "=", "1")
        ]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain 
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.opsnal", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_opsnal(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'user_input_ids', 'tot_comp_survey',
                        'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'triwulan']
        custDomain = [("department_id", "=", 32), ("active", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )
    
    @validate_token
    @http.route("/api/survey.bidgasopsnal", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_bidgasopsnal(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'date_start', 'date_end', 'narasi', 'tot_comp_survey', 'department_id', 'responden'
                        , 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'public_url', 'result_url']
        custDomain = [("department_id", "=", 32), ("public_publish", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.gasbin", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_gasbin(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'date_start', 'date_end', 'narasi', 'tot_comp_survey', 'department_id', 'responden'
                        , 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'public_url', 'result_url']
        custDomain = [("department_id", "=", 33), ("public_publish", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.rikwastu", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_rikwastu(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'date_start', 'date_end', 'narasi', 'tot_comp_survey', 'department_id', 'responden'
                        , 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'public_url', 'result_url']
        custDomain = [("department_id", "=", 34), ("public_publish", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.labtekpol", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_labtekpol(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'date_start', 'date_end', 'narasi', 'tot_comp_survey', 'department_id', 'responden'
                        , 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'public_url', 'result_url']
        custDomain = [("department_id", "=", 35), ("public_publish", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.dokinfo", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_dokinfo(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'date_start', 'date_end', 'narasi', 'tot_comp_survey', 'department_id', 'responden'
                        , 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'public_url', 'result_url']
        custDomain = [("department_id", "=", 40), ("public_publish", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.survey/all", type="http", auth="none", methods=["GET"], csrf=False) #Keperluan Web
    def get_survey_survey_all(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'date_start', 'date_end', 'narasi', 'tot_comp_survey', 'department_id', 'responden'
                        , 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'public_url', 'result_url']
        custDomain = [("public_publish", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/all.survey", type="http", auth="none", methods=["GET"], csrf=False) #Keperluan Web
    def get_all_survey(self, id=None, **payload):
        model = "v.survey.stage"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'bidbag', 'title', 'stage', 'public_publish']
        custDomain = [("bidbag", "!=", "0"), ("active", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey/stage", type="http", auth="none", methods=["GET"], csrf=False) #Keperluan Web
    def get_survey_stage_id(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'stage_id', 'date_start', 'date_end', 'narasi', 'tot_comp_survey', 'department_id', 'responden'
                        , 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'public_url', 'result_url', 'description']
        custDomain = [("stage_id", "=", 6),("tahun", "=", "2022"), ("active", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))

            if id:
                domain = [("id", "=", int(id))]
                data = (request.env[_model.model].sudo().search_read(
                    domain = domain,
                    fields = fields,
                    offset = offset,
                    limit = limit,
                    order = order
                ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    
    @validate_token
    @http.route("/api/survey.all/notopsnal", type="http", auth="none", methods=["GET"], csrf=False) #Keperluan Web
    def get_not_opsnal(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'polda_id', 'polres_id', 'department_id', 'title', 'stage_id', 'tahun']
        custDomain = [("department_id", "!=", 32),
        ("active", "=", "1")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )
    
    @validate_token
    @http.route("/api/hasil.survey", type="http", auth="none", methods=["GET"], csrf=False)
    def get_hasil_survey(self, id=None, **payload):
        model = "v.survey.survey"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'title', 'page_ids', 'stage_id', 'description', 'user_input_ids', 
                        'responden', 'jenis_penelitian_id', 'polda_id', 'polres_id', 'fungsi', 'tahun', 'triwulan', 'department_id']
        custDomain = [
            ("active", "=", "1"),
            ("jenis_penelitian_id", "=", int(payload['jenis_penelitian_id'])),
            ("polda_id", "=", int(payload["polda_id"])),

        ]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain 
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/jenis.penelitian", type="http", auth="none", methods=["GET"], csrf=False)
    def get_jenis_penelitian(self, id=None, **payload):
        model = "survey.jenispenelitian"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id','name','department_id']
        custDomain = [
            ("id", "!=", (1,2)),

        ]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain 
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/hr.department", type="http", auth="none", methods=["GET"], csrf=False)
    def get_hr_department(self, id=None, **payload):
        model = "hr.department"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'name']
        custDomain = [('id', "in", (32,33,34,35,40))]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.question", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_question(self, id=None, **payload):
        model = "survey.question"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'question', 'description', 'type', 'survey_id', 'page_id', 'constr_mandatory', 'labels_ids', 'labels_ids_2',
                        'matrix_subtype', 'comments_allowed', 'comments_message', 'comment_count_as_answer']
        custDomain = [('survey_id', '=', int(payload["survey_id"]))]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.allquestion", type="http", auth="none", methods=["GET"], csrf=False)
    def get_all_question(self, id=None, **payload):
        model = "survey.question"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'question', 'description', 'type', 'survey_id', 'page_id', 'constr_mandatory', 
                        'matrix_subtype', 'comments_allowed', 'comments_message', 'comment_count_as_answer']

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.label", type="http", auth="none",methods=["GET"], csrf=False)
    def get_survey_question_label(self, id=None, **payload):
        model = "survey.label"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        custFields = ["id", "value", "question_id", "question_id_2"]
        custDomain = ["|", ("question_id", "=", int(payload["question_id"])), ("question_id_2", "=", int(payload["question_id_2"]))]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain=domain,
                fields=fields,
                offset=offset,
                limit=limit,
                order=order
            ))

            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry" % ioc_name
        )

    @validate_token
    @http.route("/api/survey/label", type="http", auth="none",methods=["GET"], csrf=False)
    def get_survey_label(self, id=None, **payload):
        model = "v.survey.label"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        custFields = ["id", "value", "question_id", "question_id_2", "page_id", "survey_id"]
        custDomain = [("survey_id", "=", int(payload["survey_id"]))]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain=domain,
                fields=fields,
                offset=offset,
                limit=limit,
                order=order
            ))

            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry" % ioc_name
        )
    
    @validate_token
    @http.route("/api/survey.all/labels", type="http", auth="none", methods=["GET"], csrf=False)
    def get_all_label(self, model=None, id=None, **payload):
        model = "survey.label"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        custFields = ["id", "value", "question_id", "question_id_2"]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.user_input", type="http", auth="none", methods=["GET"], csrf=False)
    def get_survey_answer(self, id=None, **payload):
        model = "survey.user_input"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'type', 'survey_id', 'page_id', 'date_create', 'state', 'result_url', 'print_url', 'quizz_score']
        custDomain = [('survey_id', '=', int(payload["survey_id"])), ('state', '=', 'done')]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.user_input", type="http", auth="none", methods=["POST"], csrf=False)
    def create_survey_answer(self, id=None, **payload):
        model = "survey.user_input"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        if _model:
            try:
                resource = request.env[_model.model].sudo().create(payload)
            except Exception as e:
                return invalid_response("params", e)
            else:
                data = {"id" : resource.id}
                if resource:
                    return valid_response(data)
                else:
                    return valid_response(data)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )
    
    @validate_token
    @http.route("/api/survey.user_input", type="http", auth="none", methods=['PUT'], csrf=False)
    def update_survey_answer_status(self, model=None, id=None, **payload):
        model = "survey.user_input"
        ioc_name = model
        try :
            _id = int(id)
        except Exception:
            return invalid_response(
                "Invalid object id",
                "Invalid literal %s for id with base" % _id
            )
        _model = (request.env[self._model].sudo().search([("model", "=", model)], limit=1))

        if not _model:
            return invalid_response(
                "Invalid object model",
                "The model %s is not available in the registry." % ioc_name,
                404
            )

        try:
            request.env[_model.model].sudo().browse(_id).write(payload)
        except Exception as e:
            return invalid_response("Exception", e)
        else:
            return valid_response(
                "update %s record with id %s successfully!" % (_model.model, _id)
            )

    @validate_token
    @http.route("/api/survey.user_input_line", type="http", auth="none", methods=["POST"], csrf=False)
    def fill_survey_question(self, id=None,**payload):
        model = "survey.user_input_line"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)

        if _model:
            try:
                resource = request.env[_model.model].sudo().create(payload)
            except Exception as e:
                return invalid_response("params", e)
            else:
                data = {"id" : resource.id}
                if resource:
                    return valid_response(data)
                else:
                    return valid_response(data)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )

    @validate_token
    @http.route("/api/survey/user_input_line", type="http", auth="none", methods=["GET"], csrf=False)
    def get_user_input_line(self, id=None, **payload):
        model = "v.survey.user.input.lines"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'survey_id', 'date_create', 'answer_type', 'value_text', 'user_input_id', 'question_id', 
                      'page_id', 'value_number', 'value_date', 'value_free_text', 'value_suggested', 'value_suggested_row', 'quizz_mark']
        custDomain = [('survey_id', '=', int(payload["survey_id"])),('user_input_id', '=', int(payload["user_input_id"])), ("state", "=", "done")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            order = "user_input_id, id"
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    @validate_token
    @http.route("/api/survey.user_input_line", type="http", auth="none", methods=["GET"], csrf=False)
    def get_responden_answer(self, id=None, **payload):
        model = "v.survey.user.input.lines"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'survey_id', 'date_create', 'answer_type', 'value_text', 'user_input_id', 'question_id', 
                      'page_id', 'value_number', 'value_date', 'value_free_text', 'value_suggested', 'value_suggested_row', 'quizz_mark']
        custDomain = [('survey_id', '=', int(payload["survey_id"])), ("state", "=", "done")]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            order = "user_input_id, id"
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )

    ################################################## PDU ##########################################################

    @validate_token
    @http.route("/api/pdu.pengajuan", type="http", auth="none", methods=["GET"], csrf=False)
    def get_pdu(self, id=None, **payload):
        model="v.pdu.pengajuan"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)

        custFields = ['id_pengajuan', 'date', 'nomor_pengajuan', 'vendor', 'status', 'nama_pengaju', 'nama_material', 'kategori', 'merk', 'tipe', 'negara_asal']
        custDomain = [("status", "!=", ("selesai"))]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            try:
                data = (request.env[_model.model].sudo().search_read(
                    domain=domain,
                    fields=fields,
                    offset=offset,
                    limit=limit,
                    order=order
                ))
                return valid_response(data)
            except Exception as e:
                return invalid_response("Exception", e)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )
    
    @validate_token
    @http.route("/api/pdu.pengajuan/pencarian", type="http", auth="none", methods=["GET"], csrf=False)
    def get_pdu_pencarian(self, id=None, **payload):
        model="v.pdu.pengajuan"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)

        custFields = ['id_pengajuan', 'date', 'nomor_pengajuan', 'vendor', 'status', 'nama_pengaju', 'nama_material', 'kategori', 'merk', 'tipe', 'negara_asal']
        custDomain = [("status", "!=", ("selesai")),('nomor_pengajuan', '=', payload["nomor_pengajuan"])]

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            domain = custDomain
            try:
                data = (request.env[_model.model].sudo().search_read(
                    domain=domain,
                    fields=fields,
                    offset=offset,
                    limit=limit,
                    order=order
                ))
                return valid_response(data)
            except Exception as e:
                return invalid_response("Exception", e)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )
        
    ################################################## TNDE ##########################################################

    @validate_token
    @http.route("/api/surat.masuk", type="http", auth="none", methods=["GET"], csrf=False)
    def get_surat_masuk(self, id=None, **payload):
        model="surat_masuk_fix"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)

        custFields = ['id', 'no_agenda', 'kategori_id', 'jenis_surat', 'name', 'tujuan_surat', 'perihal', 'sifat_surat', 'tgl_diterima', 'tgl_surat', 'tindakan', 'state']

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            try:
                data = (request.env[_model.model].sudo().search_read(
                    domain=domain,
                    fields=fields,
                    offset=offset,
                    limit=limit,
                    order=order
                ))
                return valid_response(data)
            except Exception as e:
                return invalid_response("Exception", e)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )
    
    @validate_token
    @http.route("/api/surat.keluar", type="http", auth="none", methods=["GET"], csrf=False)
    def get_surat_keluar(self, id=None, **payload):
        model="v.surat.keluar"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)

        custFields = ['id', 'jenis_surat', 'kepada', 'konseptor', 'perihal', 'tindakan', 'kd_klasifikasi', 'lampiran_srt_msk', 'tgl_surat', 'state', 'penandatangan']

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            try:
                data = (request.env[_model.model].sudo().search_read(
                    domain=domain,
                    fields=fields,
                    offset=offset,
                    limit=limit,
                    order=order
                ))
                return valid_response(data)
            except Exception as e:
                return invalid_response("Exception", e)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )
        
    
    ################################################## DEFAULT ##########################################################

    @validate_token
    @http.route(_routes, type="http", auth="none", methods=["GET"], csrf=False)
    def get(self, model=None, id=None, **payload):
        ioc_name = model
        model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        if model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            try:
                data = (
                    request.env[model.model]
                    .sudo()
                    .search_read(
                        domain=domain,
                        fields=fields,
                        offset=offset,
                        limit=limit,
                        order=order,
                    )
                )
                return valid_response(data)
            except Exception as e:
                return invalid_response("Exception", e)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )

    @validate_token
    @http.route(_routes, type="http", auth="none", methods=["POST"], csrf=False)
    def create(self, model=None, id=None, **payload):
        """Create a new record.
        Basic sage:
        import requests

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'charset': 'utf-8',
            'access-token': 'access_token'
        }
        data = {
            'name': 'Babatope Ajepe',
            'country_id': 105,
            'child_ids': [
                {
                    'name': 'Contact',
                    'type': 'contact'
                },
                {
                    'name': 'Invoice',
                   'type': 'invoice'
                }
            ],
            'category_id': [{'id': 9}, {'id': 10}]
        }
        req = requests.post('%s/api/res.partner/' %
                            base_url, headers=headers, data=data)

        """
        ioc_name = model
        model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        if model:
            try:
                resource = request.env[model.model].sudo().create(payload)
            except Exception as e:
                return invalid_response("params", e)
            return {"id": resource.id}
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )

    @validate_token
    @http.route(_routes, type="http", auth="none", methods=["PUT"], csrf=False)
    def put(self, model=None, id=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response(
                "invalid object id", "invalid literal %s for id with base " % id
            )
        _model = (
            request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        )
        if not _model:
            return invalid_response(
                "invalid object model",
                "The model %s is not available in the registry." % model,
                404,
            )
        try:
            request.env[_model.model].sudo().browse(_id).write(payload)
        except Exception as e:
            return invalid_response("exception", e.name)
        else:
            return valid_response(
                "update %s record with id %s successfully!" % (_model.model, _id)
            )

    @validate_token
    @http.route(_routes, type="http", auth="none", methods=["DELETE"], csrf=False)
    def delete(self, model=None, id=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response(
                "invalid object id", "invalid literal %s for id with base " % id
            )
        try:
            record = request.env[model].sudo().search([("id", "=", _id)])
            if record:
                record.unlink()
            else:
                return invalid_response(
                    "missing_record",
                    "record object with id %s could not be found" % _id,
                    404,
                )
        except Exception as e:
            return invalid_response("exception", e.name, 503)
        else:
            return valid_response("record %s has been successfully deleted" % record.id)

    @validate_token
    @http.route(_routes, type="http", auth="none", methods=["PATCH"], csrf=False)
    def patch(self, model=None, id=None, action=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response(
                "invalid object id", "invalid literal %s for id with base " % id
            )
        try:
            record = request.env[model].sudo().search([("id", "=", _id)])
            _callable = action in [
                method for method in dir(record) if callable(getattr(record, method))
            ]
            if record and _callable:
                # action is a dynamic variable.
                getattr(record, action)()
            else:
                return invalid_response(
                    "missing_record",
                    "record object with id %s could not be found or %s object has no method %s"
                    % (_id, model, action),
                    404,
                )
        except Exception as e:
            return invalid_response("exception", e, 503)
        else:
            return valid_response("record %s has been successfully patched" % record.id)


################################################## Link Tracker ##########################################################

    @validate_token
    @http.route("/api/link.tracker", type="http", auth="none", methods=["GET"], csrf=False)
    def get_link_tracker(self, model=None, id=None, **payload):
        model = "link.tracker"
        ioc_name = model
        _model = request.env[self._model].sudo().search([("model", "=", model)], limit=1)
        
        custFields = ['id', 'count', 'url', 'title']

        if _model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            fields = custFields
            data = (request.env[_model.model].sudo().search_read(
                domain = domain,
                fields = fields,
                offset = offset,
                limit = limit,
                order = order
            ))
            
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name
        )
