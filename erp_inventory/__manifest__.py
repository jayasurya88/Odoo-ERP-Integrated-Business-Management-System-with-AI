# -*- coding: utf-8 -*-
{
    'name': 'ERP Inventory Management',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Complete Inventory and Warehouse Management System',
    'description': """
        Inventory Management Module
        ============================
        * Product creation and categorization
        * Multi-warehouse support
        * Stock tracking and movements
        * Barcode/QR code scanning
        * Low-stock alerts and reorder suggestions
        * Integration with AI prediction module
    """,
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'product', 'stock'],
    'data': [
        'security/inventory_security.xml',
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/warehouse_views.xml',
        'views/stock_move_views.xml',
        'views/menu_views.xml',
        'data/product_category_data.xml',
        'reports/inventory_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
