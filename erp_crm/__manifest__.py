# -*- coding: utf-8 -*-
{
    'name': 'ERP CRM',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Customer Relationship Management System',
    'description': """
        CRM Module
        ==========
        * Lead and opportunity tracking
        * Follow-ups and activity scheduling
        * Conversion analytics
        * Email notifications
        * Sales pipeline management
    """,
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'crm', 'mail', 'erp_sales'],
    'data': [
        'security/crm_security.xml',
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
