# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    # Additional attendance fields
    work_hours = fields.Float('Work Hours', compute='_compute_work_hours', store=True)
    overtime_hours = fields.Float('Overtime Hours', compute='_compute_overtime', store=True)
    is_late = fields.Boolean('Late Arrival', compute='_compute_late_arrival')
    late_minutes = fields.Integer('Late by (minutes)', compute='_compute_late_arrival')
    attendance_status = fields.Selection([
        ('present', 'Present'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('overtime', 'Overtime'),
    ], string='Status', compute='_compute_attendance_status', store=True)
    
    notes = fields.Text('Notes')
    
    @api.depends('check_in', 'check_out')
    def _compute_work_hours(self):
        """Calculate total work hours"""
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                attendance.work_hours = delta.total_seconds() / 3600
            else:
                attendance.work_hours = 0.0
    
    @api.depends('work_hours')
    def _compute_overtime(self):
        """Calculate overtime hours (assuming 8 hours standard)"""
        for attendance in self:
            standard_hours = 8.0
            if attendance.work_hours > standard_hours:
                attendance.overtime_hours = attendance.work_hours - standard_hours
            else:
                attendance.overtime_hours = 0.0
    
    @api.depends('check_in')
    def _compute_late_arrival(self):
        """Check if employee arrived late (assuming 9 AM start time)"""
        for attendance in self:
            if attendance.check_in:
                check_in_time = attendance.check_in.time()
                standard_time = datetime.strptime('09:00:00', '%H:%M:%S').time()
                
                if check_in_time > standard_time:
                    attendance.is_late = True
                    # Calculate late minutes
                    check_in_dt = datetime.combine(date.today(), check_in_time)
                    standard_dt = datetime.combine(date.today(), standard_time)
                    attendance.late_minutes = int((check_in_dt - standard_dt).total_seconds() / 60)
                else:
                    attendance.is_late = False
                    attendance.late_minutes = 0
            else:
                attendance.is_late = False
                attendance.late_minutes = 0
    
    @api.depends('work_hours', 'is_late', 'overtime_hours')
    def _compute_attendance_status(self):
        """Determine attendance status"""
        for attendance in self:
            if attendance.overtime_hours > 0:
                attendance.attendance_status = 'overtime'
            elif attendance.is_late:
                attendance.attendance_status = 'late'
            elif attendance.work_hours < 4:
                attendance.attendance_status = 'half_day'
            else:
                attendance.attendance_status = 'present'


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # Additional leave fields
    leave_reason = fields.Text('Reason for Leave', required=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approval_date = fields.Datetime('Approval Date', readonly=True)
    rejection_reason = fields.Text('Rejection Reason')
    
    def action_approve(self):
        """Override approve to track approver"""
        res = super(HrLeave, self).action_approve()
        for leave in self:
            leave.approved_by = self.env.user
            leave.approval_date = fields.Datetime.now()
        return res
    
    def action_refuse(self):
        """Override refuse to require rejection reason"""
        for leave in self:
            if not leave.rejection_reason:
                raise ValidationError("Please provide a reason for rejecting this leave request!")
        return super(HrLeave, self).action_refuse()
