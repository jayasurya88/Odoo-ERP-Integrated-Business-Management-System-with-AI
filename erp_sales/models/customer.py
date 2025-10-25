# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Customer classification
    customer_type = fields.Selection([
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('government', 'Government'),
    ], string='Customer Type', default='individual')
    
    customer_rating = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐'),
    ], string='Customer Rating')
    
    # Sales statistics
    total_orders = fields.Integer('Total Orders', compute='_compute_sales_stats', store=True)
    total_sales_amount = fields.Monetary('Total Sales', compute='_compute_sales_stats', store=True, currency_field='currency_id')
    average_order_value = fields.Monetary('Average Order Value', compute='_compute_sales_stats', store=True, currency_field='currency_id')
    last_order_date = fields.Date('Last Order Date', compute='_compute_sales_stats', store=True)
    
    # Customer preferences
    preferred_payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('online', 'Online Payment'),
    ], string='Preferred Payment Method')
    
    credit_limit = fields.Monetary('Credit Limit', currency_field='currency_id')
    current_credit_used = fields.Monetary('Credit Used', compute='_compute_credit_used', currency_field='currency_id')
    
    # Additional contact info
    alternate_phone = fields.Char('Alternate Phone')
    tax_id_number = fields.Char('Tax ID Number')
    
    @api.depends('sale_order_ids', 'sale_order_ids.state', 'sale_order_ids.amount_total')
    def _compute_sales_stats(self):
        """Compute customer sales statistics"""
        for partner in self:
            confirmed_orders = partner.sale_order_ids.filtered(lambda o: o.state in ['sale', 'done'])
            partner.total_orders = len(confirmed_orders)
            partner.total_sales_amount = sum(confirmed_orders.mapped('amount_total'))
            partner.average_order_value = partner.total_sales_amount / partner.total_orders if partner.total_orders > 0 else 0.0
            partner.last_order_date = max(confirmed_orders.mapped('date_order')).date() if confirmed_orders else False
    
    @api.depends('sale_order_ids', 'sale_order_ids.payment_status')
    def _compute_credit_used(self):
        """Calculate current credit used by customer"""
        for partner in self:
            unpaid_orders = partner.sale_order_ids.filtered(
                lambda o: o.state in ['sale', 'done'] and o.payment_status in ['unpaid', 'partial']
            )
            partner.current_credit_used = sum(unpaid_orders.mapped('amount_total'))
    
    def action_view_customer_orders(self):
        """View all orders for this customer"""
        self.ensure_one()
        return {
            'name': 'Customer Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id}
        }
