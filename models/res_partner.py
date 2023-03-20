# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
	_inherit = "res.partner"

	nif = fields.Char("NIF")
	stat = fields.Char("STAT")
	social_reason = fields.Char("Raison Sociale")