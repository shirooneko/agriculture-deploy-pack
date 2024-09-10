from odoo import models, fields, api

class AgriTask(models.Model):
    _name = 'agri.task'
    _description = 'Agriculture Task'

    actual_completion_date = fields.Datetime(string='Actual Completion Date', compute='_compute_actual_completion_date', store=True)
    attachment = fields.Binary(string='Attachment')
    completed_by = fields.Many2one('res.users', string='Completed By', default=lambda self: self.env.user.id)
    delta_completion_days = fields.Integer(string='Days Late', compute='_compute_delta_completion_days', store=True)
    is_completed = fields.Boolean(string='Completed?', default=False, store=True)
    is_optional = fields.Boolean(string='Optional Task?', store=True)
    name = fields.Char(string='Name', compute='_compute_task_name', inverse='_set_task_name', required=True, store=True)
    notes = fields.Html(string='Notes')
    project_ids = fields.Many2many('project.project', string='Projects')
    pic_ids = fields.Many2many('res.users', string='PICs')
    planned_completion_date = fields.Datetime(string='Planned Completion Date', store=True)
    sequence = fields.Integer(string='Sequence')
    stage_id = fields.Many2one('agri.stage', string='State')
    target_days_completed = fields.Integer(string='Target Days')
    task_template_id = fields.Many2one('agri.task.template', string='Task')
