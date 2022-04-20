from odoo import fields, api, models
from datetime import datetime
from dateutil.relativedelta import relativedelta

class MCSDashboardIframe(models.Model):
    _name = 'mcs.dashboard.iframe'
    _description = 'Dashboard Iframe'

    name = fields.Char('Name')