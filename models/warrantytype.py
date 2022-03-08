# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductInherit(models.Model):
    _inherit = 'product.product'

    eligible = fields.Boolean(string='Warranty Eligible')
    type_id = fields.Many2one('warranty.type', string="Warranty Type")
    product_line = fields.One2many('warranty.type', 'product_id', string="Product Warranty Information")


class WarrantyType(models.Model):
    _name = "warranty.type"
    _rec_name = "name_period"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_period = fields.Char(string="Name", track_visibility="always", required="True")
    warranty_period = fields.Integer(string="Warranty Period", required="True")
    unit = fields.Selection([
        ('day', 'Day'),
        ('month', 'Month'),
        ('year', 'Year'),
    ], default='year', string="Unit", track_visibility="always", required="True")
    note = fields.Text(string='Description')
    product_id = fields.Many2one('product.product', string="Product", required="True")
