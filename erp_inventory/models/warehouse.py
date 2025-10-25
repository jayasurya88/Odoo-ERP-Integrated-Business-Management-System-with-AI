# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    # Additional warehouse fields
    manager_id = fields.Many2one('res.users', string='Warehouse Manager')
    capacity = fields.Float('Storage Capacity', help="Total storage capacity in cubic meters")
    current_utilization = fields.Float('Current Utilization %', compute='_compute_utilization')
    address = fields.Text('Warehouse Address')
    contact_phone = fields.Char('Contact Phone')
    contact_email = fields.Char('Contact Email')
    is_active = fields.Boolean('Active', default=True)
    
    @api.depends('lot_stock_id')
    def _compute_utilization(self):
        """Calculate warehouse utilization percentage"""
        for warehouse in self:
            # Simplified calculation - can be enhanced based on actual volume
            if warehouse.capacity > 0:
                total_products = self.env['stock.quant'].search_count([
                    ('location_id', 'child_of', warehouse.lot_stock_id.id),
                    ('quantity', '>', 0)
                ])
                warehouse.current_utilization = min((total_products / warehouse.capacity) * 100, 100)
            else:
                warehouse.current_utilization = 0.0


class StockLocation(models.Model):
    _inherit = 'stock.location'

    # Additional location fields
    aisle = fields.Char('Aisle')
    rack = fields.Char('Rack')
    shelf = fields.Char('Shelf')
    bin = fields.Char('Bin')
    barcode = fields.Char('Location Barcode')
    temperature_controlled = fields.Boolean('Temperature Controlled')
    temperature_range = fields.Char('Temperature Range')
    
    @api.depends('aisle', 'rack', 'shelf', 'bin')
    def _compute_display_name(self):
        """Enhanced display name with location details"""
        super()._compute_display_name()
        for location in self:
            if location.aisle or location.rack:
                parts = [location.name]
                if location.aisle:
                    parts.append(f"Aisle {location.aisle}")
                if location.rack:
                    parts.append(f"Rack {location.rack}")
                if location.shelf:
                    parts.append(f"Shelf {location.shelf}")
                location.display_name = " - ".join(parts)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # Additional inventory tracking fields
    last_inventory_date = fields.Datetime('Last Inventory Date')
    expiry_date = fields.Date('Expiry Date')
    batch_number = fields.Char('Batch Number')
    
    @api.constrains('quantity')
    def _check_negative_quantity(self):
        """Prevent negative stock quantities"""
        for quant in self:
            if quant.quantity < 0 and quant.location_id.usage == 'internal':
                raise ValidationError(f"Negative stock not allowed for {quant.product_id.name} at {quant.location_id.name}")
