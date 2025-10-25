# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Additional fields for inventory management
    barcode = fields.Char('Barcode', copy=False, help="Product barcode for scanning")
    qr_code = fields.Char('QR Code', copy=False, help="Product QR code")
    min_stock_level = fields.Float('Minimum Stock Level', default=10.0, 
                                   help="Alert when stock falls below this level")
    max_stock_level = fields.Float('Maximum Stock Level', default=100.0,
                                   help="Maximum stock capacity")
    reorder_quantity = fields.Float('Reorder Quantity', default=20.0,
                                    help="Suggested quantity to reorder")
    warehouse_location = fields.Char('Warehouse Location', help="Physical location in warehouse")
    is_low_stock = fields.Boolean('Low Stock Alert', compute='_compute_low_stock', store=True)
    stock_status = fields.Selection([
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
    ], string='Stock Status', compute='_compute_stock_status', store=True)
    
    @api.depends('qty_available', 'min_stock_level')
    def _compute_low_stock(self):
        """Check if product stock is below minimum level"""
        for product in self:
            product.is_low_stock = product.qty_available < product.min_stock_level
    
    @api.depends('qty_available', 'min_stock_level')
    def _compute_stock_status(self):
        """Compute current stock status"""
        for product in self:
            if product.qty_available <= 0:
                product.stock_status = 'out_of_stock'
            elif product.qty_available < product.min_stock_level:
                product.stock_status = 'low_stock'
            else:
                product.stock_status = 'in_stock'
    
    @api.constrains('min_stock_level', 'max_stock_level')
    def _check_stock_levels(self):
        """Validate stock level constraints"""
        for product in self:
            if product.min_stock_level < 0:
                raise ValidationError("Minimum stock level cannot be negative!")
            if product.max_stock_level < product.min_stock_level:
                raise ValidationError("Maximum stock level must be greater than minimum stock level!")
    
    def action_generate_reorder_suggestion(self):
        """Generate reorder suggestion based on stock levels"""
        self.ensure_one()
        if self.is_low_stock:
            suggested_qty = self.reorder_quantity
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Reorder Suggestion',
                    'message': f'Suggested reorder quantity for {self.name}: {suggested_qty} units',
                    'type': 'warning',
                    'sticky': False,
                }
            }


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    def action_view_stock_moves(self):
        """View all stock movements for this product"""
        self.ensure_one()
        return {
            'name': 'Stock Movements',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id}
        }
