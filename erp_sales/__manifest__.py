# -*- coding: utf-8 -*-
{
    'name': 'ERP Sales Management',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Complete Sales and Customer Management System',
    'description': """
        Sales Management Module
        =======================
        * Customer registration and management
        * Quotation and order creation
        * Invoice generation (PDF)
        * Payment tracking
        * Historical sales data for AI predictions
        * Sales analytics and reporting
    """,
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'sale', 'account', 'erp_inventory'],
    'data': [
        'security/sales_security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/customer_views.xml',
        'views/menu_views.xml',
        'reports/sale_report_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
