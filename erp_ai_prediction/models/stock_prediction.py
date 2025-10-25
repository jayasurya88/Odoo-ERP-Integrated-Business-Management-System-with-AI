# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from .prediction_engine import PredictionEngine
import logging

_logger = logging.getLogger(__name__)


class StockPrediction(models.Model):
    _name = 'stock.prediction'
    _description = 'Stock Demand Prediction'
    _order = 'prediction_date desc'

    name = fields.Char('Reference', required=True, copy=False, readonly=True, default='New')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', string='Product Template')
    
    # Current stock information
    current_stock = fields.Float('Current Stock', related='product_id.qty_available', readonly=True)
    min_stock_level = fields.Float('Min Stock Level', related='product_tmpl_id.min_stock_level', readonly=True)
    max_stock_level = fields.Float('Max Stock Level', related='product_tmpl_id.max_stock_level', readonly=True)
    
    # Prediction data
    prediction_date = fields.Date('Prediction Date', default=fields.Date.today, required=True)
    prediction_period = fields.Selection([
        ('week', 'Next Week'),
        ('month', 'Next Month'),
    ], string='Prediction Period', default='week', required=True)
    
    predicted_demand = fields.Float('Predicted Demand', readonly=True)
    confidence_score = fields.Float('Confidence Score %', readonly=True)
    prediction_method = fields.Selection([
        ('moving_average', 'Moving Average'),
        ('linear_regression', 'Linear Regression'),
        ('hybrid', 'Hybrid (MA + LR)'),
    ], string='Prediction Method', default='hybrid')
    
    # Reorder suggestion
    reorder_quantity = fields.Float('Reorder Quantity', readonly=True)
    reorder_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', compute='_compute_reorder_priority', store=True)
    
    # Actual data (for accuracy tracking)
    actual_demand = fields.Float('Actual Demand')
    accuracy = fields.Float('Accuracy %', compute='_compute_accuracy', store=True)
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('predicted', 'Predicted'),
        ('validated', 'Validated'),
    ], string='Status', default='draft')
    
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    
    @api.model
    def create(self, vals):
        """Generate sequence for prediction"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.prediction') or 'New'
        return super(StockPrediction, self).create(vals)
    
    @api.depends('current_stock', 'predicted_demand', 'min_stock_level')
    def _compute_reorder_priority(self):
        """Calculate reorder priority based on stock levels"""
        for prediction in self:
            if prediction.current_stock <= 0:
                prediction.reorder_priority = 'urgent'
            elif prediction.current_stock < prediction.min_stock_level:
                prediction.reorder_priority = 'high'
            elif prediction.current_stock < (prediction.min_stock_level + prediction.predicted_demand):
                prediction.reorder_priority = 'medium'
            else:
                prediction.reorder_priority = 'low'
    
    @api.depends('predicted_demand', 'actual_demand')
    def _compute_accuracy(self):
        """Calculate prediction accuracy"""
        engine = PredictionEngine()
        for prediction in self:
            if prediction.actual_demand > 0:
                prediction.accuracy = engine.calculate_accuracy(
                    prediction.predicted_demand,
                    prediction.actual_demand
                )
            else:
                prediction.accuracy = 0.0
    
    def action_generate_prediction(self):
        """Generate AI prediction for product demand"""
        self.ensure_one()
        
        engine = PredictionEngine()
        
        # Get historical sales data
        days_back = 90  # Look back 90 days
        date_from = datetime.now() - timedelta(days=days_back)
        
        sale_lines = self.env['sale.order.line'].search([
            ('product_id', '=', self.product_id.id),
            ('order_id.date_order', '>=', date_from),
            ('order_id.state', 'in', ['sale', 'done'])
        ])
        
        if not sale_lines:
            self.predicted_demand = 0.0
            self.confidence_score = 0.0
            self.reorder_quantity = 0.0
            self.state = 'predicted'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Historical Data',
                    'message': f'No sales history found for {self.product_id.name}',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Prepare data
        df = engine.prepare_sales_data(sale_lines)
        
        if df is None:
            _logger.error("Failed to prepare sales data")
            return
        
        # Generate prediction
        predicted_demand = engine.predict_demand(df, self.product_id.id, self.prediction_method)
        
        # Calculate reorder quantity
        reorder_qty = engine.calculate_reorder_quantity(
            predicted_demand,
            self.current_stock,
            self.min_stock_level,
            self.max_stock_level
        )
        
        # Calculate confidence score based on data availability
        data_points = len(df[df['product_id'] == self.product_id.id])
        confidence = min(100, (data_points / 30) * 100)  # 30 data points = 100% confidence
        
        # Update prediction
        self.write({
            'predicted_demand': predicted_demand,
            'reorder_quantity': reorder_qty,
            'confidence_score': confidence,
            'state': 'predicted',
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Prediction Generated',
                'message': f'Predicted demand: {predicted_demand:.2f} units, Reorder: {reorder_qty:.2f} units',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_validate(self):
        """Validate prediction"""
        self.write({'state': 'validated'})
    
    def action_create_purchase_order(self):
        """Create purchase order based on prediction"""
        self.ensure_one()
        
        if self.reorder_quantity <= 0:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Reorder Needed',
                    'message': 'Reorder quantity is zero or negative',
                    'type': 'info',
                    'sticky': False,
                }
            }
        
        # This would create a purchase order in a real implementation
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Purchase Order',
                'message': f'Purchase order for {self.reorder_quantity:.2f} units of {self.product_id.name} should be created',
                'type': 'info',
                'sticky': True,
            }
        }
    
    @api.model
    def cron_generate_predictions(self):
        """Cron job to generate predictions for all products"""
        _logger.info("Starting automatic prediction generation...")
        
        # Get all products with sales history
        products = self.env['product.product'].search([
            ('type', '=', 'product'),
            ('active', '=', True)
        ])
        
        predictions_created = 0
        for product in products:
            # Check if prediction already exists for today
            existing = self.search([
                ('product_id', '=', product.id),
                ('prediction_date', '=', fields.Date.today())
            ])
            
            if not existing:
                prediction = self.create({
                    'product_id': product.id,
                    'prediction_period': 'week',
                    'prediction_method': 'hybrid',
                })
                prediction.action_generate_prediction()
                predictions_created += 1
        
        _logger.info(f"Generated {predictions_created} predictions")
        return True


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    prediction_ids = fields.One2many('stock.prediction', 'product_tmpl_id', string='Predictions')
    prediction_count = fields.Integer('Prediction Count', compute='_compute_prediction_count')
    latest_prediction = fields.Float('Latest Prediction', compute='_compute_latest_prediction')
    
    @api.depends('prediction_ids')
    def _compute_prediction_count(self):
        for product in self:
            product.prediction_count = len(product.prediction_ids)
    
    @api.depends('prediction_ids')
    def _compute_latest_prediction(self):
        for product in self:
            latest = product.prediction_ids.sorted('prediction_date', reverse=True)[:1]
            product.latest_prediction = latest.predicted_demand if latest else 0.0
    
    def action_view_predictions(self):
        """View all predictions for this product"""
        self.ensure_one()
        return {
            'name': 'Stock Predictions',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.prediction',
            'view_mode': 'tree,form,graph',
            'domain': [('product_tmpl_id', '=', self.id)],
            'context': {'default_product_id': self.product_variant_id.id}
        }
