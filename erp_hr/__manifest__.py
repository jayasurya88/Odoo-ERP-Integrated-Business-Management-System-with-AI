# -*- coding: utf-8 -*-
{
    'name': 'ERP HR & Payroll Management',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Complete HR and Payroll Management System',
    'description': """
        HR & Payroll Management Module
        ===============================
        * Employee registration and profile management
        * Attendance and leave management
        * Salary computation and payslip generation
        * Role-based access control
        * Performance tracking
        * Department and job position management
    """,
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'hr', 'hr_attendance', 'hr_holidays', 'hr_contract'],
    'data': [
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/attendance_views.xml',
        'views/payroll_views.xml',
        'views/menu_views.xml',
        'reports/payslip_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
