# -*- coding: utf-8 -*-

import base64
import locale

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import tools
from odoo.exceptions import Warning
from odoo import api, fields , models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

import xlwt
from cStringIO import StringIO


class ExcelExportSummay(models.TransientModel):

    _name = "excel.export.summay"

    file = fields.Binary("Click On Save As Button To Download File",
                         readonly=True)
    name = fields.Char("Name" , size=32, default='Bank_summary.xls')

