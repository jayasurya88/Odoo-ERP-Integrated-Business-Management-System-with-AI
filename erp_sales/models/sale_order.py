# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Additional sales fields
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
    ], string='Payment Status', compute='_compute_payment_status', store=True)
    
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('online', 'Online Payment'),
    ], string='Payment Method')
    
    delivery_status = fields.Selection([
        ('pending', 'Pending'),
        ('partial', 'Partially Delivered'),
        ('delivered', 'Delivered'),
    ], string='Delivery Status', compute='_compute_delivery_status', store=True)
    
    sales_person_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    discount_percentage = fields.Float('Discount %', default=0.0)
    total_discount = fields.Monetary('Total Discount', compute='_compute_total_discount', store=True)
    expected_delivery_date = fields.Date('Expected Delivery Date')
    actual_delivery_date = fields.Date('Actual Delivery Date')
    customer_notes = fields.Text('Customer Notes')
    internal_notes = fields.Text('Internal Notes')
    
    # AI prediction related fields
    predicted_delivery_date = fields.Date('Predicted Delivery Date', compute='_compute_predicted_delivery')
    
    @api.depends('invoice_ids', 'invoice_ids.payment_state', 'amount_total')
    def _compute_payment_status(self):
        """Compute payment status based on invoices"""
        for order in self:
            if not order.invoice_ids:
                order.payment_status = 'unpaid'
            else:
                paid_invoices = order.invoice_ids.filtered(lambda inv: inv.payment_state == 'paid')
                if all(inv.payment_state == 'paid' for inv in order.invoice_ids):
                    order.payment_status = 'paid'
                elif any(inv.payment_state == 'paid' for inv in order.invoice_ids):
                    order.payment_status = 'partial'
                else:
                    order.payment_status = 'unpaid'
    
    @api.depends('picking_ids', 'picking_ids.state')
    def _compute_delivery_status(self):
        """Compute delivery status based on pickings"""
        for order in self:
            if not order.picking_ids:
                order.delivery_status = 'pending'
            else:
                done_pickings = order.picking_ids.filtered(lambda p: p.state == 'done')
                if all(p.state == 'done' for p in order.picking_ids):
                    order.delivery_status = 'delivered'
                elif any(p.state == 'done' for p in order.picking_ids):
                    order.delivery_status = 'partial'
                else:
                    order.delivery_status = 'pending'
    
    @api.depends('amount_total', 'discount_percentage')
    def _compute_total_discount(self):
        """Calculate total discount amount"""
        for order in self:
            order.total_discount = order.amount_total * (order.discount_percentage / 100)
    
    @api.depends('date_order')
    def _compute_predicted_delivery(self):
        """Predict delivery date based on historical data (simplified)"""
        for order in self:
            if order.date_order:
                # Simple prediction: add 7 days to order date
                order.predicted_delivery_date = order.date_order.date() + timedelta(days=7)
            else:
                order.predicted_delivery_date = False
    
    def action_confirm_with_stock_check(self):
        """Confirm order with stock availability check"""
        for order in self:
            # Check stock availability
            for line in order.order_line:
                if line.product_id.type == 'product':
                    if line.product_uom_qty > line.product_id.qty_available:
                        raise ValidationError(
                            f"Insufficient stock for {line.product_id.name}. "
                            f"Available: {line.product_id.qty_available}, Required: {line.product_uom_qty}"
                        )
        return self.action_confirm()
    
    def action_mark_delivered(self):
        """Mark order as delivered"""
        self.ensure_one()
        self.actual_delivery_date = fields.Date.today()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Delivery Confirmed',
                'message': f'Order {self.name} marked as delivered',
                'type': 'success',
                'sticky': False,
            }
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Additional line fields
    line_discount_amount = fields.Monetary('Discount Amount', compute='_compute_line_discount')
    margin_percentage = fields.Float('Margin %', compute='_compute_margin')
    cost_price = fields.Float('Cost Price', related='product_id.standard_price', readonly=True)
    
    @api.depends('price_subtotal', 'discount')
    def _compute_line_discount(self):
        """Calculate discount amount for line"""
        for line in self:
            if line.discount > 0:
                line.line_discount_amount = line.price_subtotal * (line.discount / 100)
            else:
                line.line_discount_amount = 0.0
    
    @api.depends('price_unit', 'cost_price')
    def _compute_margin(self):
        """Calculate profit margin percentage"""
        for line in self:
            if line.cost_price > 0:
                line.margin_percentage = ((line.price_unit - line.cost_price) / line.cost_price) * 100
            else:
                line.margin_percentage = 0.0
