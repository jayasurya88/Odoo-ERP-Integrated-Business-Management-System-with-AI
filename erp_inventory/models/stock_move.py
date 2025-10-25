# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Additional tracking fields
    move_reason = fields.Selection([
        ('sale', 'Sale Order'),
        ('purchase', 'Purchase Order'),
        ('adjustment', 'Inventory Adjustment'),
        ('return', 'Return'),
        ('transfer', 'Internal Transfer'),
        ('manufacturing', 'Manufacturing'),
        ('scrap', 'Scrap'),
    ], string='Move Reason', default='adjustment')
    
    approved_by = fields.Many2one('res.users', string='Approved By')
    approval_date = fields.Datetime('Approval Date')
    notes = fields.Text('Notes')
    cost_impact = fields.Monetary('Cost Impact', compute='_compute_cost_impact', currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    
    @api.depends('product_id', 'product_uom_qty', 'product_id.standard_price')
    def _compute_cost_impact(self):
        """Calculate the cost impact of this stock move"""
        for move in self:
            move.cost_impact = move.product_uom_qty * move.product_id.standard_price


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Additional picking fields
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgent'),
        ('2', 'Very Urgent'),
    ], string='Priority', default='0')
    
    delivery_notes = fields.Text('Delivery Notes')
    vehicle_number = fields.Char('Vehicle Number')
    driver_name = fields.Char('Driver Name')
    driver_phone = fields.Char('Driver Phone')
    estimated_delivery_date = fields.Datetime('Estimated Delivery Date')
    actual_delivery_date = fields.Datetime('Actual Delivery Date')
    
    def action_confirm_delivery(self):
        """Confirm delivery and set actual delivery date"""
        self.ensure_one()
        self.actual_delivery_date = fields.Datetime.now()
        return self.button_validate()
