# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyReportWizard(models.Model):
    _name = "warranty.report.wizard"
    _description = 'Warranty Report Wizard'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    filter_date_type = fields.Selection([('start', 'Warranty Start Date'), ('end', 'Warranty End Date')],
                                        string='Filter Date Type', default="start")
    date_start = fields.Date(string="Warranty Start Date")
    date_end = fields.Date(string="Warranty End Date")
    _date_end = fields.Date(string="Warranty End Date")
    product_select = fields.Boolean(string="Product")
    product_id = fields.Many2one('product.product', string="Product")
    customer_select = fields.Boolean(string="Customer")
    customer_id = fields.Many2one('res.partner', string="Customer")
    sale_select = fields.Boolean(string="Salesperson")
    user_id = fields.Many2one('res.users', string="Salesperson")
    date_action = fields.Date.today()
    state_select = fields.Boolean(string='Status')
    state = fields.Selection(
        [('in warranty', 'In warranty'),
         ('near', 'Near warranty expiry'), ('expired', 'Expired')], copy=False, string='Status')

    @api.multi
    def print_pdf(self):
        data = self.read()[0]
        domain = []
        if self.filter_date_type == 'start':
            domain.append(('date_start', '>=', self.date_from))
            domain.append(('date_start', '<=', self.date_to))
            domain.append(('state', '!=', 'draft'))
            if self.product_id:
                domain.append(('product_id', '=', self.product_id.id))
                if self.customer_id:
                    domain.append(('customer_id', '=', self.customer_id.id))
            if self.user_id:
                domain.append(('user_id', '=', self.user_id.id))
            if self.state == 'in warranty':
                domain.append(('state', '=', 'in warranty'))
            if self.state == 'near':
                domain.append(('state', '=', 'near'))
            if self.state == 'expired':
                domain.append(('state', '=', 'expired'))
            bid_ids = self.env['product.warranty'].search(domain).ids
            datas = {'ids': bid_ids}
            datas.update(model='product.warranty')
            datas.update({'form': data})
            return self.env.ref('product_warranty.action_summary_product_warranty_pdf').with_context(landscape=True)\
                .report_action(
                self, data=datas,
                config=False)  # odoo 11
            # return act
        elif self.filter_date_type == 'end':
            domain.append(('_date_end', '>=', self.date_from))
            domain.append(('_date_end', '<=', self.date_to))
            domain.append(('state', '!=', 'cancel'))
            if self.product_id:
                domain.append(('product_id', '=', self.product_id.id))
                if self.customer_id:
                    domain.append(('customer_id', '=', self.customer_id.id))
            if self.user_id:
                domain.append(('user_id', '=', self.user_id.id))
            if self.state == 'in warranty':
                domain.append(('state', '=', 'in warranty'))
            if self.state == 'near':
                domain.append(('state', '=', 'near'))
            if self.state == 'expired':
                domain.append(('state', '=', 'expired'))
            bid_ids = self.env['product.warranty'].search(domain).ids
            datas = {'ids': bid_ids}
            datas.update(model='product.warranty')
            datas.update({'form': data})
            return self.env.ref('product_warranty.action_summary_product_warranty_pdf').with_context(landscape=True)\
                .report_action(
                self, data=datas,
                config=False)  # odoo 11
            # return act

