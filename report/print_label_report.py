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
        self.env.cr.execute(
            """
                SELECT sp.min_date, sot.name, rp.name, pp.default_code, pt.name, sol.observation, mp.product_qty, mp.name
                FROM mrp_production mp
                JOIN stock_move sm ON sm.production_id = mp.id
                JOIN stock_move smd ON smd.id = sm.move_dest_id
                JOIN procurement_order po ON po.id = smd.procurement_id
                JOIN sale_order_line sol ON sol.id = po.sale_line_id
                JOIN stock_picking sp ON sp.id = smd.picking_id
                JOIN sale_order so ON so.id = mp.sale_id
                JOIN sale_order_type sot ON sot.id = so.type_id
                JOIN res_partner rp ON rp.id = mp.partner_id
                JOIN product_product pp ON pp.id = mp.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                WHERE sm.production_id = %s;
            """,
            (mrp_id,)
        )
        dat = self.env.cr.fetchone()
        data = {}
        if dat:
            data['date'] = dat[0]
            data['type'] = dat[1]
            data['partner_name'] = dat[2][:41]
            data['product_default'] = dat[3]
            data['product_name'] = dat[4][:82]
            data['observation'] = dat[5]
            data['qty'] = int(dat[6])
            data['mrp_name'] = dat[7]
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
