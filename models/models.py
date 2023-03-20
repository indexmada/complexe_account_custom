# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AnnexeTVA(models.Model):
    _name = "annexe.tva.export"
    _description = "Un fichier excel à exporter depuis la comptabilité"

    date_from = fields.Date(string="De", help="Date début", required=True, default=fields.Date.today())
    date_to = fields.Date(string="A", help="Date fin", required=True, default=fields.Date.today())


    def export_xlsx(self):
        actions = {
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': '/web/binary/report/annexe_tva_report?date_from=' + format(self.date_from) +
                   "&date_to=" + format(self.date_to)
        }
        return actions