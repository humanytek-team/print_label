# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, models
import logging
_logger = logging.getLogger(__name__)


class PrintLabelProd2(models.AbstractModel):
    _name = 'report.print_label.print_label_prod2'

    def decimal_format(self, num):
        return int(num)

    def op_name(self, move_id):
        StockMove = self.env['stock.move']
        moves = StockMove.search([('move_dest_id.id', '=', move_id)])
        if moves:
            return moves[0].production_id.name
        return ''

    def get_observation(self, move_id):
        StockMove = self.env['stock.move']
        moves = StockMove.search([('move_dest_id.id', '=', move_id)])
        if moves:
            return moves[0].production_id.sale_line_observation
        return ''

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        StockPicking = self.env['stock.picking']
        report = Report._get_report_from_name(
            'print_label.print_label_product2')
        docs = StockPicking.browse(docids)
        docargs = {
            'get_observation': self.get_observation,
            'op_name': self.op_name,
            'decimal_format': self.decimal_format,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'data': data,
        }

        return Report.render('print_label.print_label_prod2', docargs)


class PrintLabelProd2Mrp(models.AbstractModel):
    _name = 'report.print_label.print_label_prod2_mrp'

    def decimal_format(self, num):
        return int(num)

    def get_date(self, mrp_id):
        StockMove = self.env['stock.move']
        moves = StockMove.search([('production_id.id', '=', mrp_id)])
        _logger.info('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        _logger.info(mrp_id)
        if moves:
            _logger.info('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            if moves[0].move_dest_id:
                if moves[0].move_dest_id.picking_id:
                    return moves[0].move_dest_id.picking_id.min_date
        return ''

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        MrpProduction = self.env['mrp.production']
        report = Report._get_report_from_name(
            'print_label.print_label_product2_mrp')
        docs = MrpProduction.browse(docids)
        docargs = {
            'get_date': self.get_date,
            'decimal_format': self.decimal_format,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'data': data,
        }

        return Report.render('print_label.print_label_prod2_mrp', docargs)
