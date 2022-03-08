# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ReportSummaryWarranty(models.AbstractModel):
    _name = 'report.product_warranty.report_warranty_detail'

    @api.model
    def _get_report_values(self, docids, data=None):  # odoo 11
        buy_ids = data['ids']
        report = self.env['ir.actions.report']._get_report_from_name(
            'product_warranty.report_warranty_detail')
        # docargs = {
        return {  # odoo 11
            'doc_ids': buy_ids,
            'doc_model': 'product.warranty',
            'docs': self.env['product.warranty'].browse(buy_ids),
            'data': data,
        }
