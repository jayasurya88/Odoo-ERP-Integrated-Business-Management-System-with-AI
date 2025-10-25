# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Personal Information
    date_of_birth = fields.Date('Date of Birth')
    age = fields.Integer('Age', compute='_compute_age', store=True)
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('o+', 'O+'), ('o-', 'O-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
    ], string='Blood Group')
    emergency_contact = fields.Char('Emergency Contact')
    emergency_phone = fields.Char('Emergency Phone')
    
    # Employment Details
    employee_code = fields.Char('Employee Code', required=True, copy=False)
    date_of_joining = fields.Date('Date of Joining', default=fields.Date.today)
    date_of_leaving = fields.Date('Date of Leaving')
    employment_status = fields.Selection([
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
    ], string='Employment Status', default='active')
    
    probation_period = fields.Integer('Probation Period (months)', default=3)
    is_probation = fields.Boolean('On Probation', compute='_compute_probation_status')
    
    # Salary Information
    basic_salary = fields.Monetary('Basic Salary', currency_field='currency_id')
    allowances = fields.Monetary('Allowances', currency_field='currency_id')
    deductions = fields.Monetary('Deductions', currency_field='currency_id')
    net_salary = fields.Monetary('Net Salary', compute='_compute_net_salary', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    # Performance
    performance_rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Below Average'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent'),
    ], string='Performance Rating')
    
    # Statistics
    total_leaves_taken = fields.Integer('Total Leaves Taken', compute='_compute_leave_stats')
    total_working_days = fields.Integer('Total Working Days', compute='_compute_attendance_stats')
    attendance_percentage = fields.Float('Attendance %', compute='_compute_attendance_stats')
    
    # Bank Details
    bank_account_number = fields.Char('Bank Account Number')
    bank_name = fields.Char('Bank Name')
    ifsc_code = fields.Char('IFSC Code')
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        """Calculate employee age"""
        for employee in self:
            if employee.date_of_birth:
                today = date.today()
                employee.age = today.year - employee.date_of_birth.year - (
                    (today.month, today.day) < (employee.date_of_birth.month, employee.date_of_birth.day)
                )
            else:
                employee.age = 0
    
    @api.depends('date_of_joining', 'probation_period')
    def _compute_probation_status(self):
        """Check if employee is still on probation"""
        for employee in self:
            if employee.date_of_joining:
                from dateutil.relativedelta import relativedelta
                probation_end = employee.date_of_joining + relativedelta(months=employee.probation_period)
                employee.is_probation = date.today() < probation_end
            else:
                employee.is_probation = False
    
    @api.depends('basic_salary', 'allowances', 'deductions')
    def _compute_net_salary(self):
        """Calculate net salary"""
        for employee in self:
            employee.net_salary = employee.basic_salary + employee.allowances - employee.deductions
    
    def _compute_leave_stats(self):
        """Calculate total leaves taken"""
        for employee in self:
            leaves = self.env['hr.leave'].search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'validate')
            ])
            employee.total_leaves_taken = sum(leaves.mapped('number_of_days'))
    
    def _compute_attendance_stats(self):
        """Calculate attendance statistics"""
        for employee in self:
            if employee.date_of_joining:
                days_since_joining = (date.today() - employee.date_of_joining).days
                attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', employee.id),
                    ('check_out', '!=', False)
                ])
                employee.total_working_days = len(set(attendances.mapped(lambda a: a.check_in.date())))
                employee.attendance_percentage = (employee.total_working_days / days_since_joining * 100) if days_since_joining > 0 else 0
            else:
                employee.total_working_days = 0
                employee.attendance_percentage = 0
    
    @api.constrains('employee_code')
    def _check_employee_code(self):
        """Ensure employee code is unique"""
        for employee in self:
            if self.search_count([('employee_code', '=', employee.employee_code), ('id', '!=', employee.id)]) > 0:
                raise ValidationError(f"Employee code {employee.employee_code} already exists!")
    
    def action_generate_payslip(self):
        """Generate payslip for employee"""
        self.ensure_one()
        return {
            'name': 'Generate Payslip',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip',
            'view_mode': 'form',
            'context': {'default_employee_id': self.id},
            'target': 'new',
        }


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    # Department details
    department_head = fields.Many2one('hr.employee', string='Department Head')
    budget = fields.Monetary('Department Budget', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    employee_count = fields.Integer('Employee Count', compute='_compute_employee_count')
    
    @api.depends('member_ids')
    def _compute_employee_count(self):
        """Count employees in department"""
        for dept in self:
            dept.employee_count = len(dept.member_ids)
