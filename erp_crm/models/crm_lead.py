# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Lead scoring and classification
    lead_score = fields.Integer('Lead Score', default=0, help="Score based on engagement and potential")
    lead_quality = fields.Selection([
        ('cold', 'Cold'),
        ('warm', 'Warm'),
        ('hot', 'Hot'),
    ], string='Lead Quality', compute='_compute_lead_quality', store=True)
    
    # Source tracking
    lead_source_detail = fields.Char('Source Detail')
    campaign_id = fields.Many2one('utm.campaign', string='Campaign')
    
    # Engagement tracking
    last_contact_date = fields.Date('Last Contact Date')
    next_followup_date = fields.Date('Next Follow-up Date')
    contact_count = fields.Integer('Contact Count', default=0)
    days_since_last_contact = fields.Integer('Days Since Last Contact', compute='_compute_days_since_contact')
    
    # Conversion tracking
    conversion_probability = fields.Float('Conversion Probability %', default=0.0)
    estimated_revenue = fields.Monetary('Estimated Revenue', currency_field='company_currency')
    actual_revenue = fields.Monetary('Actual Revenue', currency_field='company_currency')
    
    # Customer information
    industry = fields.Char('Industry')
    company_size = fields.Selection([
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('500+', '500+ employees'),
    ], string='Company Size')
    
    # Status tracking
    is_qualified = fields.Boolean('Qualified Lead', default=False)
    qualification_date = fields.Date('Qualification Date')
    lost_reason_detail = fields.Text('Lost Reason Detail')
    
    @api.depends('lead_score')
    def _compute_lead_quality(self):
        """Classify lead quality based on score"""
        for lead in self:
            if lead.lead_score >= 70:
                lead.lead_quality = 'hot'
            elif lead.lead_score >= 40:
                lead.lead_quality = 'warm'
            else:
                lead.lead_quality = 'cold'
    
    @api.depends('last_contact_date')
    def _compute_days_since_contact(self):
        """Calculate days since last contact"""
        for lead in self:
            if lead.last_contact_date:
                delta = fields.Date.today() - lead.last_contact_date
                lead.days_since_last_contact = delta.days
            else:
                lead.days_since_last_contact = 0
    
    def action_log_contact(self):
        """Log a contact with the lead"""
        self.ensure_one()
        self.last_contact_date = fields.Date.today()
        self.contact_count += 1
        # Increase lead score for engagement
        self.lead_score = min(self.lead_score + 5, 100)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Contact Logged',
                'message': f'Contact logged for {self.name}',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_qualify_lead(self):
        """Mark lead as qualified"""
        self.ensure_one()
        self.is_qualified = True
        self.qualification_date = fields.Date.today()
        self.lead_score = min(self.lead_score + 20, 100)
        return self.action_set_won()
    
    def action_schedule_followup(self):
        """Schedule a follow-up activity"""
        self.ensure_one()
        return {
            'name': 'Schedule Follow-up',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'context': {
                'default_res_id': self.id,
                'default_res_model': 'crm.lead',
                'default_summary': f'Follow-up: {self.name}',
            },
            'target': 'new',
        }


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    # Stage analytics
    average_days_in_stage = fields.Float('Avg Days in Stage', compute='_compute_stage_analytics')
    conversion_rate = fields.Float('Conversion Rate %', compute='_compute_stage_analytics')
    
    def _compute_stage_analytics(self):
        """Calculate stage analytics"""
        for stage in self:
            leads_in_stage = self.env['crm.lead'].search([('stage_id', '=', stage.id)])
            stage.average_days_in_stage = 7.0  # Simplified - would need actual calculation
            stage.conversion_rate = 50.0  # Simplified - would need actual calculation


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    # Team performance metrics
    total_leads = fields.Integer('Total Leads', compute='_compute_team_stats')
    converted_leads = fields.Integer('Converted Leads', compute='_compute_team_stats')
    team_conversion_rate = fields.Float('Team Conversion Rate %', compute='_compute_team_stats')
    total_revenue = fields.Monetary('Total Revenue', compute='_compute_team_stats', currency_field='currency_id')
    
    def _compute_team_stats(self):
        """Calculate team statistics"""
        for team in self:
            team_leads = self.env['crm.lead'].search([('team_id', '=', team.id)])
            team.total_leads = len(team_leads)
            team.converted_leads = len(team_leads.filtered(lambda l: l.stage_id.is_won))
            team.team_conversion_rate = (team.converted_leads / team.total_leads * 100) if team.total_leads > 0 else 0
            team.total_revenue = sum(team_leads.filtered(lambda l: l.stage_id.is_won).mapped('actual_revenue'))
