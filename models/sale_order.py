# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class CustomSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    type_id = fields.Many2one('warranty.type', string="Warranty Type")


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    date_start = fields.Date(string="Warranty Start Date", default=lambda self: fields.date.today(), required="True")
    warranty_seq = fields.Char(string='Warranty Number Before Extended')
