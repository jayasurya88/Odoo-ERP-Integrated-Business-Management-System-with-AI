# -*- coding: utf-8 -*-
{
    'name': 'ERP AI Stock Prediction',
    'version': '17.0.1.0.0',
    'category': 'Inventory/AI',
    'summary': 'AI-based Stock Demand Prediction and Reorder Suggestions',
    'description': """
        AI Prediction Module
        ====================
        * Analyze historical sales data
        * Predict product demand for next week/month
        * Recommend optimal reorder quantities
        * Display predicted vs actual sales comparison
        * Alert for potential stockouts
        * Uses linear regression and moving average algorithms
    """,
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'erp_inventory', 'erp_sales'],
    'external_dependencies': {
        'python': ['numpy', 'pandas', 'sklearn'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/prediction_views.xml',
        'views/menu_views.xml',
        'data/prediction_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
