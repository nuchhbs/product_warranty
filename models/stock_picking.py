from odoo import models, fields, api, _


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    type_id = fields.Many2one('warranty.type', string="Warranty Type", compute="_get_type_id")

    def _get_type_id(self):
        for line in self:
            order_line_id = self.env['sale.order.line'].search(
                [('order_id.name', '=', line.origin), ('product_id', '=', line.product_id.id)])
            for rec in order_line_id:
                line.type_id = rec.type_id.id


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    warranty_count = fields.Integer(string='Warranty', compute='get_warranty_count')
    date_start = fields.Date(string="Warranty Start Date", compute="_get_start_date")
    picking_warranty_note = fields.Text(string='Warranty Note')

    def _get_start_date(self):
        print("send start date")
        order_id = self.env['sale.order'].search([('name', '=', self.origin)])
        for line in order_id:
            self.date_start = line.date_start

    def action_open_warranty(self):
        quantity_product = 0.0
        product_warranty_obj = self.env['product.warranty']
        for line_move in self.move_ids_without_package:
            product_id = line_move.product_id
            type_id = line_move.type_id
            if product_id.tracking == "none":
                quantity_product = line_move.quantity_done
                product_warranty_data = {
                    'customer_id': self.partner_id.id,
                    'user_id':  self.env.uid,
                    'picking_id': self.id,
                    'product_id': product_id.id,
                    'date_start': self.date_start,
                    'type_id': type_id.id,
                    'sale_order_name': self.origin,
                    'quantity_product': quantity_product,
                    'warranty_note': self.picking_warranty_note,
                }
                warranty_id = product_warranty_obj.create(product_warranty_data)
                product_warranty_obj += warranty_id

            if product_id.tracking == "serial":
                for move_line_id in line_move.move_line_ids:
                    product_lot = move_line_id.lot_id.id
                    quantity_product = move_line_id.qty_done
                    product_warranty_data = {
                        'customer_id': self.partner_id.id,
                        'user_id': self.env.uid,
                        'picking_id': self.id,
                        'product_id': product_id.id,
                        'date_start': self.date_start,
                        'type_id': type_id.id,
                        'sale_order_name': self.origin,
                        'quantity_product': quantity_product,
                        'product_lot_id': product_lot,
                        'warranty_note': self.picking_warranty_note,
                    }
                    warranty_id = product_warranty_obj.create(product_warranty_data)
                    product_warranty_obj += warranty_id

            if product_id.tracking == "lot":
                for move_line_id in line_move.move_line_ids:
                    product_lot = move_line_id.lot_id.id
                    quantity_product = move_line_id.qty_done
                    product_warranty_data = {
                        'customer_id': self.partner_id.id,
                        'user_id': self.env.uid,
                        'picking_id': self.id,
                        'product_id': product_id.id,
                        'date_start': self.date_start,
                        'type_id': type_id.id,
                        'sale_order_name': self.origin,
                        'quantity_product': quantity_product,
                        'product_lot_id': product_lot,
                        'warranty_note': self.picking_warranty_note,
                    }
                    warranty_id = product_warranty_obj.create(product_warranty_data)
                    product_warranty_obj += warranty_id

        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('product_warranty.action_product_profile')
        list_view_id = imd.xmlid_to_res_id('product_warranty.product_list_tree')
        form_view_id = imd.xmlid_to_res_id('product_warranty.product_list_view')
        result = {
            'name': action.name,
            # 'help': action.help,
            'type': 'ir.actions.act_window',
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'],
                      [False, 'calendar'], [False, 'pivot']],
            # 'target': 'new',
            # 'context': 'new',
            'res_model': 'product.warranty',
        }
        if len(warranty_id) > 1:
            result['domain'] = "[('id','in',%s)]" % warranty_id.ids
        elif len(warranty_id) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = warranty_id.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    @api.multi
    def open_warranty_info(self):
        self.ensure_one()
        return {
            'name': _('Product Warranty'),
            'domain': [('picking_id', '=', self.name), ('order_id', '=', self.origin)],
            'view_type': 'form',
            'res_model': 'product.warranty',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_warranty_count(self):
        for record in self:
            record.warranty_count = self.env['product.warranty'].search_count(
                [('picking_id', '=', self.name), ('order_id', '=', self.origin)])