# -*- coding: utf-8 -*-
import xlsxwriter
import io
from odoo import http, fields, exceptions
from odoo.http import request
import base64
from dateutil.rrule import rrule, MONTHLY
import datetime
import calendar

COLUMN = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R']

class AnnexeTVAController(http.Controller):
    @http.route('/web/binary/report/annexe_tva_report', auth='public', website=True)
    def download_annexe_tva_report(self, date_from, date_to, **kw):
        filename = "annexe_tva.xlsx"
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet()
        
        # Styles
        top_header_format = workbook.add_format({'border':1,'bold':1,'font_size':'13px'})
        global_format = workbook.add_format({'font_size': '12px','border':1})

        # Header
        top_header_content = ['Fournisseur(F) Client(C) Débours(D)', 'Local(L) ou Etranger(E)',
                    'NIF (Online) (10 Chiffres)', 'Raison Sociale', 'STAT', 'Adresse', 
                    'Montant HT(Ar)', 'TVA (Ar)', 'Facture', 'Date Facture (jj/mm/aaaa)', 
                    'Bien(B) Service(S) Immobilisation(I)', 'Libellé Opération','Date paiement (jj/mm/aaaa)',
                    'Mois (En Chiffre: mois de l\'opération)', 'Année', 'Obsérvation', 'N° DAU']
        column = COLUMN
        i=0
        line = 1
        for item in top_header_content:
            cell = column[i]+str(line)
            sheet.write(cell, item, top_header_format)
            i+=1

        # Content
        account_move_line_ids = request.env['account.move.line'].sudo().search([('move_id.date', '>=', date_from), ('move_id.date', '<=', date_to),('move_id.state','=', 'posted'),('move_id.type', 'in', ["out_invoice","in_invoice"]), ('exclude_from_invoice_tab', '=', False)])
        line = 2
        for  move_line_id in account_move_line_ids:
            move_id = move_line_id.move_id
            partner_id = move_id.partner_id

            # Type
            i = 0
            cell = column[i]+str(line)
            move_type = 'C' if (move_id.type in ['out_invoice', 'out_refund', 'out_receipt']) else 'F' if (move_id.type in ['in_invoice', 'in_refund', 'in_receipt']) else 'D'
            sheet.write(cell, move_type, global_format)

            # Local ou Etranger
            i+=1
            cell = column[i]+str(line)
            location = 'L' if (move_id.location_state == 'local') else 'E'
            sheet.write(cell, location, global_format)

            # Nif
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, partner_id.nif, global_format)

            # Raison Social
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, partner_id.social_reason, global_format)

            # Stat
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, partner_id.stat, global_format)

            # Adresse
            i+=1
            cell = column[i]+str(line)
            adress = ((partner_id.street and (partner_id.street+' ') or '')+
                    (partner_id.city and (partner_id.city)+' ' or '')+ 
                    (partner_id.state_id.name and (partner_id.state_id.name)+' ' or '')+
                    (partner_id.country_id.name and (partner_id.country_id.name) or ''))
            sheet.write(cell, adress, global_format)

            # Montant HT
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, round(move_line_id.price_subtotal,2), global_format)
            
            # Montant TVA
            i+=1
            cell = column[i]+str(line)
            try:
                tax_amount = move_line_id.price_total - move_line_id.price_subtotal
            except:
                tax_amount = 0
            sheet.write(cell, tax_amount, global_format)

            # Facture
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, move_id.name, global_format)

            # Date Facture
            i+=1
            cell = column[i]+str(line)
            inv_date = move_id.invoice_date.strftime('%d/%m/%Y')
            sheet.write(cell, inv_date, global_format)

            # Bien ou Service ou immobilié
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, '', global_format)

            # Libellé opération
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, move_line_id.name, global_format)

            # Date paiement
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, move_id.invoice_date_due.strftime('%d/%m/%Y'), global_format)

            # mois de l'opération
            i+=1
            cell = column[i]+str(line)
            op_month = move_id.date.month
            sheet.write(cell, op_month, global_format)

            # année de l'opération
            i+=1
            cell = column[i]+str(line)
            op_year = move_id.date.year
            sheet.write(cell, op_year, global_format)

            # Observation
            i+=1
            cell = column[i]+str(line)
            obs = ''
            for t in move_line_id.tax_ids:
                obs += t.name
            sheet.write(cell, obs, global_format)

            # N°DAU
            i+=1
            cell = column[i]+str(line)
            sheet.write(cell, '', global_format)

            line +=1

        workbook.close()
        output.seek(0)
        xlsheader = [('Content-Type', 'application/octet-stream'),
                     ('Content-Disposition', 'attachment; filename=%s;' % filename)]
        return request.make_response(output, xlsheader)       

