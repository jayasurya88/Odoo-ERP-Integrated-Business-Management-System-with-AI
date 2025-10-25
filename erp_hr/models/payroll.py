# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class HrPayslip(models.Model):
    _name = 'hr.payslip'
    _description = 'Employee Payslip'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_from desc'

    name = fields.Char('Payslip Reference', required=True, copy=False, readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department', store=True)
    job_id = fields.Many2one('hr.job', related='employee_id.job_id', string='Job Position', store=True)
    
    # Date range
    date_from = fields.Date('Date From', required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date('Date To', required=True)
    
    # Salary components
    basic_salary = fields.Monetary('Basic Salary', related='employee_id.basic_salary', currency_field='currency_id')
    allowances = fields.Monetary('Allowances', related='employee_id.allowances', currency_field='currency_id')
    
    # Deductions
    tax_deduction = fields.Monetary('Tax Deduction', currency_field='currency_id')
    insurance_deduction = fields.Monetary('Insurance', currency_field='currency_id')
    other_deductions = fields.Monetary('Other Deductions', currency_field='currency_id')
    total_deductions = fields.Monetary('Total Deductions', compute='_compute_totals', store=True, currency_field='currency_id')
    
    # Bonuses and overtime
    overtime_hours = fields.Float('Overtime Hours')
    overtime_amount = fields.Monetary('Overtime Amount', compute='_compute_overtime_amount', currency_field='currency_id')
    bonus = fields.Monetary('Bonus', currency_field='currency_id')
    
    # Totals
    gross_salary = fields.Monetary('Gross Salary', compute='_compute_totals', store=True, currency_field='currency_id')
    net_salary = fields.Monetary('Net Salary', compute='_compute_totals', store=True, currency_field='currency_id')
    
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting for Verification'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    
    # Payment
    payment_date = fields.Date('Payment Date')
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
    ], string='Payment Method')
    
    notes = fields.Text('Notes')
    
    @api.model
    def create(self, vals):
        """Generate sequence for payslip"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.payslip') or 'New'
        return super(HrPayslip, self).create(vals)
    
    @api.depends('overtime_hours', 'employee_id.basic_salary')
    def _compute_overtime_amount(self):
        """Calculate overtime payment (1.5x hourly rate)"""
        for payslip in self:
            if payslip.basic_salary and payslip.overtime_hours:
                # Assuming 160 working hours per month
                hourly_rate = payslip.basic_salary / 160
                payslip.overtime_amount = payslip.overtime_hours * hourly_rate * 1.5
            else:
                payslip.overtime_amount = 0.0
    
    @api.depends('basic_salary', 'allowances', 'overtime_amount', 'bonus', 
                 'tax_deduction', 'insurance_deduction', 'other_deductions')
    def _compute_totals(self):
        """Calculate gross and net salary"""
        for payslip in self:
            payslip.gross_salary = (payslip.basic_salary + payslip.allowances + 
                                   payslip.overtime_amount + payslip.bonus)
            payslip.total_deductions = (payslip.tax_deduction + payslip.insurance_deduction + 
                                       payslip.other_deductions)
            payslip.net_salary = payslip.gross_salary - payslip.total_deductions
    
    def action_verify(self):
        """Move payslip to verification"""
        self.write({'state': 'verify'})
    
    def action_done(self):
        """Mark payslip as done"""
        self.write({
            'state': 'done',
            'payment_date': fields.Date.today()
        })
    
    def action_cancel(self):
        """Cancel payslip"""
        self.write({'state': 'cancel'})
    
    def action_draft(self):
        """Reset to draft"""
        self.write({'state': 'draft'})
    
    def action_print_payslip(self):
        """Print payslip report"""
        return self.env.ref('erp_hr.action_report_payslip').report_action(self)
