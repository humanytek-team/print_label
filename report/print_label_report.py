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
    #_template = 'print_label.print_label_prod2'

    def decimal_format(self, num):
        _logger.info('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
        _logger.info(num)
        return int(num)

    def len_pack_operation_product(self, o):
        _logger.info('LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL')
        #return len(o.pack_operation_product_ids)
        return 4

    @api.model
    def render_html(self, docids, data=None):
        #docids = self._ids
        Report = self.env['report']
        StockPicking = self.env['stock.picking']
        report = Report._get_report_from_name(
            'print_label.print_label_product2')
        docs = StockPicking.browse(docids)
        #tz = self.env.context.get('tz', False)
        #if not tz:
            #tz = 'US/Arizona'
        #datetime_now = datetime.now(timezone(tz))
        #data['extra_data'].update({
            #'datetime': datetime_now.strftime('%d/%m/%y %H:%M:%S'), })
        docargs = {
            'len_pack_operation_product': self.len_pack_operation_product,
            'decimal_format': self.decimal_format,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'data': data,
        }

        return Report.render('print_label.print_label_prod2', docargs)
