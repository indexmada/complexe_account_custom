# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
	_inherit = "account.move"

	location_state = fields.Selection([('local', 'Local'),('foreign','Etranger')],string="Location", default="local")