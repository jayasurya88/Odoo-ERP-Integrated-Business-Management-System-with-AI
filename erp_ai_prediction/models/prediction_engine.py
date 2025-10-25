# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta

try:
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
except ImportError:
    np = None
    pd = None
    LinearRegression = None
    StandardScaler = None

_logger = logging.getLogger(__name__)


class PredictionEngine:
    """AI Engine for stock demand prediction"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        
    def prepare_sales_data(self, sale_order_lines):
        """
        Prepare historical sales data for prediction
        
        Args:
            sale_order_lines: recordset of sale.order.line
            
        Returns:
            pandas DataFrame with prepared data
        """
        if not pd:
            _logger.error("Pandas not installed. Cannot prepare data.")
            return None
            
        data = []
        for line in sale_order_lines:
            if line.order_id.state in ['sale', 'done']:
                data.append({
                    'date': line.order_id.date_order,
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price': line.price_unit,
                    'day_of_week': line.order_id.date_order.weekday(),
                    'month': line.order_id.date_order.month,
                })
        
        if not data:
            return None
            
        df = pd.DataFrame(data)
        return df
    
    def calculate_moving_average(self, sales_data, window=7):
        """
        Calculate moving average for demand prediction
        
        Args:
            sales_data: list of quantities
            window: number of periods for moving average
            
        Returns:
            predicted quantity
        """
        if not sales_data or len(sales_data) == 0:
            return 0.0
            
        if len(sales_data) < window:
            return sum(sales_data) / len(sales_data)
        
        recent_sales = sales_data[-window:]
        return sum(recent_sales) / len(recent_sales)
    
    def predict_with_linear_regression(self, df, product_id):
        """
        Predict demand using linear regression
        
        Args:
            df: pandas DataFrame with historical data
            product_id: product ID to predict
            
        Returns:
            predicted quantity
        """
        if not LinearRegression or not np:
            _logger.error("Scikit-learn not installed. Cannot use linear regression.")
            return 0.0
        
        # Filter data for specific product
        product_data = df[df['product_id'] == product_id].copy()
        
        if len(product_data) < 3:
            # Not enough data for regression
            return self.calculate_moving_average(product_data['quantity'].tolist())
        
        # Create time-based features
        product_data['days_since_start'] = (product_data['date'] - product_data['date'].min()).dt.days
        
        # Prepare features and target
        X = product_data[['days_since_start', 'day_of_week', 'month']].values
        y = product_data['quantity'].values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict for next period (7 days ahead)
        max_days = product_data['days_since_start'].max()
        next_period = [[max_days + 7, datetime.now().weekday(), datetime.now().month]]
        prediction = model.predict(next_period)[0]
        
        return max(0, prediction)  # Ensure non-negative
    
    def predict_demand(self, df, product_id, method='hybrid'):
        """
        Predict demand using specified method
        
        Args:
            df: pandas DataFrame with historical data
            product_id: product ID to predict
            method: 'moving_average', 'linear_regression', or 'hybrid'
            
        Returns:
            predicted quantity
        """
        if df is None or len(df) == 0:
            return 0.0
        
        product_data = df[df['product_id'] == product_id]
        
        if len(product_data) == 0:
            return 0.0
        
        if method == 'moving_average':
            return self.calculate_moving_average(product_data['quantity'].tolist())
        
        elif method == 'linear_regression':
            return self.predict_with_linear_regression(df, product_id)
        
        elif method == 'hybrid':
            # Use both methods and average
            ma_pred = self.calculate_moving_average(product_data['quantity'].tolist())
            lr_pred = self.predict_with_linear_regression(df, product_id)
            return (ma_pred + lr_pred) / 2
        
        return 0.0
    
    def calculate_reorder_quantity(self, predicted_demand, current_stock, min_stock, max_stock, safety_factor=1.2):
        """
        Calculate optimal reorder quantity
        
        Args:
            predicted_demand: predicted demand quantity
            current_stock: current stock level
            min_stock: minimum stock level
            max_stock: maximum stock level
            safety_factor: safety stock multiplier
            
        Returns:
            recommended reorder quantity
        """
        # Calculate safety stock
        safety_stock = predicted_demand * safety_factor
        
        # Calculate reorder point
        reorder_point = min_stock + safety_stock
        
        # If current stock is below reorder point, calculate order quantity
        if current_stock < reorder_point:
            # Order enough to reach max stock plus predicted demand
            order_qty = max_stock - current_stock + predicted_demand
            return max(0, order_qty)
        
        return 0.0
    
    def calculate_accuracy(self, predicted, actual):
        """
        Calculate prediction accuracy
        
        Args:
            predicted: predicted value
            actual: actual value
            
        Returns:
            accuracy percentage
        """
        if actual == 0:
            return 0.0
        
        error = abs(predicted - actual)
        accuracy = max(0, 100 - (error / actual * 100))
        return accuracy
