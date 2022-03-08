# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import timedelta


class ProductWarranty(models.Model):
    _name = "product.warranty"
    _rec_name = "warranty_seq"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    warranty_seq = fields.Char(string='Warranty Number', copy=False, readonly=True,
                               default=lambda self: _('New'))
    order_id = fields.Many2one('sale.order', string="Sale Order", compute='_sale_order')
    sale_order_name = fields.Char(string="Sale Order")
    product_id = fields.Many2one('product.product', string="Product",
                                 track_visibility="always", required="True")
    customer_id = fields.Many2one('res.partner', string="Customer", track_visibility="always", required="True")
    user_id = fields.Many2one('res.users', string="Salesperson", track_visibility="always",
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Company')
    type_id = fields.Many2one('warranty.type', string="Warranty Type", track_visibility="always")
    date_start = fields.Date(string="Warranty Start Date", track_visibility="always",
                             default=lambda self: fields.date.today())
    date_end = fields.Date(string="Warranty End Date", track_visibility="onchange", compute='_compute_chek_date_end')
    _date_end = fields.Date(string="Warranty End Date")
    date_action = fields.Date.today()
    warranty_note = fields.Text(string='Notes')
    state = fields.Selection(
        [('draft', 'Draft'), ('in warranty', 'In warranty'),
         ('near', 'Near warranty expiry'), ('expired', 'Expired')], string="Status",
        default="draft", copy=False, track_visibility='onchange')

    not_renew = fields.Selection([('not_renew', 'Not Extended warranty')], copy=False, track_visibility='onchange',
                                 string="Status")

    # ตัวรับ picking_id
    picking_id = fields.Many2one('stock.picking', string="Picking", ondelete='cascade', required="True")
    quantity_product = fields.Float(string="Product Quantity")
    product_lot_id = fields.Many2one('stock.production.lot', string='Product Lot/Serial')

    def action_in_warranty(self):
        self.state = 'in warranty'
        if self.date_end:
            self._date_end = self.date_end

    def action_expired(self):
        self.state = 'expired'

    def action_not_renew(self):
        self.not_renew = 'not_renew'

    @api.model
    def create(self, vals):
        if vals.get('warranty_seq', _('New')) == _('New'):
            vals['warranty_seq'] = self.env['ir.sequence'].next_by_code('product.warranty.sequence') or _('New')
        result = super(ProductWarranty, self).create(vals)
        return result

    def _compute_chek_date_end(self):
        for line in self:
            if line.type_id.unit == 'year':
                line.date_end = line.date_start + timedelta(days=356 * line.type_id.warranty_period)
            if line.type_id.unit == 'month':
                line.date_end = line.date_start + timedelta(days=30 * line.type_id.warranty_period)
            if line.type_id.unit == 'day':
                line.date_end = line.date_start + timedelta(days=1 * line.type_id.warranty_period)

    @api.multi
    def _sale_order(self):
        for line in self:
            order_id = self.env['sale.order'].search([("name", "=", line.sale_order_name)])
            if order_id:
                line.order_id = order_id.id

    @api.multi
    def check_in_warranty(self):
        today = fields.Date.today()
        product_warranty = self.env['product.warranty'].search([])
        for rec in product_warranty:
            if rec.state == 'draft' and rec.date_start <= today:
                rec.state = 'in warranty'
            if rec.date_end:
                rec._date_end = rec.date_end

    @api.multi
    def near_expiry(self):
        today = fields.Date.today()
        product_warranty = self.env['product.warranty'].search([])
        for line in product_warranty:
            line._date_end = line.date_end
            line.near_date = line._date_end - timedelta(days=7)
            if line.state == 'in warranty' and line.near_date <= today:
                line.state = 'near'

    @api.multi
    def check_expiry(self):
        today = fields.Date.today()
        product_warranty = self.env['product.warranty'].search([])
        for warranty in product_warranty:
            warranty._date_end = warranty.date_end
            warranty.new_date = warranty._date_end + timedelta(days=1)
            if warranty.state == 'near' and warranty.new_date == today:
                warranty.state = 'expired'

    def action_renew_warranty(self):
        for warranty in self:
            if self.order_id:
                sale = {
                    'partner_id': self.customer_id.id,
                    'warranty_seq': self.warranty_seq,
                }
                selling = self.env['sale.order'].create(sale)
                self.order_id = selling.id

    def action_create_renew_warranty(self):
        # product_warranty = self.env['product.warranty']
        for rec in self:
            renew_date = self.date_end + timedelta(days=1)
            renew_product_warranty_data = {
                'customer_id': self.customer_id.id,
                'user_id': self.user_id.id,
                'product_id': self.product_id.id,
                'picking_id': self.picking_id.id,
                'quantity_product': self.quantity_product,
                'date_start': renew_date,
                'warranty_note': self.warranty_note
            }
            renew_warranty = self.env['product.warranty'].create(renew_product_warranty_data)
