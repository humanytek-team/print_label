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

    def get_data(self, mrp_id):
        mrp_production = self.env['mrp.production'].browse(mrp_id)
        data = {}
        if mrp_production:
            data['qty'] = int(mrp_production.product_qty)
            data['mrp_production_name'] = mrp_production.name
            sale_order = mrp_production.sale_id
            sale_order_type = sale_order and sale_order.type_id
            data['type'] = sale_order_type and sale_order_type.name or 'UNKNOWN'
            res_partner = mrp_production.partner_id
            data['partner_name'] = res_partner and res_partner.name or 'UNKNOWN'
            product_product = mrp_production.product_id
            data['product_default'] = product_product and product_product.default_code or 'UNKNOWN'
            product_template = product_product and product_product.product_tmpl_id
            data['product_name'] = product_template and product_template.name or 'UNKNOWN'
            stock_move = self.env['stock.move'].search([('production_id', '=', mrp_production.id)], limit=1)
            stock_move_dest = stock_move and stock_move.move_dest_id
            stock_picking = stock_move_dest and stock_move_dest.picking_id
            data['date'] = stock_picking and stock_picking.min_date or 'UNKNOWN'
            procurement_order = stock_move_dest and stock_move_dest.procurement_id
            sale_order_line = procurement_order and procurement_order.sale_line_id
            if sale_order_line:
                data['observation'] = sale_order_line.observation
            else:
                data['observation'] = 'UNKNOWN'
        return data

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        report = Report._get_report_from_name(
            'print_label.print_label_product2_mrp')
        docs = docids
        docargs = {
            'get_data': self.get_data,
            'decimal_format': self.decimal_format,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'data': data,
        }
        return Report.render('print_label.print_label_prod2_mrp', docargs)
